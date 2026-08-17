# JDIS Adjournment Feasibility Assessment

**Project**: Judicial Delay Intelligence System (JDIS)  
**Role**: Tanmay — Data Engineer & Data Architect  
**Date**: August 2026  
**Document Classification**: Scientific Feasibility & Scope Determination  
**Target Feasibility Status**: **PARTIALLY FEASIBLE (Proxy Required)**

---

## 1. Objective of Investigation

The JDIS research plan and execution manual define an intended predictive component for *adjournment prediction / next-hearing risk*. 

As mandated by **Rule 5 of the Data Engineer Master Instructions**, we conducted an exhaustive schema and record-level inspection across all raw archives (`cases.tar.gz`, `keys.tar.gz`, `judges_clean.tar.gz`, `acts_sections.tar.gz`) to determine whether:
1. An explicit, ground-truth adjournment status exists for individual hearing events.
2. A scientifically valid and defensible proxy can be constructed.
3. The module must be scoped and renamed to prevent scientific misrepresentation.

---

## 2. Empirical Findings from Raw Dataset

### 2.1 Absence of Granular Hearing-by-Hearing Logs
- The Development Data Lab (DDL) public e-Courts release does **not** include a per-hearing transaction table (e.g., individual hearing date logs with per-session outcome codes).
- The raw dataset stores case-level aggregate milestones on each case record in `cases_YYYY.csv`:
  - `date_of_filing`: Initial filing date (100% present).
  - `date_first_list`: First hearing listing date (99.64% present).
  - `date_last_list`: Last hearing listing date (99.52% present).
  - `date_next_list`: Next scheduled listing date (99.52% present).
  - `purpose_name`: Single integer code mapping to the primary/current hearing stage purpose in `purpose_name_key.csv`.

### 2.2 Absence of Explicit Binary Adjournment Column
- There is **no explicit binary column** such as `is_adjourned (0/1)` or `adjournment_granted (True/False)` in the case records.
- In `purpose_name_key.csv`, out of 80,935,944 historical hearing purpose instances, specific adjournment-related purpose codes exist in only 153,146 records (0.19%):
  - `"adjourned"`: 151,013 instances
  - `"adjourned-191"`: 1,174 instances
  - `"no sitting case adjourned to"`: 230 instances
  - `"call on / stayed / awaiting notice / awaiting warrant"`: 8,472,130 instances (10.47%)

### 2.3 Scientific Risk of Fabricating Labels
- In standard Indian District Court procedure under the Civil Procedure Code (CPC Order XVII) and Criminal Procedure Code (CrPC), a case proceeds through multiple substantive hearings (e.g., *Summons → Framing of Charge → Evidence / Cross-Examination → Arguments → Judgement*).
- **The mere occurrence of multiple listings or hearing dates does NOT constitute an adjournment.**
- Manufacturing a synthetic binary `adjourned = 1` whenever `date_last_list != date_first_list` would be scientifically fraudulent and violate IEEE peer-review standards.

---

## 3. Formal Feasibility Classification

### Verdict: **PARTIALLY FEASIBLE**

Direct session-level adjournment classification is **not feasible** on the static DDL snapshot without granular proceeding-level logs. However, **Case-Level Hearing Continuation Risk** and **Hearing-Gap Escalation** can be rigorously and defensibly formulated.

---

## 4. Scientifically Defensible Proxy Formulation

In alignment with **Section 4.4 and Section 14 of the IEEE Execution Manual**, we formulate two defensible, leakage-safe hearing delay metrics:

### Proxy 1: Hearing Span Index (`hearing_span_days`)
The total temporal footprint of court hearings observed for the case:
$$\text{hearing\_span\_days} = \text{date\_last\_list} - \text{date\_first\_list}$$
- **Sample Median**: 356.0 days (~11.7 months)
- **Sample Mean**: 583.0 days (~19.2 months)

### Proxy 2: Next-Listing Gap / Scheduling Latency (`next_listing_gap_days`)
The interval between the last hearing and the subsequent scheduled date:
$$\text{next\_listing\_gap\_days} = \text{date\_next\_list} - \text{date\_last\_list}$$
- Reflects court congestion, administrative backlog, and procedural delay between successive listings.

### Proxy 3: Hearing Delay Risk Classification (`hearing_delay_risk`)
A binary risk indicator defined for active/in-progress cases:
$$\text{hearing\_delay\_risk} = \begin{cases} 1 & \text{if } \text{hearing\_span\_days} > 365.25 \text{ days} \\ 0 & \text{otherwise} \end{cases}$$
- For in-progress cases, this models whether the hearing process has extended past 1 calendar year without resolution.

---

## 5. Required Actions & Stop Condition

> [!IMPORTANT]
> **Action Required for Gaurav (AI/ML Lead) and Shukla (Frontend Lead):**
> 1. In all research papers, model architectures, and API endpoints, the module must be designated as:
>    - **"Hearing Delay Risk & Continuation Predictor"** (NOT "Individual Session Adjournment Classifier").
> 2. The API route should be documented as:
>    - `POST /api/predict/hearing-risk` or `POST /api/predict/delay-risk`.
> 3. The IEEE research paper Section III (Methodology) will explicitly document this operational definition and reference DDL data structure constraints.

**Human Team Approval**: This feasibility report is submitted for user review before pipeline execution.
