pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-u root'
        }
    }

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

        stage('Install Dependencies') {
            steps {
                sh '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest pytest-cov
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                python -m pytest --junitxml=test-results.xml --cov=. --cov-report=xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    /opt/sonar-scanner/bin/sonar-scanner \
                    -Dsonar.projectKey=aceest-fitness \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=$SONAR_HOST_URL \
                    -Dsonar.login=$SONAR_TOKEN
                    '''
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
                sh '''
                docker version || true
                '''
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh """
                docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .
                docker tag $DOCKER_IMAGE:$BUILD_NUMBER $DOCKER_IMAGE:latest

                echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin

                docker push $DOCKER_IMAGE:$BUILD_NUMBER
                docker push $DOCKER_IMAGE:latest
                """
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
