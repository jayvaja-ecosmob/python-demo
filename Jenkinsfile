pipeline {
    agent any
    environment {
        IMAGE_NAME = "jayv1161/python-demo"
        APP_VERSION = "3.0"
        IMAGE_TAG = "v${APP_VERSION}.${BUILD_NUMBER}"
    }
    stages {
        stage('Clone Repo') {
            steps {
                git branch: env.BRANCH_NAME, url: 'https://github.com/jayvaja-ecosmob/python-demo.git'
            }
        }

        stage('SonarQube Analysis') {
            environment {
                scannerHome = tool 'sonar-scanner'
            }
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                    ${scannerHome}/bin/sonar-scanner \
                    -Dsonar.projectKey=python-demo \
                    -Dsonar.projectName=python-demo \
                    -Dsonar.sources=.
                    """
                }
            }
        }

        stage('Run Python Script') {
            steps {
                sh 'python3 app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $IMAGE_NAME:$IMAGE_TAG
                    docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy to Dev Server (Server A)') {
            when {
                branch 'dev'
            }
            steps {
                sshagent(['serverA-ssh']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@172.31.16.199 "
                    docker pull jayv1161/python-demo:latest
                    docker stop python-demo || true
                    docker rm python-demo || true
                    docker run -d --name python-demo jayv1161/python-demo:latest
                    "
                    '''
                }
            }
        }

        stage('Deploy to QA Server (Server B)') {
            when {
                branch 'QA'
            }
            steps {
                sshagent(['serverB-ssh']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@172.31.66.75 "
                    docker pull jayv1161/python-demo:latest
                    docker stop python-demo || true
                    docker rm python-demo || true
                    docker run -d --name python-demo jayv1161/python-demo:latest
                    "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded on branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "Pipeline failed on branch: ${env.BRANCH_NAME}"
        }
    }
}
