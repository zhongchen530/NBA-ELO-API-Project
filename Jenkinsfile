pipeline {
    agent any
    environment{
        registryName = "django_nba"
        registryCredential = "ACR"
        registryUrl = "djangonba.azurecr.io"
    }
    stages {
        stage('Build') {
            steps {
                script{
                    def dockerImage = docker.build(tags:registryName,context:".\Django_NBA")
                    docker.withRegistry( "http://${registryUrl}", registryCredential ) {
                    dockerImage.push()
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                withKubeConfig([credentialsId: 'K8S', serverUrl: '']) {
                sh ('kubectl apply -f  ./kubernetes_files/Database-secrets.yml')
                sh ('kubectl apply -f  ./kubernetes_files/Services-Config.yml')
                sh ('kubectl apply -f  ./kubernetes_files/Redis.yml')
                sh ('kubectl apply -f  ./kubernetes_files/Django.yml')
                sh ('kubectl apply -f  ./kubernetes_files/Celery.yml')
                sh ('kubectl apply -f  ./kubernetes_files/Celery-beat.yml')
                }
            }
        }
    }
}
}