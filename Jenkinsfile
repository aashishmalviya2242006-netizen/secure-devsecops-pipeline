pipeline {

    agent any

    options {
        timestamps()
    }

    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_NAMESPACE = 'aashu006'

        USER_IMAGE = 'aashu006/devsecops-user-service:v1'
        AUTH_IMAGE = 'aashu006/devsecops-auth-service:v1'
        GATEWAY_IMAGE = 'aashu006/devsecops-gateway-service:v1'
        LOGGING_IMAGE = 'aashu006/devsecops-logging-service:v1'
        NOTIFICATION_IMAGE = 'aashu006/devsecops-notification-service:v1'
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
                    cosign version
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
                    echo "Security policy: HIGH and CRITICAL findings are reported but do not block CI."

                    trivy fs \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/reports/trivy-report.json \
                        --exit-code 0 \
                        .

                    trivy fs \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format table \
                        --output security/trivy/reports/trivy-report.txt \
                        --exit-code 0 \
                        .

                    echo "========== Trivy Filesystem Scan Completed =========="
                    echo "HIGH and CRITICAL findings, if any, are available in the archived reports."
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

                    echo "========== Trivy Docker Image Security Scan =========="
                    echo "Security policy: HIGH and CRITICAL findings are reported but do not block CI."

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/user-service-report.json \
                        --exit-code 0 \
                        user-service:v1

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/auth-service-report.json \
                        --exit-code 0 \
                        auth-service:v1

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/gateway-service-report.json \
                        --exit-code 0 \
                        gateway-service:v1

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/logging-service-report.json \
                        --exit-code 0 \
                        logging-service:v1

                    trivy image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/notification-service-report.json \
                        --exit-code 0 \
                        notification-service:v1

                    echo "========== Trivy Image Scan Completed =========="
                    echo "HIGH and CRITICAL findings, if any, are available in the archived reports."
                '''
            }
        }

        stage('Push Images to Registry') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "========== Docker Registry Login =========="

                        echo "$DOCKERHUB_PASSWORD" | docker login \
                            -u "$DOCKERHUB_USERNAME" \
                            --password-stdin

                        echo "========== Tagging Images =========="

                        docker tag user-service:v1 "$USER_IMAGE"
                        docker tag auth-service:v1 "$AUTH_IMAGE"
                        docker tag gateway-service:v1 "$GATEWAY_IMAGE"
                        docker tag logging-service:v1 "$LOGGING_IMAGE"
                        docker tag notification-service:v1 "$NOTIFICATION_IMAGE"

                        echo "========== Pushing Images =========="

                        docker push "$USER_IMAGE"
                        docker push "$AUTH_IMAGE"
                        docker push "$GATEWAY_IMAGE"
                        docker push "$LOGGING_IMAGE"
                        docker push "$NOTIFICATION_IMAGE"

                        echo "========== Registry Push Completed =========="
                    '''
                }
            }
        }

        stage('Get Image Digests') {
            steps {
                script {

                    env.USER_DIGEST = sh(
                        script: "docker inspect --format='{{index .RepoDigests 0}}' ${env.USER_IMAGE}",
                        returnStdout: true
                    ).trim()

                    env.AUTH_DIGEST = sh(
                        script: "docker inspect --format='{{index .RepoDigests 0}}' ${env.AUTH_IMAGE}",
                        returnStdout: true
                    ).trim()

                    env.GATEWAY_DIGEST = sh(
                        script: "docker inspect --format='{{index .RepoDigests 0}}' ${env.GATEWAY_IMAGE}",
                        returnStdout: true
                    ).trim()

                    env.LOGGING_DIGEST = sh(
                        script: "docker inspect --format='{{index .RepoDigests 0}}' ${env.LOGGING_IMAGE}",
                        returnStdout: true
                    ).trim()

                    env.NOTIFICATION_DIGEST = sh(
                        script: "docker inspect --format='{{index .RepoDigests 0}}' ${env.NOTIFICATION_IMAGE}",
                        returnStdout: true
                    ).trim()

                    echo "========== IMAGE DIGESTS =========="
                    echo "User:         ${env.USER_DIGEST}"
                    echo "Auth:         ${env.AUTH_DIGEST}"
                    echo "Gateway:      ${env.GATEWAY_DIGEST}"
                    echo "Logging:      ${env.LOGGING_DIGEST}"
                    echo "Notification: ${env.NOTIFICATION_DIGEST}"
                }
            }
        }

        stage('Cosign Sign Images') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'cosign-private-key',
                        variable: 'COSIGN_KEY'
                    ),
                    string(
                        credentialsId: 'cosign-key-password',
                        variable: 'COSIGN_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "========== Cosign Signing =========="

                        cosign sign \
                            --yes \
                            --key "$COSIGN_KEY" \
                            "$USER_DIGEST"

                        cosign sign \
                            --yes \
                            --key "$COSIGN_KEY" \
                            "$AUTH_DIGEST"

                        cosign sign \
                            --yes \
                            --key "$COSIGN_KEY" \
                            "$GATEWAY_DIGEST"

                        cosign sign \
                            --yes \
                            --key "$COSIGN_KEY" \
                            "$LOGGING_DIGEST"

                        cosign sign \
                            --yes \
                            --key "$COSIGN_KEY" \
                            "$NOTIFICATION_DIGEST"

                        echo "========== All Images Signed Successfully =========="
                    '''
                }
            }
        }

        stage('Cosign Verify Images') {
            steps {
                sh '''
                    set -e

                    echo "========== Cosign Verification =========="

                    test -f cosign.pub

                    cosign verify \
                        --key cosign.pub \
                        "$USER_DIGEST"

                    cosign verify \
                        --key cosign.pub \
                        "$AUTH_DIGEST"

                    cosign verify \
                        --key cosign.pub \
                        "$GATEWAY_DIGEST"

                    cosign verify \
                        --key cosign.pub \
                        "$LOGGING_DIGEST"

                    cosign verify \
                        --key cosign.pub \
                        "$NOTIFICATION_DIGEST"

                    echo "========== All Image Signatures Verified =========="
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

CI + SECURE ARTIFACT PIPELINE COMPLETED.

✔ Environment Verification
✔ Unit Tests Passed
✔ SonarQube Analysis
✔ OWASP Dependency Check
✔ Trivy Filesystem Scan
✔ Docker Images Built
✔ Trivy Image Security Scan
✔ Images Pushed to Docker Hub
✔ Immutable Image Digests Generated
✔ Images Signed with Cosign
✔ Image Signatures Verified
✔ Security Reports Archived

====================================================
'''
        }

        failure {
            echo '''
====================================================

CI PIPELINE FAILED.

Review the failed stage and console output.

Check the specific failed stage in the Jenkins
console output.

Trivy filesystem and image scans are report-only
for HIGH and CRITICAL vulnerabilities.

Registry push and Cosign signing occur only
after the preceding CI/security stages succeed.

====================================================
'''
        }
    }
}
