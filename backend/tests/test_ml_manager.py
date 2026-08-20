from backend.app.ml.manager import model_manager

def test_model_manager_loaded():
    assert model_manager.is_loaded is True
    assert model_manager.classifier is not None
    assert model_manager.regressor is not None
    assert model_manager.explainer is not None

def test_model_manager_health():
    health = model_manager.get_health_status()
    assert health["status"] == "ok"
    assert health["classifier_loaded"] is True
    assert health["regressor_loaded"] is True
    assert health["shap_explainer_ready"] is True
