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
                sh 'python3 -m pip install -r requirements.txt || true'
                sh 'python3 -m pip install pytest pytest-cov'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m pytest --junitxml=test-results.xml --cov=. --cov-report=xml'
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
                    sh 'sonar-scanner -Dsonar.login=$SONAR_TOKEN'
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

        stage('Docker Build & Push') {
            steps {
                sh "docker build -t $DOCKER_IMAGE:$BUILD_NUMBER ."
                sh "docker tag $DOCKER_IMAGE:$BUILD_NUMBER $DOCKER_IMAGE:latest"
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                sh "docker push $DOCKER_IMAGE:$BUILD_NUMBER"
                sh "docker push $DOCKER_IMAGE:latest"
            }
        }

        // ❗ Disable Kubernetes for now
        // stage('Deploy to Kubernetes') {
        //     steps {
        //         sh "kubectl apply -f k8s/deployment.yaml"
        //         sh "kubectl apply -f k8s/service.yaml"
        //     }
        // }
    }

    post {
        failure {
            echo 'Pipeline FAILED!'
        }
        success {
            echo 'Pipeline SUCCESS — deployed!'
        }
    }
}
