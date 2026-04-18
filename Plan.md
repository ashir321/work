```mermaid
graph TD

A[Developer Commit] --> B[GitHub]
B --> C[Jenkins CI Pipeline]

C --> D[Build Docker Image]
D --> E[SBOM Generation - Syft]
E --> F[CVE Scan - Grype/Trivy]

F -->|Vulnerable| G[AI Analysis Engine]
G --> H[Auto Fix Recommendation]
H --> C

F -->|Secure| I[Push to Registry]

I --> J[Deploy via GitOps]
J --> K[Kubernetes Cluster - EKS]

K --> L[Karpenter Autoscaling]
L --> M[Dynamic Node Provisioning]

K --> N[Monitoring - Prometheus]
N --> O[Grafana Dashboards]

K --> P[Runtime Security Policies]
