pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-python-app:latest .'
            }
        }
        
        stage('Run Container') {
            steps {
                script {
                    sh 'docker rm -f running-app || true'
                    sh 'docker run -d \
                        -p 5001:5000 \
                        --name running-app \
                        --user root \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        my-python-app:latest'
                }
            }
        }
    }
}
