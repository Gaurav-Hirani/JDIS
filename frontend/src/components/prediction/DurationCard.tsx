import React from 'react';
import { formatDurationDays } from '../../utils/formatters';
import { Calendar, AlertTriangle, Clock } from 'lucide-react';

interface DurationCardProps {
  predictedDurationDays?: number;
  limitationsFlag?: string;
}

export const DurationCard: React.FC<DurationCardProps> = ({
  predictedDurationDays,
  limitationsFlag = 'Systematically underpredicts extreme outliers (>5 years). Associational estimate only.',
}) => {
  return (
    <div className="card-glass p-6 border-slate-800 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-600/20 text-indigo-400 rounded-lg border border-indigo-500/30">
            <Clock className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-200">Predicted Case Duration</h3>
            <p className="text-xs text-slate-400">Estimated expected total days from filing to initial resolution</p>
          </div>
        </div>

        <div className="text-right">
          <div className="text-2xl font-bold font-mono text-indigo-300">
            {formatDurationDays(predictedDurationDays)}
          </div>
        </div>
      </div>

      {limitationsFlag && (
        <div className="flex items-start space-x-2.5 text-xs text-amber-300/90 bg-amber-950/30 p-3 rounded-lg border border-amber-800/50">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <span className="font-semibold block text-amber-200">Model Limitation Notice:</span>
            {limitationsFlag} Case duration estimates are non-causal statistical associations subject to long-tail variance.
          </div>
        </div>
      )}
    </div>
  );
};
