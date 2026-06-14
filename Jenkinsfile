pipeline {
    agent any
    
    options {
        skipDefaultCheckout(true)
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }
    
    environment {
        APP_NAME = 'LabFull'
        PUBLIC_URL = 'https://labfull.maurocastro.cl'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Validate Dependencies') {
            steps {
                sh 'bash ./scripts/validate_deps.sh'
            }
        }
        
        stage('Deploy Minikube') {
            steps {
                script {
                    load 'vars/deployMinikube.groovy'
                    deployMinikube(
                        host: '192.168.1.12',
                        user: 'mauro',
                        publicUrl: env.PUBLIC_URL
                    )
                }
            }
        }
        
        stage('Notify ClawCode') {
            steps {
                script {
                    load 'vars/notifyClawCode.groovy'
                    notifyClawCode(
                        app: env.APP_NAME,
                        publicUrl: env.PUBLIC_URL
                    )
                }
            }
        }
    }
    
    post {
        success {
            echo "Pipeline completado exitosamente"
            cleanWs()
        }
        failure {
            echo 'Pipeline falló. Revisar los logs.'
        }
    }
}
