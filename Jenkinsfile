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
                    trivy --version
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
                    set -e

                    mkdir -p security/trivy/reports

                    echo "========== Trivy Filesystem Scan =========="

                    echo "Scanning for HIGH and CRITICAL vulnerabilities..."

                    trivy fs \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/reports/trivy-report.json \
                        --exit-code 1 \
                        .

                    trivy fs \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format table \
                        --output security/trivy/reports/trivy-report.txt \
                        --exit-code 1 \
                        .

                    echo "========== Trivy Filesystem Scan Passed =========="
                    echo "No HIGH or CRITICAL vulnerabilities found."
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    set -e

                    echo "========== Building Docker Images =========="

                    docker build \
                        -f docker/user-service/Dockerfile \
                        -t user-service:v1 \
                        services/user-service

                    docker build \
                        -f docker/auth-service/Dockerfile \
                        -t auth-service:v1 \
                        services/auth-service

                    docker build \
                        -f docker/gateway-service/Dockerfile \
                        -t gateway-service:v1 \
                        services/gateway-service

                    docker build \
                        -f docker/logging-service/Dockerfile \
                        -t logging-service:v1 \
                        services/logging-service

                    docker build \
                        -f docker/notification-service/Dockerfile \
                        -t notification-service:v1 \
                        services/notification-service

                    echo "========== Docker Images Built Successfully =========="
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                    set -e

                    mkdir -p security/trivy/image-reports

                    echo "========== Scanning Docker Images =========="

                    echo "Security policy: HIGH and CRITICAL vulnerabilities will fail the pipeline."

                    echo "========== Scanning user-service:v1 =========="

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/user-service-report.json \
                        --exit-code 1 \
                        user-service:v1

                    echo "========== Scanning auth-service:v1 =========="

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/auth-service-report.json \
                        --exit-code 1 \
                        auth-service:v1

                    echo "========== Scanning gateway-service:v1 =========="

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/gateway-service-report.json \
                        --exit-code 1 \
                        gateway-service:v1

                    echo "========== Scanning logging-service:v1 =========="

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/logging-service-report.json \
                        --exit-code 1 \
                        logging-service:v1

                    echo "========== Scanning notification-service:v1 =========="

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/notification-service-report.json \
                        --exit-code 1 \
                        notification-service:v1

                    echo "========== Trivy Image Scan Passed =========="
                    echo "No HIGH or CRITICAL vulnerabilities found in Docker images."
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
                artifacts: 'security/trivy/reports/*,security/trivy/image-reports/*',
                fingerprint: true
            )

            cleanWs(
                deleteDirs: true,
                disableDeferredWipeout: true
            )
        }

        success {
            echo '''
====================================================

CI Pipeline completed successfully.

✔ Environment Verification
✔ Unit Tests Passed
✔ SonarQube Analysis
✔ OWASP Dependency Check
✔ Trivy Filesystem Scan
✔ Docker Images Built
✔ Trivy Image Scan

====================================================
'''
        }

        failure {
            echo '''
====================================================

CI Pipeline Failed.

Review the failed stage and console output.

If Trivy failed, check the HIGH/CRITICAL vulnerabilities
reported in the Trivy scan output and archived reports.

====================================================
'''
        }
    }
}
