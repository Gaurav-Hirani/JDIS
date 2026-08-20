import axios from 'axios';
import { HealthCheckResponse } from '../types/api';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';
// Resolve server root from API base path (e.g. "http://localhost:8000/api/v1" -> "http://localhost:8000")
const SERVER_ROOT = API_BASE.includes('/api/v1') 
  ? API_BASE.replace('/api/v1', '') 
  : '';

export async function fetchHealthStatus(): Promise<HealthCheckResponse> {
  try {
    const healthUrl = `${SERVER_ROOT}/health`;
    const response = await axios.get<HealthCheckResponse>(healthUrl, { timeout: 4000 });
    return response.data;
  } catch (error) {
    // Fallback attempt to /health via base client if root fails
    const fallbackUrl = '/health';
    const response = await axios.get<HealthCheckResponse>(fallbackUrl, { timeout: 4000 });
    return response.data;
  }
}
