// JDIS API Base Error and Health Response Interfaces

export interface HealthCheckResponse {
  status: string;
  database: string;
  models: string;
  model_version: string;
  details: {
    classifier_loaded: boolean;
    regressor_loaded: boolean;
    shap_ready: boolean;
  };
}

export interface ApiValidationErrorDetail {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface ApiErrorResponse {
  error: boolean;
  message: string;
  details?: ApiValidationErrorDetail[] | Record<string, unknown>;
  path?: string;
}
