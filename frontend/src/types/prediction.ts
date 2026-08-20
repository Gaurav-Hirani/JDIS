// JDIS Prediction & SHAP Feature Interfaces matching ML_INFERENCE_CONTRACT.md

export type RiskBand = 'Low' | 'Moderate' | 'High' | 'Very High';

export interface FilingCaseFeatures {
  // Required string fields per contract
  state_code: string;
  dist_code: string;
  court_no: string;
  type_name: string;

  // Temporal metadata
  filing_month?: number;        // 1..12 (default 1)
  filing_day_of_week?: number;  // 0..6 (default 1)
  filing_quarter?: number;      // 1..4 (default 1)

  // Case classification
  case_type_str?: string;
  case_category?: string;
  is_criminal_code?: number;    // 0 or 1

  // Statutory details
  statutory_act_count?: number;
  ipc_section_count?: number;
  bailable_ipc_flag?: string;
  primary_act_id?: string;

  // Demographics & counsel
  female_defendant_clean?: string;
  female_petitioner_clean?: string;
  female_adv_def_clean?: string;
  female_adv_pet_clean?: string;

  // Geography & Court labels
  state_str?: string;
  district_str?: string;
  court_str?: string;

  // Judicial attributes
  ddl_filing_judge_id?: string;
  judge_position_clean?: string;
  judge_gender?: string;
  judge_tenure_days?: number;

  // Historical court throughput metrics
  court_prior_delay_rate?: number;
  court_prior_avg_duration?: number;
  court_prior_active_backlog?: number;
  casetype_prior_delay_rate?: number;
}

export interface SHAPExplanationItem {
  feature_name: string;
  contribution: number;
  direction: 'positive' | 'negative';
  feature_group?: string;
  human_readable_description?: string;
  parent_feature?: string;
  feature_value?: string | number | null;
  rank?: number;
}

export interface DelayPredictionResponse {
  prediction_id: string;
  case_id?: string | null;
  raw_probability: number;
  calibrated_probability: number;
  risk_score: number; // 0..100 integer
  risk_band: RiskBand;
  model_version: string;
  timestamp: string;
  shap_explanations?: SHAPExplanationItem[];
}

export interface DurationPredictionResponse {
  prediction_id: string;
  predicted_duration_days: number;
  model_version: string;
  limitations_flag: string;
  timestamp: string;
}

export interface DetailedExplanationResponse {
  prediction_id: string;
  model_version: string;
  calibrated_probability: number;
  risk_score: number;
  risk_band: RiskBand;
  top_contributors: SHAPExplanationItem[];
  summary: string;
  timestamp: string;
}
