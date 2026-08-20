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
    <div className="space-y-6">
      <button
        onClick={() => navigate('/cases')}
        className="inline-flex items-center space-x-2 text-xs font-semibold text-slate-300 hover:text-white bg-slate-850 hover:bg-slate-800 px-3.5 py-2 rounded-lg border border-slate-700/60 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Cases Repository</span>
      </button>

      <div className="card-glass p-6 border-slate-800 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-bold font-mono text-slate-100">
                Case #{record.ddl_case_id || record.id.substring(0, 8)}
              </h1>
              {pred && <RiskBadge band={pred.risk_band} score={pred.risk_score} showScore size="md" />}
            </div>
            <p className="text-xs text-slate-400 mt-1 capitalize">
              {record.type_name} ({record.case_category || 'Category N/A'}) • Filed on {formatDate(record.created_at)}
            </p>
          </div>
        </div>

        {pred && (
          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-blue-400 flex items-center space-x-1.5">
                <Activity className="w-4 h-4" />
                <span>Latest Automated Delay Prediction</span>
              </span>
              <span className="text-slate-500 font-mono">{pred.model_version || 'v1.0-config-d'}</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center pt-1">
              <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Risk Score</span>
                <span className="text-xl font-bold font-mono text-slate-100">{pred.risk_score} / 100</span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Risk Band</span>
                <div className="mt-1"><RiskBadge band={pred.risk_band} size="sm" /></div>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Calibrated Prob.</span>
                <span className="text-sm font-bold font-mono text-blue-400 mt-1 block">
                  {formatProbability(pred.calibrated_probability)}
                </span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Evaluation Date</span>
                <span className="text-xs font-mono text-slate-300 mt-1 block">
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
