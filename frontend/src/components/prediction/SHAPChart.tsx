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
      <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm p-6 text-center font-body-md text-body-md text-on-surface-variant">
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
    <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm p-6 md:p-8 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-outline-variant pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-secondary" />
            <h3 className="font-headline-sm text-headline-sm text-primary">Why This Prediction?</h3>
          </div>
          <p className="font-body-md text-body-md text-on-surface-variant mt-1">
            Local SHAP attributions describing top feature drivers pushing delay risk higher or lower
          </p>
        </div>

        <div className="flex items-center gap-4 font-label-sm text-label-sm">
          <div className="flex items-center gap-1.5 text-error">
            <span className="w-2.5 h-2.5 rounded-full bg-error inline-block"></span>
            <span>+ Increases Delay Risk</span>
          </div>
          <div className="flex items-center gap-1.5 text-secondary">
            <span className="w-2.5 h-2.5 rounded-full bg-secondary inline-block"></span>
            <span>- Mitigates Delay Risk</span>
          </div>
        </div>
      </div>

      {/* Summary Narrative Banner */}
      {summaryNarrative && (
        <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 font-body-md text-body-md text-on-surface leading-relaxed">
          <span className="font-bold text-primary block mb-1">Executive Explanation Summary:</span>
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
            <div key={idx} className="p-4 rounded-lg bg-surface-container-highest border border-outline-variant/50 hover:border-outline transition-colors">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-2">
                <div className="flex items-center gap-2">
                  {isPositive ? (
                    <TrendingUp className="w-4 h-4 text-error shrink-0" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-secondary shrink-0" />
                  )}
                  <span className="font-data-mono font-bold text-primary">
                    {item.feature_name}
                  </span>
                  {item.feature_group && (
                    <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-low text-on-surface-variant">
                      {item.feature_group}
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-3 font-data-mono font-bold">
                  <span className={isPositive ? 'text-error' : 'text-secondary'}>
                    {isPositive ? '+' : ''}{item.contribution.toFixed(4)}
                  </span>
                </div>
              </div>

              {/* Human-Readable Description */}
              {item.human_readable_description && (
                <p className="font-body-sm text-body-sm text-on-surface-variant mb-3 pl-6">
                  {item.human_readable_description}
                </p>
              )}

              {/* Progress Bar Visualization */}
              <div className="w-full bg-surface-container-low rounded-full h-2 overflow-hidden flex">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${
                    isPositive ? 'bg-error' : 'bg-secondary'
                  }`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Mandatory Governance Non-Causal Note */}
      <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 flex items-start gap-3 font-body-sm text-body-sm text-on-surface-variant mt-6">
        <Info className="w-4 h-4 text-secondary shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong className="text-on-surface">Non-Causal Governance Notice:</strong> These factors describe statistical model contribution and predictive association based on historical administrative data; they should not be interpreted as causal effects or judicial responsibility.
        </p>
      </div>
    </div>
  );
};
