import { RiskBand } from './prediction';

export interface AnalyticsSummary {
  total_cases: number;
  total_predictions: number;
  high_risk_cases_count: number;
  high_risk_cases_percentage: number;
  average_risk_score: number;
  average_predicted_duration_days: number;
}

export interface RiskDistributionItem {
  risk_band: RiskBand;
  count: number;
  percentage: number;
}

export interface CourtAnalyticsItem {
  court_identifier?: string;
  court_str?: string;
  state_code?: string;
  dist_code?: string;
  court_no?: string;
  case_count: number;
  high_risk_count?: number;
  high_risk_percentage: number;
  average_risk_score: number;
  average_duration_days?: number;
}

export interface CaseTypeAnalyticsItem {
  type_name: string;
  case_count: number;
  high_risk_count?: number;
  high_risk_percentage: number;
  average_risk_score: number;
}
