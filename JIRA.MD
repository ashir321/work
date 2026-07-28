# Secure Cloud-Native Delivery Platform — Jira Backlog

## Source

This backlog is derived from the architecture flow in `Plan.md`: developer commits move through GitHub and Jenkins, image build, SBOM and vulnerability scanning, AI-assisted remediation, registry publication, GitOps deployment to EKS, Karpenter autoscaling, observability, and runtime security.

## Epic

### SECPLAT-EPIC — Build a secure cloud-native delivery platform

**Goal:** Deliver an automated software supply chain that builds, assesses, remediates, deploys, scales, monitors, and protects containerized workloads.

**Definition of done:**

- The end-to-end path from source commit to EKS deployment is automated.
- Vulnerable artifacts are blocked and secure artifacts are published.
- Deployments are reconciled through GitOps.
- Autoscaling, monitoring, dashboards, and runtime controls are operational.
- Operating procedures and evidence for each control are documented.

## Stories

### SECPLAT-01 — Trigger Jenkins CI from GitHub commits

**User story:** As a developer, I want commits to trigger the Jenkins pipeline so that every change is validated consistently.

**Acceptance criteria:**

- Commits to configured branches trigger the correct pipeline.
- The pipeline checks out the exact triggering revision.
- Trigger and checkout failures are visible to developers.

### SECPLAT-02 — Build an immutable container image

**User story:** As a platform engineer, I want the pipeline to build a versioned container image so that releases are reproducible and traceable.

**Acceptance criteria:**

- The image build runs only after source checkout succeeds.
- Every image is tagged with an immutable revision identifier.
- Build failures stop all downstream stages.

### SECPLAT-03 — Generate a software bill of materials

**User story:** As a security engineer, I want an SBOM generated for every image so that included software components are auditable.

**Acceptance criteria:**

- Syft generates an SBOM for each built image.
- The SBOM is stored as a pipeline artifact and linked to the image revision.
- Failure to generate the SBOM blocks promotion.

### SECPLAT-04 — Scan images for known vulnerabilities

**User story:** As a security engineer, I want each image scanned for CVEs so that vulnerable artifacts cannot be promoted.

**Acceptance criteria:**

- Grype or Trivy scans the built image and its packages.
- Configurable severity thresholds determine pass or fail.
- Scan findings are retained and visible from the pipeline.
- Images above the threshold do not reach the registry.

### SECPLAT-05 — Analyze vulnerability findings with AI

**User story:** As a developer, I want vulnerability findings enriched with remediation guidance so that issues can be resolved efficiently.

**Acceptance criteria:**

- Failed scan findings are sent to the analysis engine without credentials or secrets.
- Recommendations identify the affected component, safe target version, and rationale.
- Recommendations link back to the originating image and scan.
- Uncertain recommendations are clearly marked for manual review.

### SECPLAT-06 — Revalidate remediated builds

**User story:** As a security engineer, I want remediated changes to repeat the build and security checks so that only verified fixes are promoted.

**Acceptance criteria:**

- A remediation starts a new pipeline execution.
- The image, SBOM, and CVE scan are regenerated.
- Promotion occurs only when the configured security gate passes.
- Retry limits prevent an uncontrolled remediation loop.

### SECPLAT-07 — Publish approved images to the registry

**User story:** As a release engineer, I want approved images published to a registry so that deployment uses trusted artifacts.

**Acceptance criteria:**

- Only images that pass required pipeline gates are pushed.
- Registry authentication uses managed credentials.
- Published image digests and SBOM references are recorded.
- Mutable tag overwrite is prevented for release images.

### SECPLAT-08 — Deploy approved images through GitOps

**User story:** As a platform engineer, I want approved image changes reconciled through GitOps so that cluster state is declarative and auditable.

**Acceptance criteria:**

- Deployment manifests reference an approved immutable image digest.
- Changes are reviewed and committed to the GitOps source of truth.
- The GitOps controller reconciles the change to EKS.
- Failed reconciliation reports actionable status and supports rollback.

### SECPLAT-09 — Provision EKS capacity with Karpenter

**User story:** As a platform engineer, I want Karpenter to provision cluster nodes dynamically so that workloads receive capacity without static overprovisioning.

**Acceptance criteria:**

- Pending eligible workloads trigger node provisioning.
- Node selection follows configured workload, security, and cost constraints.
- Unused capacity is consolidated without disrupting protected workloads.
- Provisioning and consolidation events are observable.

### SECPLAT-10 — Collect platform and workload metrics

**User story:** As an SRE, I want Prometheus to collect platform and workload metrics so that service health and capacity can be measured.

**Acceptance criteria:**

- Prometheus discovers and scrapes the agreed EKS targets.
- Collection failures and storage pressure generate alerts.
- Metric retention and access controls meet platform requirements.
- Karpenter and workload health metrics are available for querying.

### SECPLAT-11 — Provide operational Grafana dashboards

**User story:** As an SRE, I want Grafana dashboards for delivery and runtime health so that teams can identify issues quickly.

**Acceptance criteria:**

- Dashboards show deployment, cluster, node, and workload health.
- Dashboard panels use the Prometheus data source and document their queries.
- Access follows least privilege.
- Dashboard definitions are version controlled.

### SECPLAT-12 — Enforce runtime security policies

**User story:** As a security engineer, I want runtime policies enforced in EKS so that deployed workloads operate within approved boundaries.

**Acceptance criteria:**

- Policies cover privileged execution, image provenance, and other agreed controls.
- Enforcement mode and exceptions are documented and auditable.
- Violations generate actionable alerts.
- Policy changes are tested before production enforcement.

## Jira import workbook

`Jira_Stories.xlsx` contains one row per issue with Jira-friendly columns. During import:

1. Replace `SECPLAT` in the **Project key** column if the target project uses another key.
2. Map **Epic Name** and **Epic Link** according to the target Jira deployment. Team-managed projects may use **Parent** instead.
3. Jira Cloud imports CSV natively; if XLSX is not accepted by the installed importer, save the **Jira Import** sheet as CSV before uploading.
4. Review user names, components, priorities, and required custom fields before completing the import.
