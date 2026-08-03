pipeline {

    agent any

    stages {

        stage('Checkout') {

            steps {
                echo 'Checking out source code...'
            }

        }

        stage('Verify Environment') {

            steps {
                sh 'pwd'
                sh 'ls -la'
                sh 'python3 --version'
                sh 'docker --version'
            }

        }

        stage('Pipeline Status') {

            steps {
                echo 'Pipeline executed successfully!'
            }

        }

    }

}
