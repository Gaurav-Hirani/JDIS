import { apiClient } from './client';
import { 
  FilingCaseFeatures, 
  DelayPredictionResponse, 
  DurationPredictionResponse, 
  DetailedExplanationResponse 
} from '../types/prediction';

export async function predictFilingDelay(features: FilingCaseFeatures): Promise<DelayPredictionResponse> {
  const response = await apiClient.post<DelayPredictionResponse>('/predictions/delay', features);
  return response.data;
}

export async function predictCaseDuration(features: FilingCaseFeatures): Promise<DurationPredictionResponse> {
  const response = await apiClient.post<DurationPredictionResponse>('/predictions/duration', features);
  return response.data;
}

export async function getSHAPExplanation(predictionId: string): Promise<DetailedExplanationResponse> {
  const response = await apiClient.get<DetailedExplanationResponse>(`/predictions/${predictionId}/explanation`);
  return response.data;
}
