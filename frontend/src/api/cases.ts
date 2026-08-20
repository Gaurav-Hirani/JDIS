import { apiClient } from './client';
import { CaseRecord, CaseListParams, CaseListResponse, CreateCaseRequest } from '../types/case';

export async function createCaseRecord(data: CreateCaseRequest): Promise<CaseRecord> {
  const response = await apiClient.post<CaseRecord>('/cases', data);
  return response.data;
}

export async function fetchCases(params: CaseListParams = {}): Promise<CaseListResponse> {
  const response = await apiClient.get<CaseListResponse>('/cases', { params });
  return response.data;
}

export async function fetchCaseById(id: string): Promise<CaseRecord> {
  const response = await apiClient.get<CaseRecord>(`/cases/${id}`);
  return response.data;
}

export async function updateCaseRecord(id: string, updates: Partial<CaseRecord>): Promise<CaseRecord> {
  const response = await apiClient.patch<CaseRecord>(`/cases/${id}`, updates);
  return response.data;
}
