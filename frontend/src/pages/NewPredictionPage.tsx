import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { predictFilingDelay } from '../api/predictions';
import { createCaseRecord } from '../api/cases';
import { PredictionForm } from '../components/prediction/PredictionForm';
import { PredictionFormValues } from '../schemas/predictionSchema';
import { ErrorState } from '../components/common/ErrorState';
import { Sparkles, FileText, Scale } from 'lucide-react';

export const NewPredictionPage: React.FC = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (values: PredictionFormValues, saveAsCase: boolean) => {
    setIsSubmitting(true);
    setError(null);
    try {
      // Execute live POST /api/v1/predictions/delay
      const delayResult = await predictFilingDelay(values);

      let caseId = delayResult.case_id;

      // Save case record to DB if requested
      if (saveAsCase) {
        try {
          const caseRecord = await createCaseRecord({
            ...values,
            ddl_case_id: `case_${Math.floor(100000 + Math.random() * 900000)}`,
          });
          caseId = caseRecord.id;
        } catch (saveErr) {
          console.warn('Case persistence note:', saveErr);
        }
      }

      // Navigate to prediction result page with full payload in state for immediate render
      navigate(`/prediction/${delayResult.prediction_id}`, {
        state: {
          prediction: delayResult,
          features: values,
          caseId: caseId,
        },
      });
    } catch (err: any) {
      setError(err.message || 'Failed to submit prediction request to JDIS backend');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="card-glass p-6 border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-100">Filing Stage Case Risk Prediction</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Enter supported 29 filing-stage case metadata to evaluate delay probability and JDIS Risk Score
            </p>
          </div>
        </div>
      </div>

      {error && (
        <ErrorState
          title="Prediction Submission Failed"
          message={error}
          onRetry={() => setError(null)}
        />
      )}

      {/* 29-Feature Form */}
      <PredictionForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />
    </div>
  );
};
