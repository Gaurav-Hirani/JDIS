import React from 'react';
import { formatDurationDays } from '../../utils/formatters';
import { AlertTriangle, Clock } from 'lucide-react';

interface DurationCardProps {
  predictedDurationDays?: number;
  limitationsFlag?: string;
}

export const DurationCard: React.FC<DurationCardProps> = ({
  predictedDurationDays,
  limitationsFlag = 'Systematically underpredicts extreme outliers (>5 years). Associational estimate only.',
}) => {
  return (
    <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm p-6 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-secondary-container text-on-secondary-container rounded-lg border border-secondary/30 shrink-0">
            <Clock className="w-5 h-5 text-secondary" />
          </div>
          <div>
            <h3 className="font-headline-sm text-headline-sm text-primary">Predicted Case Duration</h3>
            <p className="font-body-md text-body-md text-on-surface-variant">Estimated expected total days from filing to initial resolution</p>
          </div>
        </div>

        <div className="text-right">
          <div className="text-2xl font-bold font-data-mono text-secondary">
            {formatDurationDays(predictedDurationDays)}
          </div>
        </div>
      </div>

      {limitationsFlag && (
        <div className="flex items-start gap-2.5 font-label-md text-label-md text-error bg-error-container p-3 rounded-lg border border-error/20 mt-4">
          <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
          <div className="leading-relaxed text-on-error-container">
            <span className="font-bold block mb-0.5">Model Limitation Notice:</span>
            {limitationsFlag} Case duration estimates are non-causal statistical associations subject to long-tail variance.
          </div>
        </div>
      )}
    </div>
  );
};
