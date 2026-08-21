import React from 'react';
import { RiskBand } from '../../types/prediction';
import { RiskBadge } from '../common/RiskBadge';
import { getRiskTheme } from '../../utils/risk';
import { formatProbability } from '../../utils/formatters';
import { Info } from 'lucide-react';

interface RiskScoreGaugeProps {
  riskScore: number; // 0..100
  riskBand: RiskBand;
  calibratedProbability: number; // 0.0..1.0
  rawProbability?: number;
  modelVersion?: string;
  timestamp?: string;
}

export const RiskScoreGauge: React.FC<RiskScoreGaugeProps> = ({
  riskScore,
  riskBand,
  calibratedProbability,
  rawProbability,
  modelVersion = 'v1.0-config-d',
  timestamp,
}) => {
  const theme = getRiskTheme(riskBand);
  // Calculate SVG arc stroke offset for circular gauge
  const radius = 68;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (riskScore / 100) * circumference;

  return (
    <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-8">
      {/* Gauge Circular Visualizer */}
      <div className="relative flex flex-col items-center justify-center shrink-0">
        <svg className="w-44 h-44 transform -rotate-90">
          <circle
            cx="88"
            cy="88"
            r={radius}
            stroke="currentColor"
            strokeWidth="12"
            fill="transparent"
            className="text-surface-container-highest"
          />
          <circle
            cx="88"
            cy="88"
            r={radius}
            stroke={theme.hex}
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-extrabold text-primary font-data-mono tracking-tight">{riskScore}</span>
          <span className="text-[10px] uppercase font-bold tracking-widest text-on-surface-variant mt-0.5">/ 100</span>
          <div className="mt-2">
            <RiskBadge band={riskBand} size="sm" />
          </div>
        </div>
      </div>

      {/* KPI Details */}
      <div className="flex-1 space-y-4 text-center md:text-left">
        <div>
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-2 mb-1">
            <h2 className="font-headline-md text-headline-md text-primary font-bold">JDIS Risk Score</h2>
            <RiskBadge band={riskBand} size="md" />
          </div>
          <p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">
            Filing-stage delay risk score computed via empirical Isotonic probability calibration
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 rounded-xl bg-surface-container-low border border-outline-variant/50">
          {rawProbability !== undefined && (
            <div>
              <span className="font-label-sm text-label-sm font-semibold text-on-surface-variant uppercase tracking-wider block">
                Raw Model Probability
              </span>
              <span className="text-xl font-bold font-data-mono text-primary">
                {formatProbability(rawProbability)}
              </span>
              <span className="font-label-sm text-label-sm text-outline block mt-0.5">Direct XGBoost output</span>
            </div>
          )}

          <div>
            <span className="font-label-sm text-label-sm font-semibold text-on-surface-variant uppercase tracking-wider block">
              Calibrated Delay Probability
            </span>
            <span className={`text-xl font-bold font-data-mono ${theme.textClass}`}>
              {formatProbability(calibratedProbability)}
            </span>
            <span className="font-label-sm text-label-sm text-outline block mt-0.5">Isotonic mapped (&gt;24 mo)</span>
          </div>
        </div>

        <div className="space-y-2">
          <p className="font-label-sm text-label-sm text-on-surface-variant leading-relaxed px-1">
            Raw probability is the direct XGBoost model output. Calibrated probability is the probability after isotonic calibration and is used for the JDIS Risk Score.
          </p>

          <div className="flex items-start gap-2 font-label-sm text-label-sm text-on-surface-variant bg-surface-container-low p-3 rounded-lg border border-outline-variant/30">
            <Info className="w-4 h-4 text-secondary shrink-0 mt-0.5" />
            <div className="space-y-1.5">
              <p>
                The JDIS Risk Score is calculated deterministically as <code className="font-data-mono font-bold text-secondary">floor(calibrated_probability * 100)</code> per research specifications.
              </p>
              <p>
                Different raw model probabilities may map to the same calibrated probability because the production calibrator uses a monotonic stepwise mapping.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
