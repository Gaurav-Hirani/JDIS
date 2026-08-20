import { apiClient } from './client';
import { 
  AnalyticsSummary, 
  RiskDistributionItem, 
  CourtAnalyticsItem, 
  CaseTypeAnalyticsItem 
} from '../types/analytics';

export async function fetchAnalyticsSummary(): Promise<AnalyticsSummary> {
  const response = await apiClient.get<AnalyticsSummary>('/analytics/summary');
  return response.data;
}

export async function fetchRiskDistribution(): Promise<RiskDistributionItem[]> {
  const response = await apiClient.get<RiskDistributionItem[]>('/analytics/risk-distribution');
  return response.data;
}

export async function fetchCourtAnalytics(): Promise<CourtAnalyticsItem[]> {
  const response = await apiClient.get<CourtAnalyticsItem[]>('/analytics/courts');
  return response.data;
}

export async function fetchCaseTypeAnalytics(): Promise<CaseTypeAnalyticsItem[]> {
  const response = await apiClient.get<CaseTypeAnalyticsItem[]>('/analytics/case-types');
  return response.data;
}
