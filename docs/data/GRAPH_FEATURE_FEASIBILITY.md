# JDIS Graph Feature Feasibility Assessment

**Project**: Judicial Delay Intelligence System (JDIS)  
**Role**: Tanmay — Data Engineer & Data Architect  
**Date**: August 2026  
**Document Classification**: Graph & Network Feature Feasibility  
**Feasibility Verdict**: **PARTIALLY FEASIBLE (Judge-Court Bipartite Graphs Supported; Litigant/Lawyer Networks Infeasible due to Anonymization)**

---

## 1. Objective

The JDIS execution manual and research proposal suggest exploring graph-based relational features (e.g., party repeat-litigation networks, lawyer case density, judge-court transfer networks) to capture institutional complexity and structural delay propagation.

This investigation audits all identifier and relationship columns across the DDL dataset to determine which graph structures are mathematically and empirically sound.

---

## 2. Identifier Audit & Anonymization Constraints

| Entity | Identifier Available in DDL | Stability Across Cases / Time | Feasibility for Graph Construction |
| :--- | :--- | :--- | :--- |
| **Judge** | `ddl_judge_id` (Integer, 1 to 98,478) | **Stable & Unique** across all postings in `judges_clean.csv` | **FULLY FEASIBLE** |
| **Court Complex** | `(state_code, dist_code, court_no)` | **Stable & Unique** across all years in `cases_court_key.csv` (6,958 courts) | **FULLY FEASIBLE** |
| **Case** | `ddl_case_id` / `cino` (CNR) | **Stable & Unique** per case filing | **FULLY FEASIBLE** |
| **Petitioner / Litigant** | None (only `female_petitioner` gender flags: `"0 male"`, `"1 female"`, `"-9998 unclear"`) | **No persistent litigant IDs** across cases (names stripped for privacy) | **INFEASIBLE** |
| **Respondent / Defendant** | None (only `female_defendant` gender flags: `"0 male"`, `"1 female"`, `"-9998 unclear"`) | **No persistent defendant IDs** across cases | **INFEASIBLE** |
| **Lawyer / Advocate** | None (only `female_adv_pet`, `female_adv_def` flags: `0`, `1`, `-9998`, `-9999`) | **No bar council registration IDs** or lawyer names | **INFEASIBLE** |

---

## 3. Feasible Graph Formulations

### 3.1 Judge-Court Bipartite & Mobility Graph
We can construct a weighted bipartite graph $G = (V_{\text{Judge}}, V_{\text{Court}}, E)$:
- **Nodes**: 98,478 Judge nodes and 6,958 Court nodes.
- **Edges**: Assigned tenure from `judges_clean.csv` where edge weight $w = \text{duration of posting in days}$.
- **Extracted Graph Features**:
  1. `judge_court_degree`: Number of distinct court complexes a judge has presided over.
  2. `court_judge_turnover_rate`: Number of distinct judicial officers assigned to a court over a 3-year rolling window (captures judicial vacancy and transfer turbulence).
  3. `judge_experience_days`: Cumulative days of judicial tenure prior to case filing date.

### 3.2 Case-Act Co-Occurrence Graph
A bipartite network linking Cases to Statutory Acts/Sections:
- **Nodes**: Cases and Legal Sections (e.g., IPC 302, CrPC 138, etc.).
- **Extracted Graph Features**:
  1. `section_degree`: Number of cases citing a particular legal section.
  2. `statutory_complexity_score`: Number of distinct legal acts attached to a single case.

---

## 4. Infeasible Formulations & Scientific Boundaries

1. **Litigant Habitual Offender / Repeat Party Graph**:
   - Because DDL strictly anonymizes litigant identities to protect personal privacy, **no cross-case litigant tracking is possible**.
   - Attempting to group cases by identical court + year to create "synthetic repeat parties" is statistically invalid and prohibited.
2. **Lawyer Case Congestion Graph**:
   - Advocate names are not provided in the public dataset; therefore, individual lawyer caseload cannot be measured directly.
3. **Graph Neural Networks (GNNs)**:
   - In alignment with Section 14.3 of the IEEE Execution Manual, deep GNN architectures should not be built as a core dependency for the 10-week timeline. Graph features will be extracted as tabular graph centrality/degree metrics.

---

## 5. Summary & Action Plan for Feature Engineering

- **Implemented Features**:
  - `court_judge_turnover_prior_3yr` (Float)
  - `judge_total_prior_tenure_days` (Integer)
  - `case_statutory_act_count` (Integer)
  - `case_ipc_section_count` (Integer)
- **Documented Limitation**: The absence of litigant and lawyer identifiers will be formally stated in `ETHICS_AND_LIMITATIONS.md` and Section III of the IEEE paper.
