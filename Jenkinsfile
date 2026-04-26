pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_IMAGE = "krishnakumar2022us70010/aceest-fitness"
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh 'python3 -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    mkdir -p reports
                    . venv/bin/activate

                    python -m pytest \
                        --junitxml=reports/test-results.xml \
                        --cov=. \
                        --cov-report=xml:reports/coverage.xml
                '''
            }

            post {
                always {
                    junit 'reports/test-results.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
    steps {
        withSonarQubeEnv('SonarQube') {
            withEnv(["PATH+SONAR=${tool 'SonarScanner'}/bin"]) {
                sh '''
                sonar-scanner \
                  -Dsonar.projectKey=aceest-fitness \
                  -Dsonar.sources=. \
                  -Dsonar.host.url=$SONAR_HOST_URL \
                  -Dsonar.login=$SONAR_TOKEN \
                  -Dsonar.python.coverage.reportPaths=reports/coverage.xml
                '''
            }
        }
    }
}


        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker version || echo "Docker not available"'
            }
        }

        stage('Docker Build & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .
                        docker tag $DOCKER_IMAGE:$BUILD_NUMBER $DOCKER_IMAGE:latest

                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        docker push $DOCKER_IMAGE:$BUILD_NUMBER
                        docker push $DOCKER_IMAGE:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS'
        }
        failure {
            echo 'Pipeline FAILED'
        }
    }
}
