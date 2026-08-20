import { FilingCaseFeatures, RiskBand } from './prediction';

export interface LatestPredictionSummary {
  id?: string;
  prediction_type?: string;
  model_version?: string;
  calibrated_probability?: number;
  risk_score: number;
  risk_band: RiskBand;
  created_at?: string;
}

export interface CaseRecord extends FilingCaseFeatures {
  id: string;
  ddl_case_id?: string | null;
  created_at: string;
  updated_at: string;
  latest_prediction?: LatestPredictionSummary | null;
}

export interface CaseListParams {
  page?: number;
  page_size?: number;
  state_code?: string;
  court_no?: string;
  type_name?: string;
  risk_band?: RiskBand;
  search?: string;
}

export interface CaseListResponse {
  total: number;
  page: number;
  page_size: number;
  items: CaseRecord[];
}

export interface CreateCaseRequest extends FilingCaseFeatures {
  ddl_case_id?: string;
}
