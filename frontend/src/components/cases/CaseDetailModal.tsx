import React from 'react';
import { CaseRecord } from '../../types/case';
import { RiskBadge } from '../common/RiskBadge';
import { formatDate, formatProbability } from '../../utils/formatters';
import { X, Calendar, MapPin, Scale, User, FileText, Activity } from 'lucide-react';

interface CaseDetailModalProps {
  record: CaseRecord | null;
  onClose: () => void;
}

export const CaseDetailModal: React.FC<CaseDetailModalProps> = ({ record, onClose }) => {
  if (!record) return null;

  const pred = record.latest_prediction;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
      <div className="card-glass w-full max-w-3xl max-h-[90vh] overflow-y-auto p-6 space-y-6 border-slate-700 shadow-2xl">
        {/* Modal Header */}
        <div className="flex items-start justify-between border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center space-x-3">
              <h2 className="text-xl font-bold text-slate-100 font-mono">
                Case #{record.ddl_case_id || record.id.substring(0, 8)}
              </h2>
              {pred && <RiskBadge band={pred.risk_band} score={pred.risk_score} showScore size="sm" />}
            </div>
            <p className="text-xs text-slate-400 mt-1 capitalize">
              {record.type_name} ({record.case_category || 'Category N/A'}) • Filed on {formatDate(record.created_at)}
            </p>
          </div>

          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Prediction Summary Section */}
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

        {/* Feature Attributes Grid */}
        <div className="space-y-4">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Filing Stage Metadata (29 Config D Features)
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-xs">
            <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">State / District / Court</span>
              <span className="text-slate-200 font-medium block mt-0.5">{record.state_str} ({record.state_code})</span>
              <span className="text-slate-400 block">{record.district_str} ({record.dist_code})</span>
              <span className="text-slate-400 block">{record.court_str} (#{record.court_no})</span>
            </div>

            <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">Statutory Provisions</span>
              <span className="text-slate-200 font-medium block mt-0.5">Acts: {record.statutory_act_count ?? 1}</span>
              <span className="text-slate-400 block">IPC Sections: {record.ipc_section_count ?? 0}</span>
              <span className="text-slate-400 block capitalize">Bailable: {record.bailable_ipc_flag || 'N/A'}</span>
            </div>

            <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">Filing Judge</span>
              <span className="text-slate-200 font-mono block mt-0.5">{record.ddl_filing_judge_id || 'N/A'}</span>
              <span className="text-slate-400 block capitalize">Pos: {record.judge_position_clean || 'Magistrate'}</span>
              <span className="text-slate-400 block">Tenure: {record.judge_tenure_days ?? 0} days</span>
            </div>

            <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">Prior Delay Metrics</span>
              <span className="text-slate-200 font-mono block mt-0.5">
                Court Delay: {formatProbability(record.court_prior_delay_rate)}
              </span>
              <span className="text-slate-400 font-mono block">
                Type Delay: {formatProbability(record.casetype_prior_delay_rate)}
              </span>
            </div>

            <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">Court Backlog</span>
              <span className="text-slate-200 font-mono block mt-0.5">
                Active Backlog: {record.court_prior_active_backlog ?? 'N/A'}
              </span>
              <span className="text-slate-400 font-mono block">
                Avg Duration: {record.court_prior_avg_duration ?? 'N/A'} days
              </span>
            </div>

            <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase font-semibold">Demographics</span>
              <span className="text-slate-200 block mt-0.5">
                Female Defendant: {record.female_defendant_clean === '1' ? 'Yes' : 'No'}
              </span>
              <span className="text-slate-400 block">
                Female Counsel: {record.female_adv_def_clean === '1' ? 'Yes' : 'No'}
              </span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-slate-800 pt-4 flex justify-end">
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-4 py-2 rounded-lg transition-colors"
          >
            Close Detail View
          </button>
        </div>
      </div>
    </div>
  );
};
