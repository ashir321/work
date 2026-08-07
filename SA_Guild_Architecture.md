# Platform Delivery Architecture
## Shipping with Helm & ArgoCD — Dev → QA

> Derived from **SA_Guils_proposal.pptx**  
> Scope: Development through QA · Staging and Production to follow

![Platform Delivery Architecture](docs/architecture/SA_Guild_Architecture_Diagram.png)

---

## 1. System Context — Delivery Contract

The platform separates **application code** from **environment/configuration**. Each path has one owner, one trigger, and one convergence point: the **Kubernetes Deployment** in the Dev namespace.

```mermaid
flowchart TB
    subgraph PEOPLE["👥 Application Squad"]
        DEV["Developer"]
        DEVOPS["DevOps / Platform Engineer"]
    end

    subgraph CODE_DOMAIN["CODE DOMAIN — Jenkins owns rollout"]
        direction TB
        APP_REPO["Application Source Repo"]
        JENKINS["Jenkins CI"]
        ECR["Amazon ECR"]
    end

    subgraph CONFIG_DOMAIN["CONFIG DOMAIN — ArgoCD owns sync"]
        direction TB
        GITLAB["GitLab — Helm Chart Repo<br/><i>my-app-deploy</i><br/>appVersion editable"]
        ARGO["ArgoCD"]
        HELM["Helm Render Engine"]
    end

    subgraph RUNTIME["RUNTIME — Single convergence point"]
        K8S["Kubernetes Cluster"]
        NS["Dev Namespace"]
        DEPLOY["Deployment<br/><code>&lt;image-tag&gt;</code> · pullPolicy: Always"]
        PODS["Running Pods"]
    end

    DEV -->|"① Push code<br/>② Trigger build"| APP_REPO
    APP_REPO --> JENKINS
    JENKINS -->|"Build image<br/>Push tags"| ECR
    JENKINS -->|"Restart Deployment<br/>(no Git change)"| DEPLOY

    DEV -->|"Edit chart / values<br/>appVersion · image tag"| GITLAB
    DEVOPS -->|"Edit chart / values<br/>Reviewed diff"| GITLAB
    GITLAB -->|"Watch repo<br/>targetRevision: develop"| ARGO
    ARGO --> HELM
    HELM -->|"Template + Apply<br/>prune: true · selfHeal: false"| DEPLOY

    ECR -.->|"Stable tag reference"| DEPLOY
    DEPLOY --> PODS
    K8S --> NS
    NS --> DEPLOY

    classDef code fill:#eff6ff,stroke:#2563eb,color:#1e3a8a
    classDef config fill:#f5f3ff,stroke:#7c3aed,color:#4c1d95
    classDef runtime fill:#f0fdf4,stroke:#16a34a,color:#14532d
    classDef people fill:#f8fafc,stroke:#64748b,color:#0f172a

    class DEV,DEVOPS people
    class APP_REPO,JENKINS,ECR code
    class GITLAB,ARGO,HELM config
    class K8S,NS,DEPLOY,PODS runtime
```

---

## 2. Dual-Path Architecture — Code vs Config

```mermaid
flowchart LR
    subgraph CODE_PATH["🔵 CODE PATH"]
        direction TB
        C1["Push & Build"]
        C2["ECR: stable tag +<br/>backup tag (_commit)"]
        C3["Jenkins restarts<br/>Deployment"]
        C4["Pods pull fresh image<br/>imagePullPolicy: Always"]
        C5["ArgoCD stays Synced<br/>(no Git diff)"]
        C1 --> C2 --> C3 --> C4 --> C5
    end

    subgraph CONFIG_PATH["🟣 CONFIG PATH"]
        direction TB
        G1["Developer / DevOps<br/>edit chart · appVersion · values"]
        G2["GitLab review + diff"]
        G3["ArgoCD detects drift"]
        G4["Helm render<br/>values-dev.yaml merge"]
        G5["Apply → Synced + Healthy"]
        G1 --> G2 --> G3 --> G4 --> G5
    end

    CONVERGE(("Kubernetes<br/>Deployment"))

    C5 --> CONVERGE
    G5 --> CONVERGE

    classDef code fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef config fill:#ede9fe,stroke:#7c3aed,color:#4c1d95
    classDef hub fill:#dcfce7,stroke:#16a34a,color:#14532d

    class C1,C2,C3,C4,C5 code
    class G1,G2,G3,G4,G5 config
    class CONVERGE hub
```

### Boundary Rule
> **Jenkins** owns fresh image rollout. **ArgoCD** owns Git-declared configuration.  
> `selfHeal: false` prevents the two systems from fighting over the same Deployment.

---

## 3. Component Ownership Model

```mermaid
block-beta
    columns 4

    block:JENKINS:2
        columns 1
        J_TITLE["Jenkins"]
        J1["Build image"]
        J2["Push ECR tags"]
        J3["Restart deployment"]
    end

    block:ECR:2
        columns 1
        E_TITLE["ECR"]
        E1["Stable deployed tag"]
        E2["Backup: tag_commitID"]
    end

    block:GITLAB:2
        columns 1
        G_TITLE["GitLab"]
        G1["Hold Helm chart"]
        G2["Review config diffs"]
        G3["Source of truth"]
    end

    block:ARGOCD:2
        columns 1
        A_TITLE["ArgoCD"]
        A1["Watch GitLab"]
        A2["Render + apply"]
        A3["Report health"]
    end

    block:DEPLOY:4
        columns 1
        D_TITLE["Kubernetes Deployment — Convergence Point"]
        D1["References stable image tag"]
        D2["imagePullPolicy: Always"]
        D3["Runtime result of both paths"]
    end

    JENKINS --> DEPLOY
    ECR --> DEPLOY
    GITLAB --> ARGOCD
    ARGOCD --> DEPLOY
```

| Component | Responsibility | Does NOT do |
|-----------|---------------|-------------|
| **Jenkins** | Build, tag, push image, restart pods | Edit Git / Helm values |
| **ECR** | Store immutable image artefacts | Deploy or configure cluster |
| **GitLab** | Version Helm charts & values | Build application images |
| **ArgoCD** | Sync declared config to cluster | Rebuild images or restart for code |
| **Deployment** | Run workloads at declared state | Act as independent automation |

---

## 4. End-to-End Sequence — Develop to Deployment

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Developer
    participant App as App Repo
    participant Jenkins as Jenkins
    participant ECR as ECR
    participant DevOps as DevOps
    participant GitLab as GitLab (Chart)
    participant Argo as ArgoCD
    participant K8s as K8s Deployment

  rect rgb(219, 234, 254)
    Note over Dev,K8s: CODE PATH — image rollout without Git change
    Dev->>App: Push application source
    Dev->>Jenkins: Trigger CI build
    Jenkins->>Jenkins: Build Docker image
    Jenkins->>ECR: Push stable tag + backup tag
    Jenkins->>K8s: Rollout restart Deployment
    K8s->>ECR: Pull image (Always)
    Note over Argo: ArgoCD unchanged — manifest byte-identical
  end

  rect rgb(237, 233, 254)
    Note over Dev,K8s: CONFIG PATH — GitOps config sync
    Dev->>GitLab: Edit chart / values / ConfigMap
    DevOps->>GitLab: Edit chart / values / ConfigMap
    GitLab->>GitLab: MR review + approved diff
    Argo->>GitLab: Detect commit drift
    Argo->>Argo: Helm template (values-dev.yaml)
    Argo->>K8s: Apply rendered manifests
    K8s-->>Argo: Synced + Healthy
  end
```

---

## 5. GitLab Chart Layout (Dev/QA Standard)

```mermaid
flowchart TD
    ROOT["my-app-deploy/"]

    ROOT --> CHART["Chart.yaml<br/>version · appVersion<br/><i>editable in Dev/QA</i>"]
    ROOT --> VALUES["values.yaml"]
    ROOT --> VALUES_DEV["values-dev.yaml<br/><i>Dev overlay</i>"]
    ROOT --> FILES["files/"]
    ROOT --> TEMPLATES["templates/"]

    FILES --> PROPS["app.properties"]
    TEMPLATES --> DEPLOY_YAML["deployment.yaml"]
    TEMPLATES --> SVC["service.yaml"]
    TEMPLATES --> CM["app-properties-configmap.yaml"]

  ARGO["ArgoCD Application"] -->|"repoURL + path: .<br/>valueFiles: values-dev.yaml"| ROOT

    classDef folder fill:#eef2ff,stroke:#4f46e5,color:#1e1b4b
    classDef file fill:#f8fafc,stroke:#64748b,color:#0f172a
    classDef watcher fill:#e0e7ff,stroke:#4f46e5,color:#1e1b4b

    class ROOT folder
    class CHART,VALUES,VALUES_DEV,PROPS,DEPLOY_YAML,SVC,CM file
    class ARGO watcher
```

### Editable App Version (Dev/QA)

During Dev and QA, the Helm chart stays as **raw, editable source files** in GitLab — not a packaged `.tgz`. ArgoCD watches `repoURL + path` and renders the chart directly, so version fields can be changed in place and reviewed through a normal Git diff.

| Field | Where | Editable in Dev/QA? | Purpose |
|-------|-------|---------------------|---------|
| `appVersion` | `Chart.yaml` | **Yes** | Declares the application release label (metadata + labels) |
| `version` | `Chart.yaml` | **Yes** | Chart packaging version while iterating in Git |
| `image.tag` | `values-dev.yaml` | **Yes** | Pin or override the container image tag for the environment |
| Packaged chart | OCI registry | **No** (post-QA) | Immutable artefact promoted unchanged after QA |

**Example — editable fields in Dev/QA**

```yaml
# Chart.yaml — appVersion is editable; bump here for config-path releases
apiVersion: v2
name: my-app
description: SA Guild sample deploy chart
type: application
version: 0.3.0        # chart version — editable during iteration
appVersion: "2.4.1"   # app version — editable in Dev/QA raw chart
```

```yaml
# values-dev.yaml — image tag override (config path)
image:
  repository: 123456789012.dkr.ecr.eu-west-1.amazonaws.com/my-app
  tag: "2.4.1"        # editable — ArgoCD sync applies on merge
```

**Boundary:** The **code path** refreshes running pods via Jenkins rollout restart without a Git change. The **config path** owns `appVersion`, chart `version`, and values overlays — including image tag when declared in Git.

### ArgoCD Application Contract (Minimum Wiring)

```yaml
source:
  repoURL: https://gitlab.com/org/my-app-deploy.git
  targetRevision: develop
  path: .
  helm:
    valueFiles:
      - values-dev.yaml
destination:
  server: https://kubernetes.default.svc
  namespace: dev
syncPolicy:
  automated:
    prune: true      # removed Git resources deleted from cluster
    selfHeal: false  # do not undo Jenkins rollout restarts
```

---

## 6. Release & QA Promotion Architecture

```mermaid
flowchart LR
    subgraph DEV_QA["DEV / QA — Flexible iteration"]
        RAW["Raw Helm chart<br/>appVersion editable"]
        ARGO_DEV["ArgoCD watches<br/>editable source"]
        QA["QA validation"]
        RAW --> ARGO_DEV --> QA
    end

    subgraph RELEASE["RELEASE — Immutable artefact"]
        PKG["helm package<br/>→ .tgz"]
        OCI["OCI Registry<br/>helm push"]
        PROMOTE["Promote unchanged<br/>artefact"]
        PKG --> OCI --> PROMOTE
    end

    QA -->|"Artefact passes QA"| PKG

    ROLLBACK["Rollback = version<br/>pointer change"]

    PROMOTE -.-> ROLLBACK

    classDef dev fill:#eff6ff,stroke:#0284c7,color:#0c4a6e
    classDef rel fill:#fffbeb,stroke:#d97706,color:#78350f

    class RAW,ARGO_DEV,QA dev
    class PKG,OCI,PROMOTE,ROLLBACK rel
```

**Release command pattern**
1. Bump `Chart.yaml` version
2. `helm package ./my-app-deploy`
3. `helm push my-app-1.0.0.tgz oci://registry/charts`

**Promotion principle:** The artefact that passes QA is the artefact promoted to Release — unchanged.

---

## 7. Layered Platform View

```mermaid
flowchart TB
    subgraph L1["LAYER 1 — Experience"]
        SQUAD["Application Squad"]
    end

    subgraph L2["LAYER 2 — Delivery Pipelines"]
        direction LR
        CI["Jenkins CI/CD<br/><i>Code path</i>"]
        GITOPS["ArgoCD GitOps<br/><i>Config path</i>"]
    end

    subgraph L3["LAYER 3 — Artefact Stores"]
        direction LR
        REG_IMG["ECR — Container Images"]
        REG_CHART["GitLab — Raw Charts"]
        REG_OCI["OCI — Packaged Charts<br/><i>Post-QA</i>"]
    end

    subgraph L4["LAYER 4 — Orchestration"]
        HELM_L["Helm Templating"]
        K8S_L["Kubernetes API"]
    end

    subgraph L5["LAYER 5 — Runtime"]
        WORKLOAD["Deployments · Services · ConfigMaps"]
    end

    SQUAD -->|"Push code"| CI
    SQUAD -->|"Edit chart / values"| GITOPS

    CI --> REG_IMG
    GITOPS --> REG_CHART
    REG_CHART --> HELM_L
    REG_IMG --> K8S_L
    HELM_L --> K8S_L
    REG_OCI -.->|"Release only"| HELM_L
    K8S_L --> WORKLOAD

    classDef l1 fill:#f8fafc,stroke:#64748b,color:#0f172a
    classDef l2 fill:#eff6ff,stroke:#2563eb,color:#1e3a8a
    classDef l3 fill:#fffbeb,stroke:#d97706,color:#78350f
    classDef l4 fill:#f5f3ff,stroke:#7c3aed,color:#4c1d95
    classDef l5 fill:#f0fdf4,stroke:#16a34a,color:#14532d

    class SQUAD l1
    class CI,GITOPS l2
    class REG_IMG,REG_CHART,REG_OCI l3
    class HELM_L,K8S_L l4
    class WORKLOAD l5
```

---

## 8. Design Principles Summary

| Principle | Implementation |
|-----------|----------------|
| **Separation of concerns** | Code → Jenkins · Config → ArgoCD |
| **Single source of truth** | GitLab for config · ECR for images |
| **No automation collision** | `selfHeal: false` on ArgoCD Application |
| **Traceable releases** | Versioned charts · commit backup tags |
| **Safe rollback** | Revert chart version pointer (config) or previous image tag (code) |
| **Dev/QA flexibility** | Raw editable charts — `appVersion` and values in GitLab |
| **Release immutability** | Package to `.tgz` → push to OCI only after QA pass |

---

## 9. Adoption Readiness Checklist

```mermaid
flowchart LR
    C1["1. Confirm scope<br/>Dev → QA"]
    C2["2. Standardize chart<br/>layout"]
    C3["3. Lock ownership<br/>Jenkins / ArgoCD"]
    C4["4. Set sync policy<br/>prune · no selfHeal"]
    C5["5. Protect secrets<br/>K8s Secret refs"]
    C6["6. Define release<br/>package post-QA"]

    C1 --> C2 --> C3 --> C4 --> C5 --> C6

    OUT["Repeatable platform pattern<br/>for all squads"]

    C6 --> OUT
```

---

*One split. One source of truth. Code changes via Jenkins. Config changes via GitLab + ArgoCD. Kubernetes Dev is the running result.*
