pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                '''
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
                . venv/bin/activate

                # Create reports directory to avoid permission issues
                mkdir -p reports

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
                echo "SonarQube stage (kept for pipeline flow)"
                // If you have sonar scanner installed, uncomment below:

                /*
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    . venv/bin/activate
                    sonar-scanner
                    '''
                }
                */
            }
        }

        stage('Quality Gate') {
            steps {
                echo "Quality Gate stage (optional wait step)"
                // If SonarQube is enabled, you can add:
                // timeout(time: 2, unit: 'MINUTES') {
                //     waitForQualityGate abortPipeline: true
                // }
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Docker Build & Push') {
            steps {
                sh '''
                echo "Building Docker Image..."
                docker build -t myapp:latest .

                echo "Logging into Docker Hub..."
                echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin

                echo "Pushing Image..."
                docker tag myapp:latest yourdockerhubusername/myapp:latest
                docker push yourdockerhubusername/myapp:latest
                '''
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
