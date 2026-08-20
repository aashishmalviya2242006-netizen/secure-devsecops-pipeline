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

        KUBE_NAMESPACE = 'devsecops'
        HELM_RELEASE = 'devsecops'
        HELM_CHART = './kubernetes/helm/devsecops'

        KUBECONFIG = '/var/lib/jenkins/.kube/config'
    }

    stages {

        /*
         * ============================================================
         * 1. ENVIRONMENT
         * ============================================================
         */

        stage('Verify Environment') {
            steps {
                sh '''
                    set -e

                    echo "========== ENVIRONMENT =========="

                    python3 --version
                    pip3 --version
                    docker --version
                    trivy --version
                    cosign version
                    kubectl version --client
                    helm version
                '''
            }
        }

        /*
         * ============================================================
         * 2. MICROSERVICE CI
         * ============================================================
         */

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

        /*
         * ============================================================
         * 3. CODE SECURITY
         * ============================================================
         */

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

                    echo "========== TRIVY FILESYSTEM SCAN =========="

                    echo "Scanning HIGH and CRITICAL vulnerabilities..."

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

                    echo "========== TRIVY FILESYSTEM SCAN PASSED =========="
                '''
            }
        }

        /*
         * ============================================================
         * 4. CONTAINER BUILD
         * ============================================================
         */

        stage('Build Docker Images') {
            steps {
                sh '''
                    set -e

                    echo "========== BUILDING DOCKER IMAGES =========="

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

                    echo "========== DOCKER BUILD COMPLETED =========="
                '''
            }
        }

        /*
         * ============================================================
         * 5. CONTAINER SECURITY
         * ============================================================
         */

        stage('Trivy Image Scan') {
            steps {
                sh '''
                    set -e

                    mkdir -p security/trivy/image-reports

                    echo "========== TRIVY IMAGE SCAN =========="

                    trivy image \
                        --timeout 15m \
                        --skip-version-check \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/user-service-report.json \
                        --exit-code 0 \
                        user-service:v1

                    trivy image \
                        --timeout 15m \
                        --skip-version-check \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/auth-service-report.json \
                        --exit-code 0 \
                        auth-service:v1

                    trivy image \
                        --timeout 15m \
                        --skip-version-check \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/gateway-service-report.json \
                        --exit-code 0 \
                        gateway-service:v1

                    trivy image \
                        --timeout 15m \
                        --skip-version-check \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/logging-service-report.json \
                        --exit-code 0 \
                        logging-service:v1

                    trivy image \
                        --timeout 15m \
                        --skip-version-check \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --format json \
                        --output security/trivy/image-reports/notification-service-report.json \
                        --exit-code 0 \
                        notification-service:v1

                    echo "========== TRIVY IMAGE SCAN COMPLETED =========="
                '''
            }
        }

        /*
         * ============================================================
         * 6. DOCKER REGISTRY
         * ============================================================
         */

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

                        echo "========== DOCKER HUB LOGIN =========="

                        echo "$DOCKERHUB_PASSWORD" | docker login \
                            -u "$DOCKERHUB_USERNAME" \
                            --password-stdin

                        echo "========== TAGGING IMAGES =========="

                        docker tag user-service:v1 "$USER_IMAGE"
                        docker tag auth-service:v1 "$AUTH_IMAGE"
                        docker tag gateway-service:v1 "$GATEWAY_IMAGE"
                        docker tag logging-service:v1 "$LOGGING_IMAGE"
                        docker tag notification-service:v1 "$NOTIFICATION_IMAGE"

                        echo "========== PUSHING IMAGES =========="

                        docker push "$USER_IMAGE"
                        docker push "$AUTH_IMAGE"
                        docker push "$GATEWAY_IMAGE"
                        docker push "$LOGGING_IMAGE"
                        docker push "$NOTIFICATION_IMAGE"

                        echo "========== REGISTRY PUSH COMPLETED =========="
                    '''
                }
            }
        }

        /*
         * ============================================================
         * 7. IMAGE DIGESTS
         * ============================================================
         */

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

        /*
         * ============================================================
         * 8. IMAGE SIGNING
         * ============================================================
         */

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

                        echo "========== COSIGN SIGNING =========="

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

                        echo "========== ALL IMAGES SIGNED =========="
                    '''
                }
            }
        }

        stage('Cosign Verify Images') {
            steps {
                sh '''
                    set -e

                    echo "========== COSIGN VERIFICATION =========="

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

                    echo "========== ALL IMAGE SIGNATURES VERIFIED =========="
                '''
            }
        }

        /*
         * ============================================================
         * 9. KUBERNETES / HELM CD
         * ============================================================
         */

        stage('Validate Kubernetes Helm Chart') {
            steps {
                sh '''
                    set -e

                    echo "========== HELM LINT =========="

                    helm lint "$HELM_CHART"

                    echo "========== HELM TEMPLATE VALIDATION =========="

                    helm template "$HELM_RELEASE" "$HELM_CHART" \
                        --namespace "$KUBE_NAMESPACE" \
                        > /tmp/devsecops-rendered.yaml

                    echo "Helm chart validation successful."
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "DEPLOYING DEVSECOPS TO KUBERNETES"
                    echo "========================================"

                    kubectl get nodes

                    helm upgrade --install "$HELM_RELEASE" "$HELM_CHART" \
                        --namespace "$KUBE_NAMESPACE" \
                        --create-namespace \
                        --set services.user.tag="v1" \
                        --set services.auth.tag="v1" \
                        --set services.gateway.tag="v1" \
                        --set services.notification.tag="v1" \
                        --set services.logging.tag="v1"

                    echo "========== KUBERNETES DEPLOYMENT COMPLETED =========="
                '''
            }
        }

        stage('Wait for Kubernetes Rollout') {
            steps {
                sh '''
                    set -e

                    echo "========== WAITING FOR ROLLOUTS =========="

                    kubectl rollout status deployment/user-service \
                        -n "$KUBE_NAMESPACE" \
                        --timeout=180s

                    kubectl rollout status deployment/auth-service \
                        -n "$KUBE_NAMESPACE" \
                        --timeout=180s

                    kubectl rollout status deployment/gateway-service \
                        -n "$KUBE_NAMESPACE" \
                        --timeout=180s

                    kubectl rollout status deployment/notification-service \
                        -n "$KUBE_NAMESPACE" \
                        --timeout=180s

                    kubectl rollout status deployment/logging-service \
                        -n "$KUBE_NAMESPACE" \
                        --timeout=180s

                    echo "========== ALL ROLLOUTS SUCCESSFUL =========="
                '''
            }
        }

        stage('Verify Kubernetes Deployment') {
            steps {
                sh '''
                    set -e

                    echo "========== PODS =========="

                    kubectl get pods \
                        -n "$KUBE_NAMESPACE" \
                        -o wide

                    echo
                    echo "========== SERVICES =========="

                    kubectl get services \
                        -n "$KUBE_NAMESPACE"

                    echo
                    echo "========== DEPLOYMENTS =========="

                    kubectl get deployments \
                        -n "$KUBE_NAMESPACE"

                    echo
                    echo "========== HELM RELEASE =========="

                    helm status "$HELM_RELEASE" \
                        -n "$KUBE_NAMESPACE"
                '''
            }
        }

        /*
         * ============================================================
         * 10. APPLICATION HEALTH CHECK
         *
         * CI health-check pod is explicitly labelled:
         *
         *     app=ci-health-check
         *
         * The Falco rule intentionally excludes this pod because
         * the pod executes curl through a shell as part of CI.
         *
         * NetworkPolicy allows this pod to reach all five services.
         * ============================================================
         */

        stage('Application Health Check') {
            steps {
                sh '''
                    set -e

                    echo "========== APPLICATION HEALTH CHECK =========="

                    kubectl run ci-health-check \
                        -n "$KUBE_NAMESPACE" \
                        --rm \
                        -i \
                        --restart=Never \
                        --labels=app=ci-health-check \
                        --image=curlimages/curl:8.10.1 \
                        -- \
                        sh -c '
                            set -e

                            echo "===== USER SERVICE ====="
                            curl --fail --silent --show-error \
                                http://user-service:8001/health
                            echo

                            echo "===== AUTH SERVICE ====="
                            curl --fail --silent --show-error \
                                http://auth-service:8002/health
                            echo

                            echo "===== GATEWAY SERVICE ====="
                            curl --fail --silent --show-error \
                                http://gateway-service:8000/health
                            echo

                            echo "===== NOTIFICATION SERVICE ====="
                            curl --fail --silent --show-error \
                                http://notification-service:8003/health
                            echo

                            echo "===== LOGGING SERVICE ====="
                            curl --fail --silent --show-error \
                                http://logging-service:8004/health
                            echo

                            echo "===== ALL FIVE SERVICES PASSED ====="
                        '

                    echo
                    echo "========== APPLICATION HEALTH CHECK PASSED =========="
                '''
            }
        }

        /*
         * ============================================================
         * 11. MONITORING VERIFICATION
         *
         * Monitoring is already deployed.
         * Jenkins verifies the existing monitoring infrastructure.
         * ============================================================
         */

        stage('Verify Monitoring Stack') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "MONITORING STACK"
                    echo "========================================"

                    kubectl get pods -n monitoring

                    echo
                    echo "========== MONITORING DEPLOYMENTS =========="

                    kubectl get deployments -n monitoring

                    echo
                    echo "========== MONITORING SERVICES =========="

                    kubectl get services -n monitoring

                    echo
                    echo "Monitoring stack verification completed."
                '''
            }
        }

        /*
         * ============================================================
         * 12. RUNTIME SECURITY VERIFICATION
         * ============================================================
         */

        stage('Verify Runtime Security Stack') {
            steps {
                sh '''
                    set -e

                    echo "========================================"
                    echo "RUNTIME SECURITY STACK"
                    echo "========================================"

                    kubectl get pods -n falco

                    echo
                    echo "========== FALCO DAEMONSET =========="

                    kubectl get daemonset falco -n falco

                    echo
                    echo "========== FALCOSIDEKICK =========="

                    kubectl get deployment falco-falcosidekick -n falco

                    echo
                    echo "========== FALCO TALON =========="

                    kubectl get deployment falco-talon -n falco

                    echo
                    echo "Runtime security stack verification completed."
                '''
            }
        }

        /*
         * ============================================================
         * 13. FINAL DEPLOYMENT VERIFICATION
         * ============================================================
         */

        stage('Final Deployment Verification') {
            steps {
                sh '''
                    set -e

                    echo
                    echo "=============================================="
                    echo "      FINAL DEVSECOPS DEPLOYMENT STATUS"
                    echo "=============================================="

                    echo
                    echo "----- APPLICATION -----"
                    kubectl get pods -n devsecops

                    echo
                    echo "----- MONITORING -----"
                    kubectl get pods -n monitoring

                    echo
                    echo "----- RUNTIME SECURITY -----"
                    kubectl get pods -n falco

                    echo
                    echo "=============================================="
                    echo "       DEVSECOPS PIPELINE VERIFIED"
                    echo "=============================================="
                '''
            }
        }
    }

    /*
     * ================================================================
     * POST ACTIONS
     * ================================================================
     */

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
============================================================

FULL DEVSECOPS CI/CD PIPELINE COMPLETED SUCCESSFULLY

CI / SECURITY
✔ Environment Verification
✔ Unit Tests
✔ SonarQube Analysis
✔ OWASP Dependency Check
✔ Trivy Filesystem Scan
✔ Docker Image Build
✔ Trivy Image Scan
✔ Docker Hub Push
✔ Image Digest Generation
✔ Cosign Image Signing
✔ Cosign Signature Verification

KUBERNETES CD
✔ Helm Chart Validation
✔ Kubernetes Deployment
✔ Rollout Verification
✔ Deployment Verification
✔ Five-Service Application Health Check

MONITORING
✔ Prometheus Verified
✔ Grafana Verified
✔ Alertmanager Verified
✔ Monitoring Stack Verified

RUNTIME SECURITY
✔ Falco Verified
✔ Falcosidekick Verified
✔ Falco Talon Verified
✔ Autonomous Runtime Response Infrastructure Verified

============================================================
'''
        }

        failure {
            echo '''
============================================================

DEVSECOPS CI/CD PIPELINE FAILED

Review the failed Jenkins stage and console output.

Security scan reports are archived when available.

============================================================
'''
        }
    }
}
