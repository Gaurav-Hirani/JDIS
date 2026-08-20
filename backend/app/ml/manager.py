import os
import joblib
import pandas as pd
import numpy as np
import shap
from typing import Dict, Any, List, Optional, Tuple
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.errors import ModelNotFoundException

class ModelManager:
    _instance: Optional["ModelManager"] = None

    def __init__(self):
        self.classifier = None
        self.regressor = None
        self.base_pipeline = None
        self.tree_model = None
        self.preprocessor = None
        self.feature_names = []
        self.explainer = None
        self.is_loaded = False
        self.model_version = settings.MODEL_VERSION

    @classmethod
    def get_instance(cls) -> "ModelManager":
        if cls._instance is None:
            cls._instance = ModelManager()
        return cls._instance

    def load_models(self) -> None:
        """Centralized singleton model loading at application startup."""
        logger.info("Initializing ModelManager: Loading ML pipelines...")
        
        clf_path = settings.MODEL_CLASSIFIER_PATH
        reg_path = settings.MODEL_REGRESSOR_PATH

        if not os.path.exists(clf_path):
            logger.error(f"Classification model artifact missing at '{clf_path}'")
            raise ModelNotFoundException(f"Classifier artifact not found at {clf_path}")

        if not os.path.exists(reg_path):
            logger.error(f"Regression model artifact missing at '{reg_path}'")
            raise ModelNotFoundException(f"Regressor artifact not found at {reg_path}")

        try:
            self.classifier = joblib.load(clf_path)
            logger.info(f"Loaded calibrated classifier from {clf_path}")

            self.regressor = joblib.load(reg_path)
            logger.info(f"Loaded duration regressor from {reg_path}")

            # Extract base pipeline and preprocessor for SHAP TreeExplainer
            if hasattr(self.classifier, "estimator"):
                base_pipe = self.classifier.estimator
                if hasattr(base_pipe, "estimator"):
                    base_pipe = base_pipe.estimator
            elif hasattr(self.classifier, "calibrated_classifiers_"):
                base_pipe = self.classifier.calibrated_classifiers_[0].estimator
                if hasattr(base_pipe, "estimator"):
                    base_pipe = base_pipe.estimator
            else:
                base_pipe = None

            if base_pipe is not None and hasattr(base_pipe, "named_steps"):
                self.base_pipeline = base_pipe
                self.preprocessor = base_pipe.named_steps["preprocessor"]
                self.tree_model = base_pipe.named_steps["model"]
                
                # Get transformed feature names
                raw_names = self.preprocessor.get_feature_names_out()
                self.feature_names = [f.replace("num__", "").replace("cat__", "") for f in raw_names]
                
                # Initialize SHAP TreeExplainer once
                self.explainer = shap.TreeExplainer(self.tree_model)
                logger.info(f"Initialized SHAP TreeExplainer with {len(self.feature_names)} feature dimensions")
            else:
                logger.warning("Could not extract underlying tree estimator for SHAP explainer.")

            self.is_loaded = True
            logger.info("All ML model artifacts loaded and validated successfully.")

        except Exception as e:
            self.is_loaded = False
            logger.exception(f"Fatal error loading model artifacts: {str(e)}")
            raise ModelNotFoundException(f"Failed to initialize ML models: {str(e)}")

    def get_health_status(self) -> Dict[str, Any]:
        return {
            "status": "ok" if self.is_loaded else "error",
            "version": self.model_version,
            "classifier_loaded": self.classifier is not None,
            "regressor_loaded": self.regressor is not None,
            "shap_explainer_ready": self.explainer is not None,
        }

model_manager = ModelManager.get_instance()
