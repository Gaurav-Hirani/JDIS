import axios, { AxiosError } from 'axios';
import { ApiErrorResponse } from '../types/api';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorResponse>) => {
    if (error.response && error.response.data) {
      const customError = new Error(error.response.data.message || 'API request failed') as Error & {
        status?: number;
        details?: unknown;
      };
      customError.status = error.response.status;
      customError.details = error.response.data.details;
      return Promise.reject(customError);
    }
    if (error.code === 'ECONNABORTED') {
      return Promise.reject(new Error('Request timed out while connecting to JDIS backend'));
    }
    return Promise.reject(new Error('Unable to connect to the JDIS backend service'));
  }
);
