pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '339712764097.dkr.ecr.us-east-1.amazonaws.com/my-repository'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Atharvajawale/task-gdc.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${env.ECR_REPO}:latest")
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    docker.withRegistry('https://339712764097.dkr.ecr.us-east-1.amazonaws.com', 'ecr:us-east-1:aws_credentials') {
                        docker.image("${env.ECR_REPO}:latest").push()
                    }
                }
            }
        }
        stage('Deploy Lambda') {
            steps {
                script {
                    sh 'aws lambda update-function-code --function-name my-function --image-uri ${env.ECR_REPO}:latest --region ${env.AWS_REGION}'
                }
            }
        }
    }
}
