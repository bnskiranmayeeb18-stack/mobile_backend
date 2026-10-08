pipeline {
    agent any
    stages {
        stage('Install Deps') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Run Automated Tests') {
            steps {
                bat 'pytest tests/ -v --junitxml=report.xml --cov=rides --cov=core --cov-report=term-missing'
            }
        }
    }
    post {
        always {
            junit 'report.xml'
            archiveArtifacts artifacts: 'report.xml', fingerprint: true
        }
    }
}
