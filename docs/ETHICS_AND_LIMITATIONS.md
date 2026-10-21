# Ethics, Scope and Limitations

> **JDIS provides associational delay estimates for judicial backlog management.
> Not a guarantee of outcome.**

That sentence appears verbatim in the frontend sidebar and is the single most
important thing to understand about this system before using it. The rest of this
document is the detailed rationale behind it.

---

## What this system does

JDIS estimates the probability that a case filed in an Indian district court will
exceed 24 months to dispose of, using only the 29 administrative fields that exist
at filing time — court identifiers, case type, judge metadata, and historical
throughput statistics computed strictly before the filing date.

It is a **backlog management tool**. It answers: *given what a clerk knows when the
case is registered, how likely is this filing to become a long-running case?* That
is a question about judicial workload distribution. It is not a question about any
party's claim.

## What this system does not do

- It does not predict the **merits, outcome, or disposition** of any case.
- It does not assess the rights, claims, or positions of any party.
- It does not model individual case complexity, evidence quality, or legal arguments.
- It does not provide legal advice and should not be interpreted as such.
- It does not substitute for judicial decision-making.

The model input contains no information about the substance of the dispute. A "High"
risk score says the court and case type historically move slowly; it says nothing
about whether the outcome is likely to be favourable to any side.

---

## Methodological honesty: published negative results

The duration regressor and the hearing-gap model are **not useful**, and their held-out
performance reflects that:

| Model | Held-out R² | Status |
| :--- | :--- | :--- |
| Delay classifier (primary) | — | ROC-AUC 0.7938, reported |
| Duration regressor | **−0.0887** | Published, not suppressed |
| Hearing-gap model | **−1.7032** | Published, not suppressed |

A negative R² means the model performs worse than a horizontal line — it is worse
than simply predicting the mean. Publishing these numbers rather than excluding them
is a deliberate methodological choice: it demonstrates that the researchers tested for
false positives, not just true positives. If the duration regressor had been dropped
silently, there would be no evidence the system was stress-tested honestly.

The duration regressor remains in the deployed API because it produces a structurally
valid output (clamped to a minimum of 1.0 day) and the `limitations_flag` field
forces clients to acknowledge its status on every response. It should never be
presented without that flag.

---

## Right-censoring rule

Unresolved cases are handled through a strict right-censoring rule in
`src/data/create_final_datasets.py`:

- A case is labelled **delayed** (1) only if it had been pending for more than
  **730.5 days** at data extraction.
- A case is labelled **not delayed** (0) only if it was disposed of within 730.5 days.
- A case still pending for ≤ 730.5 days at extraction is excluded as **unknown**.

This means the model has never learned to classify cases that are genuinely ambiguous
at the 24-month boundary — those were removed before training. The model's apparent
accuracy on the test set is partly a consequence of that filtering, not evidence that
it would generalise cleanly to live, in-progress cases.

---

## Calibration: isotonic monotonic-stepwise caveat

The production classifier applies isotonic regression to calibrate raw model
probabilities against the validation cohort. Isotonic regression is monotonic and
stepwise: it preserves the ordering of raw probabilities but can map many distinct
raw values to the same calibrated value.

As a consequence, **two filings with different raw model outputs can legitimately
receive the same risk score.** This is not a bug or a tie-breaking artefact — it is
the mathematical behaviour of a monotonic calibrator. If you observe identical scores
for cases the model otherwise treats as distinguishable, the isotonic step function is
the reason, not a data error.

Calibration quality is measured on held-out data (ECE 0.0453), but no held-out data
exists for the operational period after 2016, so the calibration claim has no
empirical support beyond that boundary.

---

## Temporal validity: unmeasured drift

**Model v1.0-config-d has never seen a case filed after 2016.** The training set
covers 2010–2014; the validation set covers 2015; the test set covers 2016. No
evaluation has been run on 2017 or later data.

Judicial throughput in India has changed materially since 2016 — digital filing
adoption, circuit courts, and the National Judicial Data Grid's own operational
changes are all relevant. The model's behaviour on any post-2016 case is
**unmeasured and potentially poor**. Any evaluation before using this system on
contemporary data should begin by measuring drift explicitly rather than assuming
the 2016 metrics still hold.

---

## Explainability: SHAP as post-hoc description, not causal claim

SHAP TreeExplainer attributions are returned with every prediction. They describe
how much each feature contributed to the model's output for that specific case. They
do not establish a causal relationship between the feature and eventual delay.

A SHAP contribution for `court_prior_delay_rate` means the model relies heavily on
that input — it does not mean that changing a court's historical delay rate would
cause the case to be delayed faster or slower. Correlation, not causation.

---

## Authentication and deployment

**There is no authentication layer.** No endpoint requires credentials; no user
accounts, tokens, or authorisation checks exist. The application is designed for
internal decision-support use on a trusted network — a court office LAN, a
government intranet, or a research evaluation environment.

It must not be exposed publicly. There is no rate limiting, no request auditing tied
to a user identity, and no input sanitisation layer above the Pydantic schema
validation. Exposing `/api/v1/` on an untrusted network would leave every case record,
prediction, and analytics aggregate reachable by any caller.

If deployment requires authentication, add a reverse proxy (e.g. OAuth 2.0 proxy,
API gateway with API keys) in front of the application before connecting it to any
network the operators do not fully control.

---

## Risk band interpretation

| Band | Score | Meaning |
| :--- | :--- | :--- |
| Low | 0–20 | Low probability of exceeding 24 months based on historical patterns |
| Moderate | 21–50 | Moderate probability |
| High | 51–80 | High probability |
| Very High | 81–100 | Very high probability |

These bands are **statistical probabilities derived from filing-time metadata**. They
are not predictions of a case's merits, outcome, or procedural fairness. They are not
guarantees. They should inform triage and resource allocation decisions, not
substitute for judicial judgement.

---

## Known limitations in one list

1. **No post-2016 evaluation.** Behaviour on contemporary filings is unmeasured.
2. **Censoring filter removes boundary cases.** Accuracy reflects the filtered test
   set, not all possible real-world cases.
3. **Duration regressor is unreliable.** R² is negative; the `limitations_flag` must
   always be displayed alongside any duration output.
4. **SHAP is not causal.** Attributions describe model dependence, not real-world
   causation.
5. **No authentication.** Not safe for public or untrusted-network exposure.
6. **Administrative metadata only.** No merits, evidence, or claim information enters
   the model. Scores cannot reflect the substance of a dispute.
7. **Isotonic calibration can produce ties.** Identical scores for distinct inputs are
   expected and correct, not a data error.
8. **Right-censoring at 730.5 days** means the model's training data excludes cases
   that were ambiguous at the 24-month boundary.

---

## References

- `docs/API_SPECIFICATION.md` — full endpoint reference including the
  `limitations_flag` contract
- `research/REPRODUCIBILITY.md` — exact reproduction steps and all reported metrics
- `docs/data/FINAL_ML_HANDOFF_TO_BACKEND.md` — inference contract and feature
  definitions
- `docs/data/FINAL_MODEL_FEATURE_SPECIFICATION.md` — the 29 Config D features
- `docs/DEMO_RUNBOOK.md` — end-to-end demonstration script
