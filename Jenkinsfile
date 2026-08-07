pipeline {

    agent any

    options {
        timestamps()
    }

    stages {

        stage('Verify Environment') {
            steps {
                sh '''
                    set -e

                    echo "========== Environment =========="

                    python3 --version
                    pip3 --version
                    docker --version
                '''
            }
        }

        stage('User Service CI') {
            steps {
                dir('services/user-service') {
                    sh '''
                        set -e

                        rm -rf .venv
                        python3 -m venv .venv
                        . .venv/bin/activate

                        python -m pip install --upgrade pip
                        pip install -r requirements.txt

                        pytest -v --junitxml=user-test-results.xml
                    '''
                }
            }
        }

        stage('Auth Service CI') {
            steps {
                dir('services/auth-service') {
                    sh '''
                        set -e

                        rm -rf .venv
                        python3 -m venv .venv
                        . .venv/bin/activate

                        python -m pip install --upgrade pip
                        pip install -r requirements.txt

                        pytest -v --junitxml=auth-test-results.xml
                    '''
                }
            }
        }

        stage('Notification Service CI') {
            steps {
                dir('services/notification-service') {
                    sh '''
                        set -e

                        rm -rf .venv
                        python3 -m venv .venv
                        . .venv/bin/activate

                        python -m pip install --upgrade pip
                        pip install -r requirements.txt

                        pytest -v --junitxml=notification-test-results.xml
                    '''
                }
            }
        }

        stage('Logging Service CI') {
            steps {
                dir('services/logging-service') {
                    sh '''
                        set -e

                        rm -rf .venv
                        python3 -m venv .venv
                        . .venv/bin/activate

                        python -m pip install --upgrade pip
                        pip install -r requirements.txt

                        pytest -v --junitxml=logging-test-results.xml
                    '''
                }
            }
        }

        stage('Gateway Service CI') {
            steps {
                dir('services/gateway-service') {
                    sh '''
                        set -e

                        rm -rf .venv
                        python3 -m venv .venv
                        . .venv/bin/activate

                        python -m pip install --upgrade pip
                        pip install -r requirements.txt

                        pytest -v --junitxml=gateway-test-results.xml
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'Sonar'

                    withSonarQubeEnv('Sonar') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner
                        """
                    }
                }
            }
        }

        stage('OWASP Dependency Check') {
            steps {
                dependencyCheck(
                    odcInstallation: 'DependencyCheck',
                    additionalArguments: '''
                        --scan .
                        --format HTML
                        --format XML
                        --out security/dependency-check/reports
                    '''
                )
            }
        }

        stage('Trivy Filesystem Scan') {
            steps {
                sh '''
                    mkdir -p security/trivy/reports

                    trivy fs \
                        --format json \
                        --output security/trivy/reports/trivy-report.json \
                        .

                    trivy fs \
                        --format table \
                        . > security/trivy/reports/trivy-report.txt
                '''
            }
        }

    }

    post {

        always {

            junit allowEmptyResults: false,
                  testResults: '**/*-test-results.xml'

            dependencyCheckPublisher(
                pattern: 'security/dependency-check/reports/dependency-check-report.xml'
            )

            archiveArtifacts(
                artifacts: 'security/trivy/reports/*',
                fingerprint: true
            )

            cleanWs(
                deleteDirs: true,
                disableDeferredWipeout: true
            )
        }

        success {
            echo '''
=========================================
CI Pipeline completed successfully.
All unit tests passed.
SonarQube analysis completed.
OWASP Dependency Check completed.
Trivy Filesystem Scan completed.
=========================================
'''
        }

        failure {
            echo '''
=========================================
CI Pipeline failed.
Review the failed stage and console output.
=========================================
'''
        }
    }
}
