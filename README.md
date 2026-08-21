# 🔐 Secure DevSecOps Pipeline for Autonomous Microservices Deployment with Continuous Threat Detection

A complete DevSecOps CI/CD pipeline for building, securing, deploying, monitoring, and verifying containerized microservices using Jenkins, Docker, Kubernetes, Helm, and integrated security and monitoring tools.

The project combines CI/CD automation, vulnerability scanning, container security, Kubernetes network security, monitoring, runtime threat detection, alerting, and automated deployment verification into a single workflow.

---

## 📌 Project Overview

Modern applications require security throughout the software development and deployment lifecycle.

This project implements a secure DevSecOps pipeline that automates:

- Source code checkout
- Application testing
- Static code analysis
- Dependency vulnerability scanning
- Filesystem vulnerability scanning
- Docker image building
- Container image vulnerability scanning
- Container image signing and verification
- Kubernetes deployment
- Kubernetes NetworkPolicy configuration
- Application health verification
- Monitoring verification
- Runtime security verification
- Final deployment verification

The project is designed around a microservices architecture and demonstrates how security can be integrated into CI/CD instead of being performed only after deployment.

---

# 🎯 Objectives

- Automate the complete CI/CD workflow.
- Integrate security into the software delivery lifecycle.
- Containerize microservices using Docker.
- Deploy microservices using Kubernetes and Helm.
- Implement least-privilege network communication.
- Detect vulnerabilities in application dependencies.
- Detect vulnerabilities in Docker images.
- Sign and verify container images.
- Perform automated application health checks.
- Monitor the Kubernetes environment.
- Configure alert handling.
- Detect suspicious runtime activity.
- Support automated runtime response.
- Reduce manual deployment and verification work.

---

# 🏗️ Project Architecture

```text
                         ┌──────────────────┐
                         │    Developer     │
                         └────────┬─────────┘
                                  │
                              Git Push
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     GitHub       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Jenkins      │
                         │    CI/CD Engine  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Application     │
                         │     Tests        │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
         SonarQube          OWASP Dependency       Trivy
         Code Analysis          Check              FS Scan
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Docker Build   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Trivy Image     │
                         │      Scan        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Cosign      │
                         │ Sign & Verify    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Kubernetes    │
                         │   + Helm Deploy  │
                         └────────┬─────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
          ▼                       ▼                       ▼
    Gateway Service         User Service            Auth Service
          │                       │
          │                       ├──────────────┐
          │                       │              │
          ▼                       ▼              ▼
 Notification Service      Logging Service    Application
                                            Health Checks

                    ┌──────────────────────────┐
                    │   Monitoring Environment  │
                    └────────────┬─────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
                 ▼               ▼               ▼
            Prometheus        Grafana       Alertmanager

                                 │
                                 ▼
                              Falco
                                 │
                                 ▼
                         Falcosidekick
                                 │
                                 ▼
                           Falco Talon
                                 │
                                 ▼
                       Automated Response


🧩 Microservices

The project contains five containerized microservices.

Service	Port	Purpose
Gateway Service	8000	Entry point and service communication
User Service	8001	User-related operations
Auth Service	8002	Authentication-related operations
Notification Service	8003	Notification handling
Logging Service	8004	Application logging
Service Communication
Gateway Service
 ├── User Service        :8001
 ├── Auth Service        :8002
 ├── Notification Service:8003
 └── Logging Service     :8004


User Service
 ├── Notification Service:8003
 └── Logging Service     :8004

🛠️ Technology Stack

CI/CD
Jenkins
GitHub
Git
Containerization
Docker
Docker Compose
Kubernetes
Kubernetes
Kind
Helm
Kubernetes NetworkPolicies
Security
SonarQube
OWASP Dependency-Check
Trivy
Cosign
Falco
Falcosidekick
Falco Talon
Monitoring
Prometheus
Grafana
Alertmanager
Kubernetes Metrics
Application
Python
FastAPI
Uvicorn
Infrastructure
Terraform
Ubuntu
VirtualBox
🔄 CI/CD Pipeline Workflow

The Jenkins pipeline follows this general workflow:

Git Checkout
     ↓
Environment Validation
     ↓
Application Tests
     ↓
SonarQube Analysis
     ↓
OWASP Dependency Check
     ↓
Trivy Filesystem Scan
     ↓
Docker Image Build
     ↓
Trivy Image Scan
     ↓
Image Signing
     ↓
Image Verification
     ↓
Helm Validation
     ↓
Kubernetes Deployment
     ↓
Application Health Checks
     ↓
Monitoring Verification
     ↓
Runtime Security Verification
     ↓
Final Deployment Verification
     ↓
Pipeline SUCCESS
🔍 Security Implementation

Security is implemented at multiple stages of the pipeline.

1. SonarQube

SonarQube is used for static code analysis and code quality checking.

It helps identify:

Code quality issues
Bugs
Code smells
Security-related issues

The pipeline also performs quality-gate verification.

2. OWASP Dependency-Check

OWASP Dependency-Check scans application dependencies for known vulnerabilities.

The generated dependency-check report is processed and archived by Jenkins.

3. Trivy Filesystem Scan

Trivy scans the project filesystem for vulnerabilities before container deployment.

This provides an early security check before the application is packaged into Docker images.

4. Trivy Container Image Scan

Trivy also scans the generated Docker images.

The pipeline scans for:

HIGH
CRITICAL

severity vulnerabilities.

Reports are generated for each microservice:

security/trivy/image-reports/
├── user-service-report.json
├── auth-service-report.json
├── gateway-service-report.json
├── logging-service-report.json
└── notification-service-report.json

The image scan uses a configured timeout and skips unnecessary Trivy version checks to improve pipeline reliability.

🔐 Container Image Signing

Cosign is used for container image signing and verification.

The workflow is:

Docker Image
     ↓
Trivy Image Scan
     ↓
Cosign Sign
     ↓
Signed Image
     ↓
Cosign Verify

This provides image integrity and establishes trust in the container artifacts used by the deployment process.

🛡️ Kubernetes Network Security

The project implements Kubernetes NetworkPolicies using a default-deny and least-privilege communication model.

Default Deny Ingress

Incoming traffic is denied by default.

Only explicitly allowed communication is permitted.

Default Deny Egress

Outgoing traffic is denied by default.

Only required destinations and ports are allowed.

DNS Access

Application pods are allowed to communicate with Kubernetes CoreDNS using:

UDP 53
TCP 53
Gateway Ingress

Traffic to the Gateway service is allowed on:

TCP 8000
Gateway Egress

The Gateway can communicate with:

User Service         :8001
Auth Service         :8002
Notification Service :8003
Logging Service      :8004
Backend Ingress

Gateway access to User and Auth services is explicitly allowed.

User Service Egress

User Service can communicate with:

Notification Service :8003
Logging Service      :8004
Support Services Ingress

Notification and Logging services accept traffic from the required application services.

CI Health Check Policies

Dedicated NetworkPolicies allow the temporary Jenkins health-check pod to communicate with the five application services.

The overall model is:

Everything Denied
       ↓
Required Communication Allowed
       ↓
Least-Privilege Network Security
☸️ Kubernetes Deployment

The application is deployed inside the Kubernetes namespace:

devsecops

The deployment is managed using Helm.

Kubernetes resources include:

Deployments
Services
ServiceAccounts
NetworkPolicies
Application configurations
Microservice workloads

Check deployed pods:

kubectl get pods -n devsecops

Check services:

kubectl get svc -n devsecops

Check NetworkPolicies:

kubectl get networkpolicy -n devsecops
📦 Helm

Helm is used to manage the Kubernetes deployment.

Project structure:

kubernetes/
└── helm/
    └── devsecops/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/

Validate the Helm chart:

helm lint kubernetes/helm/devsecops

Render the templates:

helm template devsecops kubernetes/helm/devsecops \
    --namespace devsecops

Install or upgrade the deployment:

helm upgrade --install devsecops \
    kubernetes/helm/devsecops \
    --namespace devsecops \
    --create-namespace
❤️ Automated Application Health Checks

After deployment, Jenkins performs automated health checks against all five microservices.

A temporary Kubernetes health-check pod is created for this purpose.

The following services are checked:

User Service
Auth Service
Gateway Service
Notification Service
Logging Service

Example successful output:

===== USER SERVICE =====
{"status":"healthy","service":"user-service"}


===== AUTH SERVICE =====
{"status":"healthy","service":"auth-service"}


===== GATEWAY SERVICE =====
{"status":"healthy","service":"gateway-service"}


===== NOTIFICATION SERVICE =====
{"status":"healthy","service":"notification-service"}


===== LOGGING SERVICE =====
{"status":"healthy","service":"logging-service"}


===== ALL FIVE SERVICES PASSED =====

This ensures that the deployment is not considered healthy simply because Kubernetes reports the pods as Running; the actual application endpoints are also tested.

📊 Monitoring

The project uses Prometheus, Grafana, and Alertmanager for monitoring.

Prometheus

Prometheus collects metrics from the Kubernetes environment.

It provides:

Metrics collection
Time-series data
Monitoring targets
Alert rule evaluation

The monitoring components are deployed separately from the application namespace.

Application workloads are in:

devsecops

Monitoring components are in:

monitoring
📈 Grafana

Grafana is used to visualize Prometheus metrics.

The monitoring flow is:

Kubernetes
     ↓
Prometheus
     ↓
Grafana

Grafana can be used to view:

CPU usage
Memory usage
Pod information
Kubernetes resources
Node metrics
Monitoring information
🚨 Alertmanager

Alertmanager receives and handles alerts generated by Prometheus.

The basic workflow is:

Monitoring Condition
        ↓
    Prometheus
        ↓
      Alert
        ↓
  Alertmanager
        ↓
    Notification

The project also contains custom DevSecOps alert rules.

🐺 Runtime Threat Detection

Trivy provides security scanning before deployment, while Falco provides runtime security monitoring after deployment.

Before Deployment
        ↓
SonarQube
OWASP Dependency Check
Trivy
Cosign
        ↓
Kubernetes Deployment
        ↓
After Deployment
        ↓
Falco Runtime Monitoring

This separates build-time security from runtime security.

🐺 Falco

Falco monitors container and Kubernetes runtime activity.

A custom DevSecOps rule is configured:

DevSecOps Shell Spawned In Container

The rule detects shell execution inside containers running in the devsecops namespace.

The event information includes:

User
User UID
Process
Parent process
Command
Container
Image
Pod
Namespace

This allows suspicious runtime activity to be detected after deployment.

🔄 Falcosidekick

Falcosidekick acts as an event forwarding component for Falco.

The workflow is:

Falco
  ↓
Falcosidekick
  ↓
Alert / Notification System
⚡ Falco Talon

Falco Talon provides the response layer for runtime security events.

The architecture is:

Suspicious Runtime Activity
          ↓
        Falco
          ↓
    Falcosidekick
          ↓
      Falco Talon
          ↓
   Automated Response

This provides the foundation for autonomous runtime threat response.

🧪 Testing and Verification

The project was tested at multiple levels.

Application Testing

Each microservice was tested through its health endpoint.

Security Testing

The pipeline performs:

SonarQube
     ↓
OWASP Dependency Check
     ↓
Trivy Filesystem Scan
     ↓
Trivy Image Scan
     ↓
Cosign Verification
Kubernetes Testing

Pods:

kubectl get pods -n devsecops

Services:

kubectl get svc -n devsecops

NetworkPolicies:

kubectl get networkpolicy -n devsecops

Helm:

helm lint kubernetes/helm/devsecops
Monitoring Testing
kubectl get pods -n monitoring
kubectl get svc -n monitoring
Runtime Security Testing
kubectl get pods -n falco

Falco logs can be reviewed using:

kubectl logs -n falco daemonset/falco -c falco
🚀 Running the Project
Prerequisites

The environment requires:

Git
Docker
Docker Compose
Python
Jenkins
kubectl
Kind
Helm
Terraform
Trivy
SonarQube
Cosign

A working Kubernetes cluster is required.

1. Clone the Repository
git clone git@github.com:aashishmalviya2242006-netizen/secure-devsecops-pipeline.git

Move into the project:

cd secure-devsecops-pipeline
2. Verify Kubernetes

Check cluster information:

kubectl cluster-info

Check nodes:

kubectl get nodes
3. Validate Helm
helm lint kubernetes/helm/devsecops

Render the manifests:

helm template devsecops kubernetes/helm/devsecops \
    --namespace devsecops
4. Deploy the Application
helm upgrade --install devsecops \
    kubernetes/helm/devsecops \
    --namespace devsecops \
    --create-namespace

Verify:

kubectl get pods -n devsecops
5. Check Application Services
kubectl get svc -n devsecops
🌐 Access Application Services

The application services use Kubernetes ClusterIP services.

For local browser access, use Kubernetes port-forwarding.

Gateway Service
kubectl port-forward -n devsecops svc/gateway-service 8000:8000

Open:

http://localhost:8000
User Service
kubectl port-forward -n devsecops svc/user-service 8001:8001

Open:

http://localhost:8001/health
Auth Service
kubectl port-forward -n devsecops svc/auth-service 8002:8002

Open:

http://localhost:8002/health
Notification Service
kubectl port-forward -n devsecops svc/notification-service 8003:8003

Open:

http://localhost:8003/health
Logging Service
kubectl port-forward -n devsecops svc/logging-service 8004:8004

Open:

http://localhost:8004/health
📈 Access Prometheus

Check the monitoring services:

kubectl get svc -n monitoring

Port-forward Prometheus:

kubectl port-forward -n monitoring \
    svc/monitoring-kube-prometheus-prometheus 9090:9090

Open:

http://localhost:9090
📊 Access Grafana

Check Grafana:

kubectl get svc -n monitoring

Port-forward Grafana:

kubectl port-forward -n monitoring \
    svc/monitoring-grafana 3000:80

Open:

http://localhost:3000
🚨 Access Alertmanager

Port-forward Alertmanager:

kubectl port-forward -n monitoring \
    svc/monitoring-kube-prometheus-alertmanager 9093:9093

Open:

http://localhost:9093
🐺 Check Falco

Check Falco pods:

kubectl get pods -n falco

Check Falco logs:

kubectl logs -n falco daemonset/falco -c falco
📁 Project Structure
secure-devsecops-pipeline/
│
├── docker/
│   ├── auth-service/
│   ├── gateway-service/
│   ├── logging-service/
│   ├── notification-service/
│   └── user-service/
│
├── docs/
│   ├── architecture.md
│   ├── learning-notes.md
│   ├── project-overview.md
│   └── roadmap.md
│
├── jenkins/
│
├── kubernetes/
│   ├── base/
│   ├── helm/
│   │   └── devsecops/
│   └── manifests/
│
├── monitoring/
│   ├── grafana/
│   ├── prometheus/
│   └── falco/
│
├── scripts/
│
├── security/
│   ├── cosign/
│   ├── dependency-check/
│   ├── falco/
│   ├── sonarqube/
│   └── trivy/
│
├── services/
│   ├── auth-service/
│   ├── gateway-service/
│   ├── logging-service/
│   ├── notification-service/
│   └── user-service/
│
├── terraform/
│
├── tests/
│
├── Jenkinsfile
│
└── README.md
🔁 Complete Pipeline and Runtime Flow
                         ┌───────────────┐
                         ┌───────────────┐
                         │  Trivy FS     │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Docker Build  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Trivy Image   │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Cosign Sign   │
                         │ & Verify      │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Kubernetes    │
                         │ + Helm        │
                         └───────┬───────┘
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
                  ▼              ▼              ▼
              Gateway          User           Auth
                  │              │
                  └──────┬───────┘
                         │
                  ┌──────┴───────┐
                  ▼              ▼
             Notification      Logging
                  │
                  ▼
            Health Checks
                  │
                  ▼
             Deployment
               Verified
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
   Monitoring          Runtime Security
        │                   │
   ┌────┴────┐              ▼
   │         │            Falco
   ▼         ▼              │
Prometheus Grafana          ▼
   │                    Falcosidekick
   ▼                         │
Alertmanager                ▼
                         Falco Talon
                             │
                             ▼
                    Automated Response
🔐 Security Layers
┌──────────────────────────────────────────┐
│             Source Code Security         │
│               SonarQube                  │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│          Dependency Security             │
│          OWASP Dependency Check          │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│          Filesystem Security             │
│                Trivy                     │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│          Container Security              │
│             Trivy Image                  │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│          Image Integrity                 │
│        Cosign Sign & Verify              │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│        Kubernetes Network Security       │
│          NetworkPolicies                 │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│          Runtime Security                │
│              Falco                      │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│       Runtime Response                   │
│          Falco Talon                     │
└──────────────────────────────────────────┘
⚙️ Pipeline Reliability

During development, delays were observed during resource-intensive pipeline operations such as:

Docker image building
SonarQube analysis
Trivy image scanning

The Ubuntu environment initially had approximately 9 GB RAM available to the VM and no swap space.

System resources were checked using:

free -h

A 4 GB swap file was configured:

sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

The swap configuration was verified using:

swapon --show

After increasing the available virtual memory resources, the complete Jenkins pipeline executed successfully.

🧠 Key Learnings

The project provided practical experience with:

CI/CD pipeline automation
Jenkins pipeline development
Docker containerization
Kubernetes deployment
Helm
Kubernetes NetworkPolicies
Static code analysis
Dependency vulnerability scanning
Container vulnerability scanning
Container image signing
Runtime threat detection
Prometheus monitoring
Grafana visualization
Alertmanager
Kubernetes health checks
DevSecOps security integration
Linux resource management
CI/CD troubleshooting
⚠️ Challenges Faced and Solutions
Jenkins Pipeline Delays

Docker builds and security scanning stages occasionally took longer than expected.

Solution

Improved the Ubuntu VM resources by configuring a 4 GB swap file.

Kubernetes NetworkPolicy Restrictions

The CI health-check pod initially could not connect to the application services because of the default-deny NetworkPolicies.

Solution

Created dedicated ingress and egress NetworkPolicies for the CI health-check pod.

Trivy Scanning Delays

Trivy vulnerability database updates and image scans sometimes required significant time.

Solution

Configured Trivy with:

--timeout 15m
--skip-version-check
Kubernetes Service Browser Access

Application services use ClusterIP, so they are not directly exposed outside the cluster.

Solution

Used Kubernetes port-forwarding for local browser access.

For production environments, Kubernetes Ingress or a LoadBalancer can be introduced.

🚀 Future Improvements

The core project has been completed. Possible future improvements include:

Kubernetes Ingress for permanent external access.
TLS/HTTPS using cert-manager.
Application-specific Prometheus metrics.
Dedicated Grafana dashboards for individual microservices.
Centralized logging using ELK or OpenSearch.
Image admission policies using Cosign verification.
Automated vulnerability remediation.
Kubernetes Horizontal Pod Autoscaling.
Deployment to AWS EKS.
GitHub webhook-based pipeline triggering.
More advanced automated runtime response policies.
📌 Project Status
Component	Status
CI/CD Pipeline	✅ Completed
Docker Containerization	✅ Completed
Kubernetes Deployment	✅ Completed
Helm Deployment	✅ Completed
SonarQube	✅ Integrated
OWASP Dependency Check	✅ Integrated
Trivy Filesystem Scan	✅ Integrated
Trivy Image Scan	✅ Integrated
Cosign Image Signing	✅ Integrated
Cosign Verification	✅ Integrated
Kubernetes NetworkPolicies	✅ Implemented
Application Health Checks	✅ Implemented
Prometheus	✅ Deployed
Grafana	✅ Deployed
Alertmanager	✅ Deployed
Falco	✅ Deployed
Falcosidekick	✅ Deployed
Falco Talon	✅ Deployed
Runtime Threat Detection	✅ Implemented
Final Pipeline Verification	✅ Completed
🏁 Conclusion

This project demonstrates how DevSecOps practices can be integrated into a complete software delivery workflow.

The implemented pipeline performs application testing, static code analysis, dependency scanning, filesystem scanning, container vulnerability scanning, image signing and verification, Kubernetes deployment, NetworkPolicy enforcement, and post-deployment application health verification.

The deployed environment is supported by Prometheus and Grafana for monitoring, Alertmanager for alert handling, and Falco for runtime threat detection.

The project demonstrates the complete security lifecycle:

Build Securely
      ↓
Scan Continuously
      ↓
Sign and Verify
      ↓
Deploy Automatically
      ↓
Verify Application Health
      ↓
Monitor Continuously
      ↓
Detect Runtime Threats
      ↓
Respond Automatically
📚 References
Kubernetes Documentation
https://kubernetes.io/docs/
Kubernetes NetworkPolicies
https://kubernetes.io/docs/concepts/services-networking/network-policies/
Jenkins Documentation
https://www.jenkins.io/doc/
Docker Documentation
https://docs.docker.com/
Helm Documentation
https://helm.sh/docs/
Trivy Documentation
https://trivy.dev/latest/
SonarQube Documentation
https://docs.sonarsource.com/sonarqube/
OWASP Dependency-Check
https://owasp.org/www-project-dependency-check/
Cosign Documentation
https://docs.sigstore.dev/cosign/
Falco Documentation
https://falco.org/docs/
Prometheus Documentation
https://prometheus.io/docs/
Grafana Documentation
https://grafana.com/docs/
Alertmanager Documentation
https://prometheus.io/docs/alerting/latest/alertmanager/
👨‍💻 Project

Secure DevSecOps Pipeline for Autonomous Microservices Deployment with Continuous Threat Detection

Domain: DevSecOps / Cloud / Kubernetes / CI-CD / Cybersecurity

Primary Platform: Ubuntu + Kubernetes + Jenkins

Status: ✅ Completed
