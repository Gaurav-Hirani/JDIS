# ML Inference Contract

```json
// Input Schema for Filing-Time Classification
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Case Filing Features",
  "type": "object",
  "properties": {
    "filing_month": { "type": "integer" },
    "filing_day_of_week": { "type": "integer" },
    "filing_quarter": { "type": "integer" },
    "type_name": { "type": "string" },
    "case_type_str": { "type": "string" },
    "case_category": { "type": "string" },
    "is_criminal_code": { "type": "integer" },
    "statutory_act_count": { "type": "integer" },
    "ipc_section_count": { "type": "integer" },
    "bailable_ipc_flag": { "type": "string" },
    "primary_act_id": { "type": "string" },
    "female_defendant_clean": { "type": "string" },
    "female_petitioner_clean": { "type": "string" },
    "female_adv_def_clean": { "type": "string" },
    "female_adv_pet_clean": { "type": "string" },
    "state_code": { "type": "string" },
    "dist_code": { "type": "string" },
    "court_no": { "type": "string" },
    "state_str": { "type": "string" },
    "district_str": { "type": "string" },
    "court_str": { "type": "string" },
    "ddl_filing_judge_id": { "type": "string" },
    "judge_position_clean": { "type": "string" },
    "judge_gender": { "type": "string" },
    "judge_tenure_days": { "type": "number" },
    "court_prior_delay_rate": { "type": "number" },
    "court_prior_avg_duration": { "type": "number" },
    "court_prior_active_backlog": { "type": "number" },
    "casetype_prior_delay_rate": { "type": "number" }
  },
  "required": ["state_code", "dist_code", "court_no", "type_name"]
}
```

```json
// Output Schema for Filing-Time Classification
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Risk Prediction Response",
  "type": "object",
  "properties": {
    "raw_probability": { "type": "number" },
    "calibrated_probability": { "type": "number" },
    "risk_score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "risk_band": { "type": "string", "enum": ["Low", "Moderate", "High", "Very High"] },
    "model_version": { "type": "string" },
    "shap_explanations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "feature_name": { "type": "string" },
          "contribution": { "type": "number" }
        }
      }
    }
  }
}
```
