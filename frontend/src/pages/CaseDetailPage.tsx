import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchCaseById } from '../api/cases';
import { CaseRecord } from '../types/case';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { RiskBadge } from '../components/common/RiskBadge';
import { formatDate, formatProbability } from '../utils/formatters';
import { ArrowLeft, Scale, Activity, Calendar, MapPin, User, FileText } from 'lucide-react';

export const CaseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [record, setRecord] = useState<CaseRecord | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadCase = async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCaseById(id);
      setRecord(data);
    } catch (err: any) {
      setError(err.message || 'Failed to retrieve case details from JDIS backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCase();
  }, [id]);

  if (loading) {
    return <LoadingState message="Loading case filing metadata..." />;
  }

  if (error || !record) {
    return <ErrorState message={error || 'Case record not found'} onRetry={loadCase} />;
  }

  const pred = record.latest_prediction;

  return (
    <div className="space-y-stack-md">
      <button
        onClick={() => navigate('/cases')}
        className="inline-flex items-center gap-2 font-label-md text-label-md text-secondary hover:text-primary bg-surface-container-low hover:bg-surface-container-high px-4 py-2 rounded-md transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Cases Repository</span>
      </button>

      <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm p-6 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-outline-variant pb-4">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="font-headline-md text-headline-md font-bold font-data-mono text-primary">
                Case #{record.ddl_case_id || record.id.substring(0, 8)}
              </h1>
              {pred && <RiskBadge band={pred.risk_band} score={pred.risk_score} showScore size="md" />}
            </div>
            <p className="font-body-md text-body-md text-on-surface-variant mt-1 capitalize">
              {record.type_name} ({record.case_category || 'Category N/A'}) • Filed on {formatDate(record.created_at)}
            </p>
          </div>
        </div>

        {pred && (
          <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 space-y-3">
            <div className="flex items-center justify-between font-label-md text-label-md">
              <span className="font-semibold text-secondary flex items-center gap-1.5">
                <Activity className="w-4 h-4" />
                <span>Latest Automated Delay Prediction</span>
              </span>
              <span className="text-on-surface-variant font-data-mono">{pred.model_version || 'v1.0-config-d'}</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center pt-1">
              <div className="p-3 rounded-md bg-surface-container-highest border border-outline-variant/50">
                <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block">Risk Score</span>
                <span className="text-xl font-bold font-data-mono text-primary">{pred.risk_score} / 100</span>
              </div>
              <div className="p-3 rounded-md bg-surface-container-highest border border-outline-variant/50">
                <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block">Risk Band</span>
                <div className="mt-1 flex justify-center"><RiskBadge band={pred.risk_band} size="sm" /></div>
              </div>
              <div className="p-3 rounded-md bg-surface-container-highest border border-outline-variant/50">
                <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block">Calibrated Prob.</span>
                <span className="text-sm font-bold font-data-mono text-secondary mt-1 block">
                  {formatProbability(pred.calibrated_probability)}
                </span>
              </div>
              <div className="p-3 rounded-md bg-surface-container-highest border border-outline-variant/50">
                <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider block">Evaluation Date</span>
                <span className="font-body-sm text-body-sm font-data-mono text-on-surface mt-1 block">
                  {formatDate(pred.created_at || record.created_at)}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
