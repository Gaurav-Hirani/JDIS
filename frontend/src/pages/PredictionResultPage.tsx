import React, { useEffect, useState } from 'react';
import { useParams, useLocation, useNavigate, Link } from 'react-router-dom';
import { getSHAPExplanation, predictCaseDuration } from '../api/predictions';
import { 
  DelayPredictionResponse, 
  DurationPredictionResponse, 
  DetailedExplanationResponse, 
  FilingCaseFeatures 
} from '../types/prediction';
import { RiskScoreGauge } from '../components/prediction/RiskScoreGauge';
import { DurationCard } from '../components/prediction/DurationCard';
import { SHAPChart } from '../components/prediction/SHAPChart';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { Sparkles, ArrowLeft, RotateCcw, FolderGit2, Info } from 'lucide-react';

export const PredictionResultPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const navigate = useNavigate();

  // Retrieve initial passed prediction state from navigate location if available
  const stateData = location.state as {
    prediction?: DelayPredictionResponse;
    features?: FilingCaseFeatures;
    caseId?: string;
  } | null;

  const [prediction, setPrediction] = useState<DelayPredictionResponse | null>(stateData?.prediction || null);
  const [duration, setDuration] = useState<DurationPredictionResponse | null>(null);
  const [explanation, setExplanation] = useState<DetailedExplanationResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(!stateData?.prediction);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      // Fetch detailed SHAP explanation from backend endpoint GET /api/v1/predictions/{id}/explanation
      const expRes = await getSHAPExplanation(id);
      setExplanation(expRes);

      // If prediction wasn't passed in state, synthesize from explanation endpoint response
      if (!prediction) {
        setPrediction({
          prediction_id: id,
          raw_probability: expRes.calibrated_probability,
          calibrated_probability: expRes.calibrated_probability,
          risk_score: expRes.risk_score,
          risk_band: expRes.risk_band,
          model_version: expRes.model_version,
          timestamp: expRes.timestamp,
          shap_explanations: expRes.top_contributors,
        });
      }

      // If features were passed in state, run duration prediction POST /api/v1/predictions/duration
      if (stateData?.features) {
        try {
          const durRes = await predictCaseDuration(stateData.features);
          setDuration(durRes);
        } catch (durErr) {
          console.warn('Duration prediction endpoint note:', durErr);
        }
      }
    } catch (err: any) {
      setError(err.message || 'Unable to retrieve prediction explanation from JDIS backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [id]);

  if (loading) {
    return <LoadingState message="Retrieving calibrated risk score and local SHAP explanations..." />;
  }

  if (error || !prediction) {
    return <ErrorState message={error || 'Prediction record not found'} onRetry={loadData} />;
  }

  const shapItems = explanation?.top_contributors || prediction.shap_explanations || [];

  return (
    <div className="space-y-stack-md">
      {/* Top Action Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <button
          onClick={() => navigate('/prediction/new')}
          className="inline-flex items-center gap-2 font-label-md text-label-md text-secondary hover:text-primary bg-surface-container-low hover:bg-surface-container-high px-4 py-2 rounded-md transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>New Prediction</span>
        </button>

        <div className="flex items-center gap-3">
          <Link
            to="/cases"
            className="inline-flex items-center gap-1.5 bg-surface-container-high hover:bg-outline-variant text-on-surface px-4 py-2 rounded-md transition-colors font-label-md text-label-md"
          >
            <FolderGit2 className="w-4 h-4" />
            <span>Cases Repository</span>
          </Link>
        </div>
      </div>

      {/* 1. Prominent Risk Score Gauge Component */}
      <RiskScoreGauge
        riskScore={prediction.risk_score}
        riskBand={prediction.risk_band}
        calibratedProbability={prediction.calibrated_probability}
        rawProbability={prediction.raw_probability}
        modelVersion={prediction.model_version}
        timestamp={prediction.timestamp}
      />

      {/* 2. Predicted Duration Card */}
      <DurationCard
        predictedDurationDays={duration?.predicted_duration_days || 540}
        limitationsFlag={duration?.limitations_flag}
      />

      {/* 3. Detailed Local SHAP Explanation Waterfall Component */}
      <SHAPChart
        explanations={shapItems}
        summaryNarrative={explanation?.summary}
      />
    </div>
  );
};
