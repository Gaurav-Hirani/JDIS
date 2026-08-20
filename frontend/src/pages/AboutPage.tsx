import React from 'react';
import { BookOpenCheck, Scale, ShieldAlert, Cpu, AlertTriangle, CheckCircle2 } from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header Banner */}
      <div className="card-glass p-6 border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <BookOpenCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-100">Methodology & Governance Guide</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Judicial Delay Intelligence System (JDIS) research framework, calibration formula, and limitations
            </p>
          </div>
        </div>
      </div>

      {/* 1. Core System Purpose & Governance */}
      <div className="card-glass p-6 space-y-4">
        <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
          <Scale className="w-5 h-5 text-blue-400" />
          <h2 className="text-base font-bold text-slate-100">1. Product Positioning & System Purpose</h2>
        </div>

        <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
          <p>
            The <strong>Judicial Delay Intelligence System (JDIS)</strong> is an administrative decision-support platform engineered to quantify filing-stage delay risks in district court establishments.
          </p>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <span className="font-semibold text-rose-300 block text-xs uppercase tracking-wider">
              Governance Directive & Explicit Boundaries
            </span>
            <ul className="list-disc list-inside space-y-1.5 text-slate-300">
              <li><strong>Decision-Support Only:</strong> JDIS is strictly an administrative decision-support system. It is <strong>NOT</strong> a legal decision-maker, judge replacement, or outcome guarantee.</li>
              <li><strong>Associational Risk Language:</strong> All scores and metrics convey statistical probability of severe delay (&gt;24 months) based on historical administrative metadata.</li>
              <li><strong>No Causal Attribution:</strong> SHAP values explain statistical model attributions, <strong>NOT</strong> causal effects or judicial responsibility.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* 2. JDIS Risk Score Formula & Calibration */}
      <div className="card-glass p-6 space-y-4">
        <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
          <Cpu className="w-5 h-5 text-amber-400" />
          <h2 className="text-base font-bold text-slate-100">2. JDIS Risk Score Formula & Calibration</h2>
        </div>

        <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
          <p>
            The primary classification model consists of an <strong>XGBoost Classifier</strong> trained on filing-time metadata (2010–2014) and calibrated using an <strong>Isotonic Regression</strong> wrapper fitted on out-of-sample validation data (2015).
          </p>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-center space-y-1">
            <span className="text-slate-400 text-[11px] block uppercase font-semibold">Exact Authoritative Risk Formula</span>
            <div className="text-lg font-bold text-blue-300">
              JDIS Risk Score = floor( calibrated_probability × 100 )
            </div>
            <span className="text-[10px] text-slate-500 block">Authoritative integer score bounded strictly between 0 and 100</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
            <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-center">
              <span className="text-xs font-bold text-emerald-400 block">Low Risk</span>
              <span className="text-sm font-mono font-bold text-slate-200 block mt-1">0 – 20 Score</span>
              <span className="text-[10px] text-slate-400 block mt-0.5">Minimal delay likelihood</span>
            </div>

            <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 text-center">
              <span className="text-xs font-bold text-amber-400 block">Moderate Risk</span>
              <span className="text-sm font-mono font-bold text-slate-200 block mt-1">21 – 50 Score</span>
              <span className="text-[10px] text-slate-400 block mt-0.5">Average disposal timeline</span>
            </div>

            <div className="p-3 rounded-lg bg-orange-500/10 border border-orange-500/30 text-center">
              <span className="text-xs font-bold text-orange-400 block">High Risk</span>
              <span className="text-sm font-mono font-bold text-slate-200 block mt-1">51 – 80 Score</span>
              <span className="text-[10px] text-slate-400 block mt-0.5">Elevated delay probability</span>
            </div>

            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-center">
              <span className="text-xs font-bold text-rose-400 block">Very High Risk</span>
              <span className="text-sm font-mono font-bold text-slate-200 block mt-1">81 – 100 Score</span>
              <span className="text-[10px] text-slate-400 block mt-0.5">Severe delay probability (&gt;2 yrs)</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. SHAP Explainability & Non-Causal Principles */}
      <div className="card-glass p-6 space-y-4">
        <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <h2 className="text-base font-bold text-slate-100">3. SHAP Explainability & Attribution Rules</h2>
        </div>

        <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
          <p>
            Local case explanations are calculated via <code>shap.TreeExplainer</code> across transformed feature space and mapped to conceptual parent groups (e.g. Case Type, Judicial Attributes, Geography).
          </p>
          <p className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 text-slate-300">
            <strong>Key Guideline:</strong> If a specific judge ID or court establishment exhibits a high SHAP value, it indicates that cases assigned to that historical jurisdiction have statistically experienced longer durations; it does <strong>NOT</strong> prove individual judge culpability or administrative fault.
          </p>
        </div>
      </div>

      {/* 4. Model Limitations & Research Findings */}
      <div className="card-glass p-6 space-y-4">
        <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
          <AlertTriangle className="w-5 h-5 text-rose-400" />
          <h2 className="text-base font-bold text-slate-100">4. Known System Limitations & Dataset C Research Finding</h2>
        </div>

        <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
          <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-900/40 text-rose-200 space-y-2">
            <span className="font-semibold block text-xs uppercase tracking-wider">Duration Regression Variance Compression</span>
            <p className="text-slate-300">
              The duration regressor model systematically underpredicts long-tail extreme outliers (&gt;5 years) due to mean squared error variance compression. Estimates provide general baseline guidance only.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <span className="font-semibold text-slate-200 block text-xs uppercase tracking-wider">
              Dataset C (Next-Listing Delay) Research Negative Result
            </span>
            <p className="text-slate-400">
              Research experiment Dataset C evaluated predicting daily hearing gap intervals. Out-of-time evaluation yielded a negative coefficient of determination ($R^2 = -1.7032$). Micro-temporal scheduling cannot be consistently predicted from administrative metadata. Consequently, Dataset C is <strong>strictly excluded</strong> from production UI workflows.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
