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
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-surface/80 backdrop-blur-sm">
      <div className="bg-surface-container-lowest border border-outline-variant/50 w-full max-w-3xl max-h-[90vh] overflow-y-auto p-6 space-y-6 shadow-md rounded-lg">
        {/* Modal Header */}
        <div className="flex items-start justify-between border-b border-outline-variant pb-4">
          <div>
            <div className="flex items-center gap-3">
              <h2 className="font-headline-sm text-headline-sm text-primary font-bold font-data-mono">
                Case #{record.ddl_case_id || record.id.substring(0, 8)}
              </h2>
              {pred && <RiskBadge band={pred.risk_band} score={pred.risk_score} showScore size="sm" />}
            </div>
            <p className="font-body-md text-body-md text-on-surface-variant mt-1 capitalize">
              {record.type_name} ({record.case_category || 'Category N/A'}) • Filed on {formatDate(record.created_at)}
            </p>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-md text-on-surface-variant hover:text-on-surface bg-surface-container-low hover:bg-surface-container-high transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Prediction Summary Section */}
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

        {/* Feature Attributes Grid */}
        <div className="space-y-4">
          <h3 className="font-label-md text-label-md font-semibold uppercase tracking-wider text-on-surface-variant">
            Filing Stage Metadata (29 Config D Features)
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 font-body-sm text-body-sm">
            <div className="p-3 rounded-md bg-surface-container-low border border-outline-variant/50">
              <span className="text-on-surface-variant block font-label-sm text-label-sm uppercase font-semibold">State / District / Court</span>
              <span className="text-on-surface font-medium block mt-0.5">{record.state_str} ({record.state_code})</span>
              <span className="text-on-surface-variant block">{record.district_str} ({record.dist_code})</span>
              <span className="text-on-surface-variant block">{record.court_str} (#{record.court_no})</span>
            </div>

            <div className="p-3 rounded-md bg-surface-container-low border border-outline-variant/50">
              <span className="text-on-surface-variant block font-label-sm text-label-sm uppercase font-semibold">Statutory Provisions</span>
              <span className="text-on-surface font-medium block mt-0.5">Acts: {record.statutory_act_count ?? 1}</span>
              <span className="text-on-surface-variant block">IPC Sections: {record.ipc_section_count ?? 0}</span>
              <span className="text-on-surface-variant block capitalize">Bailable: {record.bailable_ipc_flag || 'N/A'}</span>
            </div>

            <div className="p-3 rounded-md bg-surface-container-low border border-outline-variant/50">
              <span className="text-on-surface-variant block font-label-sm text-label-sm uppercase font-semibold">Filing Judge</span>
              <span className="text-on-surface font-data-mono block mt-0.5">{record.ddl_filing_judge_id || 'N/A'}</span>
              <span className="text-on-surface-variant block capitalize">Pos: {record.judge_position_clean || 'Magistrate'}</span>
              <span className="text-on-surface-variant block">Tenure: {record.judge_tenure_days ?? 0} days</span>
            </div>

            <div className="p-3 rounded-md bg-surface-container-low border border-outline-variant/50">
              <span className="text-on-surface-variant block font-label-sm text-label-sm uppercase font-semibold">Prior Delay Metrics</span>
              <span className="text-on-surface font-data-mono block mt-0.5">
                Court Delay: {formatProbability(record.court_prior_delay_rate)}
              </span>
              <span className="text-on-surface-variant font-data-mono block">
                Type Delay: {formatProbability(record.casetype_prior_delay_rate)}
              </span>
            </div>

            <div className="p-3 rounded-md bg-surface-container-low border border-outline-variant/50">
              <span className="text-on-surface-variant block font-label-sm text-label-sm uppercase font-semibold">Court Backlog</span>
              <span className="text-on-surface font-data-mono block mt-0.5">
                Active Backlog: {record.court_prior_active_backlog ?? 'N/A'}
              </span>
              <span className="text-on-surface-variant font-data-mono block">
                Avg Duration: {record.court_prior_avg_duration ?? 'N/A'} days
              </span>
            </div>

            <div className="p-3 rounded-md bg-surface-container-low border border-outline-variant/50">
              <span className="text-on-surface-variant block font-label-sm text-label-sm uppercase font-semibold">Demographics</span>
              <span className="text-on-surface block mt-0.5">
                Female Defendant: {record.female_defendant_clean === '1' ? 'Yes' : 'No'}
              </span>
              <span className="text-on-surface-variant block">
                Female Counsel: {record.female_adv_def_clean === '1' ? 'Yes' : 'No'}
              </span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-outline-variant pt-4 flex justify-end">
          <button
            onClick={onClose}
            className="bg-surface-container-high hover:bg-outline-variant text-on-surface font-label-md text-label-md font-semibold px-4 py-2 rounded-md transition-colors"
          >
            Close Detail View
          </button>
        </div>
      </div>
    </div>
  );
};
