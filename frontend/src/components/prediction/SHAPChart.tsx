import React from 'react';
import { SHAPExplanationItem } from '../../types/prediction';
import { HelpCircle, TrendingUp, TrendingDown, Info, Sparkles } from 'lucide-react';

interface SHAPChartProps {
  explanations?: SHAPExplanationItem[];
  summaryNarrative?: string;
}

export const SHAPChart: React.FC<SHAPChartProps> = ({ explanations = [], summaryNarrative }) => {
  if (!explanations || explanations.length === 0) {
    return (
      <div className="card-glass p-6 text-center text-xs text-slate-400">
        No SHAP local attributions available for this prediction record.
      </div>
    );
  }

  // Sort by absolute contribution magnitude descending
  const sortedExplanations = [...explanations].sort(
    (a, b) => Math.abs(b.contribution) - Math.abs(a.contribution)
  );

  const maxMagnitude = Math.max(...sortedExplanations.map((item) => Math.abs(item.contribution)), 0.001);

  return (
    <div className="card-glass p-6 md:p-8 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-bold text-slate-100">Why This Prediction?</h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Local SHAP attributions describing top feature drivers pushing delay risk higher or lower
          </p>
        </div>

        <div className="flex items-center space-x-4 text-xs font-medium">
          <div className="flex items-center space-x-1.5 text-rose-400">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span>
            <span>+ Increases Delay Risk</span>
          </div>
          <div className="flex items-center space-x-1.5 text-blue-400">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block"></span>
            <span>- Mitigates Delay Risk</span>
          </div>
        </div>
      </div>

      {/* Summary Narrative Banner */}
      {summaryNarrative && (
        <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-300 leading-relaxed">
          <span className="font-semibold text-blue-300 block mb-1">Executive Explanation Summary:</span>
          {summaryNarrative}
        </div>
      )}

      {/* Horizontal Bar Breakdown List */}
      <div className="space-y-4">
        {sortedExplanations.map((item, idx) => {
          const isPositive = item.direction === 'positive' || item.contribution > 0;
          const magnitude = Math.abs(item.contribution);
          const percentage = Math.min((magnitude / maxMagnitude) * 100, 100);

          return (
            <div key={idx} className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/80 hover:border-slate-700 transition-colors">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-2">
                <div className="flex items-center space-x-2">
                  {isPositive ? (
                    <TrendingUp className="w-4 h-4 text-rose-400 shrink-0" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-blue-400 shrink-0" />
                  )}
                  <span className="text-xs font-bold text-slate-200 font-mono">
                    {item.feature_name}
                  </span>
                  {item.feature_group && (
                    <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-medium">
                      {item.feature_group}
                    </span>
                  )}
                </div>

                <div className="flex items-center space-x-3 text-xs font-mono">
                  <span className={isPositive ? 'text-rose-400 font-bold' : 'text-blue-400 font-bold'}>
                    {isPositive ? '+' : ''}{item.contribution.toFixed(4)}
                  </span>
                </div>
              </div>

              {/* Human-Readable Description */}
              {item.human_readable_description && (
                <p className="text-[11px] text-slate-400 mb-2 pl-6">
                  {item.human_readable_description}
                </p>
              )}

              {/* Progress Bar Visualization */}
              <div className="w-full bg-slate-850 rounded-full h-2 overflow-hidden flex">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    isPositive ? 'bg-gradient-to-r from-orange-500 to-rose-500' : 'bg-gradient-to-r from-cyan-500 to-blue-500'
                  }`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Mandatory Governance Non-Causal Note */}
      <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex items-start space-x-3 text-xs text-slate-400">
        <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong className="text-slate-300">Non-Causal Governance Notice:</strong> These factors describe statistical model contribution and predictive association based on historical administrative data; they should not be interpreted as causal effects or judicial responsibility.
        </p>
      </div>
    </div>
  );
};
