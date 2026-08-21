import React from 'react';
import { RiskBand } from '../../types/prediction';
import { RiskBadge } from '../common/RiskBadge';
import { getRiskTheme } from '../../utils/risk';
import { formatProbability } from '../../utils/formatters';
import { ShieldCheck, Info } from 'lucide-react';

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
    <div className="card-glass p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-8 border-slate-800">
      {/* Gauge Circular Visualizer */}
      <div className="relative flex flex-col items-center justify-center">
        <svg className="w-44 h-44 transform -rotate-90">
          <circle
            cx="88"
            cy="88"
            r={radius}
            stroke="currentColor"
            strokeWidth="12"
            fill="transparent"
            className="text-slate-800"
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
          <span className="text-4xl font-extrabold text-slate-100 font-mono tracking-tight">{riskScore}</span>
          <span className="text-[10px] uppercase font-bold tracking-widest text-slate-400 mt-0.5">/ 100</span>
          <div className="mt-2">
            <RiskBadge band={riskBand} size="sm" />
          </div>
        </div>
      </div>

      {/* KPI Details */}
      <div className="flex-1 space-y-4 text-center md:text-left">
        <div>
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-2 mb-1">
            <h2 className="text-xl font-bold text-slate-100">JDIS Risk Score</h2>
            <RiskBadge band={riskBand} size="md" />
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Filing-stage delay risk score computed via empirical Isotonic probability calibration
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 rounded-xl bg-slate-950/60 border border-slate-850">
          {rawProbability !== undefined && (
            <div>
              <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">
                Raw Model Probability
              </span>
              <span className="text-xl font-bold font-mono text-slate-300">
                {formatProbability(rawProbability)}
              </span>
              <span className="text-[10px] text-slate-500 block mt-0.5">Direct XGBoost output</span>
            </div>
          )}

          <div>
            <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">
              Calibrated Delay Probability
            </span>
            <span className={`text-xl font-bold font-mono ${theme.textClass}`}>
              {formatProbability(calibratedProbability)}
            </span>
            <span className="text-[10px] text-slate-500 block mt-0.5">Isotonic mapped (&gt;24 mo)</span>
          </div>
        </div>

        <div className="space-y-2">
          <p className="text-[11px] text-slate-400 leading-relaxed px-1">
            Raw probability is the direct XGBoost model output. Calibrated probability is the probability after isotonic calibration and is used for the JDIS Risk Score.
          </p>

          <div className="flex items-start space-x-2 text-[11px] text-slate-400 bg-slate-800/40 p-2.5 rounded-lg border border-slate-800">
            <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
            <div className="space-y-1.5">
              <p>
                The JDIS Risk Score is calculated deterministically as <code className="font-mono text-blue-300">floor(calibrated_probability * 100)</code> per research specifications.
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
