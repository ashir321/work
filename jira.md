# JIRA Story — AWS Compute Cost Optimisation Strategy

> Source: `AWS_Compute_Cost_Optimisation_Strategy.pptx`
> A 90-day, metrics-led model to reduce AWS VM compute cost through visibility, scheduling, right-sizing, dynamic scaling and commercial optimisation.

---

## Epic

**Epic Name:** AWS Compute Cost Optimisation Strategy (90-Day Operating Model)

**Summary:** Implement a governed, metrics-led operating model to reduce AWS EC2/VM compute cost by 30–40% within 90 days across R&D, SaaS and departmental installations, without causing critical incidents.

**Description:**
Infrastructure often remains active beyond actual workload demand; some VMs are idle or underutilised, and fixed worker capacity is kept for intermittent workloads. This epic instruments all VMs, classifies utilisation, automates non-production runtime, right-sizes capacity, migrates eligible workloads, optimises load balancers, dynamically scales EKS workloads, and applies commercial commitments only after the baseline stabilises.

**Governance principle:** Recommendations are evidence-backed; production execution remains owner-approved; savings are verified through AWS billing data.

**Scope:** AWS EC2 / VM compute only. LLM cost, GPU, storage/ECR and network transfer are separate optimisation tracks.

**Success Metrics / Acceptance Criteria:**
- 30–40% target compute-cost reduction achieved in 90 days.
- 100% of VM inventory mapped to owner and application.
- >80% of approved actions implemented across eligible environments.
- 0 critical incidents caused by optimisation.
- Savings validated through AWS billing data.

**Execution sequence (must be respected):** Identify → Schedule → Right-size → Consolidate → Migrate/Modernise → Dynamically Scale → Commercially Commit. Reserved Instances are assessed only after idle runtime, oversized capacity and non-optimised platform choices are addressed.

---

## Stories

### Story 1 — Baseline & Visibility (VorteX + AWS inventory)
**As a** FinOps/platform team,
**I want** complete VM inventory, owner mapping, VorteX agent coverage, a cost baseline and utilisation classification,
**so that** every optimisation action is evidence-backed and traceable to an owner.

**Acceptance Criteria:**
- All AWS VMs have VorteX agents deployed capturing utilisation, runtime and ownership.
- 100% of VM inventory mapped to owner and application.
- Cost baseline established from AWS billing.
- VMs classified as idle, underutilised, overutilised or intermittent.

**Phase:** Weeks 1–3.

---

### Story 2 — Self-Service Grouping & Scheduling
**As an** application owner,
**I want** grouping, scheduled start/stop and component-level grouping,
**so that** only required VMs run and non-production runtime is automated.

**Acceptance Criteria:**
- Self-service grouping and component-level grouping available.
- Scheduled start/stop configured for eligible non-production environments.
- Idle VM removal executed for approved resources.

**Phase:** Weeks 4–8.

---

### Story 3 — Right-Size & Consolidate
**As a** platform engineer,
**I want** oversized instances downsized and compatible workloads consolidated onto fewer right-sized hosts,
**so that** capacity follows actual demand.

**Acceptance Criteria:**
- Oversized instances identified and right-sized after owner approval.
- Compatible workloads consolidated onto fewer right-sized hosts.
- No critical incidents introduced by changes.

**Phase:** Weeks 4–8.

---

### Story 4 — EKS + OS Optimisation
**As a** platform team,
**I want** eligible native Kubernetes workloads moved to Amazon EKS and RHEL worker dependency reduced where Amazon Linux is sufficient,
**so that** per-instance OS licence cost is reduced (draft example ~39% per-instance OS licence saving).

**Acceptance Criteria:**
- Eligible native K8s workloads migrated to EKS.
- RHEL-based workers replaced with Amazon Linux where sufficient.
- OS licence saving measured and reported.

**Phase:** Weeks 4–8.

---

### Story 5 — CLB / ELB → NLB Consolidation
**As a** network/platform engineer,
**I want** suitable traffic shifted from multiple CLBs/ELBs to a consolidated NLB model per environment,
**so that** load-balancer cost is reduced through consolidation.

**Acceptance Criteria:**
- Suitable traffic migrated to a consolidated NLB per environment.
- LB inventory reduced; conversions tracked in the scorecard.

**Phase:** Weeks 4–8.

---

### Story 6 — Karpenter Dynamic Scaling for EKS Workloads
**As a** platform team,
**I want** Karpenter to dynamically provision and consolidate EKS worker nodes for native Python, AI/ML and agentic workloads,
**so that** we avoid permanently running worker nodes for intermittent processing.

**Acceptance Criteria:**
- Karpenter provisions worker nodes on demand and removes them when demand reduces.
- No over-provisioning "just in case"; start small and scale only when needed.
- First Karpenter workloads onboarded and utilisation tracked.

**Phase:** Weeks 4–8 (first workloads), expand Weeks 9–12.

---

### Story 7 — AI Recommendation Layer (VorteX + AWS Signals)
**As a** FinOps team,
**I want** an AI agent using VorteX + AWS cost signals to continuously rank idle, underutilised, overutilised and oversized VMs with estimated savings,
**so that** owners receive ranked, evidence-backed actions.

**Acceptance Criteria:**
- Agent continuously identifies idle/underutilised/overutilised/oversized VMs.
- Ranked actions produced with estimated savings.
- Initial mode is recommendation-only; production changes require owner validation, dependency assessment and approved change execution.

**Phase:** Weeks 4–12.

---

### Story 8 — Reserved Instance (Commercial) Strategy
**As a** FinOps lead,
**I want** 1-year or 3-year commitments applied only to predictable, always-on workloads,
**so that** we do not lock in excess capacity.

**Acceptance Criteria:**
- RI evaluation performed only after scheduling, right-sizing, consolidation and dynamic scaling are complete.
- Commitments applied to stable baseline capacity only.
- Pricing figures validated via AWS Cost Explorer / Pricing Calculator before commitment.

**Phase:** Weeks 9–12.

---

### Story 9 — Scale, Govern & Validate Savings
**As a** program owner,
**I want** the model expanded to eligible environments with savings validated and a dashboard published,
**so that** the optimisation is a governed operating discipline, not a one-time cleanup.

**Acceptance Criteria:**
- Model expanded to eligible environments.
- Savings validated through AWS billing and utilisation dashboard.
- Monthly scorecard published: baseline vs current cost, idle/underutilised VMs, non-business-hour runtime, right-sized/consolidated VMs, EKS/OS migrations, CLB→NLB conversions, Karpenter utilisation, RI baseline, billing-validated savings.
- 0 critical incidents caused by optimisation.

**Phase:** Weeks 9–12.

---

## Validated Reference Pattern — mcube Demo
The mcube demo environment achieved ≈50% compute-cost reduction by moving to Amazon EKS, enabling self-service grouping, starting only required component groups and stopping unused component VMs. Use this as a validated reference pattern — not a flat promise — and apply only after assessing architecture, dependencies, usage pattern and risk for each environment.
