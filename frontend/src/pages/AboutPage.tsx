import React from 'react';
import { BookOpenCheck, Scale, ShieldAlert, Cpu, AlertTriangle, CheckCircle2 } from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-stack-md max-w-4xl mx-auto">
      {/* Header Banner */}
      <div className="bg-surface-container-lowest border border-outline-variant/50 p-6 rounded-lg shadow-sm">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-primary-container text-on-primary-container rounded-lg border border-primary/20 shrink-0">
            <BookOpenCheck className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h1 className="font-headline-sm text-headline-sm font-bold text-primary">Methodology & Governance Guide</h1>
            <p className="font-body-md text-body-md text-on-surface-variant mt-1">
              Judicial Delay Intelligence System (JDIS) research framework, calibration formula, and limitations
            </p>
          </div>
        </div>
      </div>

      {/* 1. Core System Purpose & Governance */}
      <div className="bg-surface-container-lowest border border-outline-variant/50 p-6 rounded-lg shadow-sm space-y-4">
        <div className="flex items-center gap-2 border-b border-outline-variant pb-3">
          <Scale className="w-5 h-5 text-secondary" />
          <h2 className="font-headline-sm text-headline-sm font-bold text-primary">1. Product Positioning & System Purpose</h2>
        </div>

        <div className="space-y-3 font-body-md text-body-md text-on-surface leading-relaxed">
          <p>
            The <strong>Judicial Delay Intelligence System (JDIS)</strong> is an administrative decision-support platform engineered to quantify filing-stage delay risks in district court establishments.
          </p>

          <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 space-y-2">
            <span className="font-label-sm text-label-sm font-semibold text-error block uppercase tracking-wider">
              Governance Directive & Explicit Boundaries
            </span>
            <ul className="list-disc list-inside space-y-1.5 text-on-surface-variant">
              <li><strong>Decision-Support Only:</strong> JDIS is strictly an administrative decision-support system. It is <strong>NOT</strong> a legal decision-maker, judge replacement, or outcome guarantee.</li>
              <li><strong>Associational Risk Language:</strong> All scores and metrics convey statistical probability of severe delay (&gt;24 months) based on historical administrative metadata.</li>
              <li><strong>No Causal Attribution:</strong> SHAP values explain statistical model attributions, <strong>NOT</strong> causal effects or judicial responsibility.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* 2. JDIS Risk Score Formula & Calibration */}
      <div className="bg-surface-container-lowest border border-outline-variant/50 p-6 rounded-lg shadow-sm space-y-4">
        <div className="flex items-center gap-2 border-b border-outline-variant pb-3">
          <Cpu className="w-5 h-5 text-tertiary" />
          <h2 className="font-headline-sm text-headline-sm font-bold text-primary">2. JDIS Risk Score Formula & Calibration</h2>
        </div>

        <div className="space-y-3 font-body-md text-body-md text-on-surface leading-relaxed">
          <p>
            The primary classification model consists of an <strong>XGBoost Classifier</strong> trained on filing-time metadata (2010–2014) and calibrated using an <strong>Isotonic Regression</strong> wrapper fitted on out-of-sample validation data (2015).
          </p>

          <div className="p-4 rounded-lg bg-surface-container-highest border border-outline-variant text-center space-y-1">
            <span className="text-on-surface-variant font-label-sm text-label-sm block uppercase font-semibold">Exact Authoritative Risk Formula</span>
            <div className="text-lg font-bold font-data-mono text-secondary">
              JDIS Risk Score = floor( calibrated_probability × 100 )
            </div>
            <span className="font-body-sm text-body-sm text-outline block">Authoritative integer score bounded strictly between 0 and 100</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
            <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 text-center">
              <span className="font-label-md text-label-md font-bold text-[#10b981] block">Low Risk</span>
              <span className="font-body-md text-body-md font-data-mono font-bold text-on-surface block mt-1">0 – 20 Score</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant block mt-0.5">Minimal delay likelihood</span>
            </div>

            <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 text-center">
              <span className="font-label-md text-label-md font-bold text-[#f59e0b] block">Moderate Risk</span>
              <span className="font-body-md text-body-md font-data-mono font-bold text-on-surface block mt-1">21 – 50 Score</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant block mt-0.5">Average disposal timeline</span>
            </div>

            <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 text-center">
              <span className="font-label-md text-label-md font-bold text-[#f97316] block">High Risk</span>
              <span className="font-body-md text-body-md font-data-mono font-bold text-on-surface block mt-1">51 – 80 Score</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant block mt-0.5">Elevated delay probability</span>
            </div>

            <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 text-center">
              <span className="font-label-md text-label-md font-bold text-error block">Very High Risk</span>
              <span className="font-body-md text-body-md font-data-mono font-bold text-on-surface block mt-1">81 – 100 Score</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant block mt-0.5">Severe delay probability (&gt;2 yrs)</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. SHAP Explainability & Non-Causal Principles */}
      <div className="bg-surface-container-lowest border border-outline-variant/50 p-6 rounded-lg shadow-sm space-y-4">
        <div className="flex items-center gap-2 border-b border-outline-variant pb-3">
          <CheckCircle2 className="w-5 h-5 text-secondary" />
          <h2 className="font-headline-sm text-headline-sm font-bold text-primary">3. SHAP Explainability & Attribution Rules</h2>
        </div>

        <div className="space-y-3 font-body-md text-body-md text-on-surface leading-relaxed">
          <p>
            Local case explanations are calculated via <code className="font-data-mono bg-surface-container-highest px-1 py-0.5 rounded">shap.TreeExplainer</code> across transformed feature space and mapped to conceptual parent groups (e.g. Case Type, Judicial Attributes, Geography).
          </p>
          <p className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 text-on-surface-variant">
            <strong className="text-on-surface">Key Guideline:</strong> If a specific judge ID or court establishment exhibits a high SHAP value, it indicates that cases assigned to that historical jurisdiction have statistically experienced longer durations; it does <strong>NOT</strong> prove individual judge culpability or administrative fault.
          </p>
        </div>
      </div>

      {/* 4. Model Limitations & Research Findings */}
      <div className="bg-surface-container-lowest border border-outline-variant/50 p-6 rounded-lg shadow-sm space-y-4">
        <div className="flex items-center gap-2 border-b border-outline-variant pb-3">
          <AlertTriangle className="w-5 h-5 text-error" />
          <h2 className="font-headline-sm text-headline-sm font-bold text-primary">4. Known System Limitations & Dataset C Research Finding</h2>
        </div>

        <div className="space-y-3 font-body-md text-body-md text-on-surface leading-relaxed">
          <div className="p-4 rounded-lg bg-error-container border border-error/30 text-on-error-container space-y-2">
            <span className="font-label-sm text-label-sm font-semibold block uppercase tracking-wider">Duration Regression Variance Compression</span>
            <p>
              The duration regressor model systematically underpredicts long-tail extreme outliers (&gt;5 years) due to mean squared error variance compression. Estimates provide general baseline guidance only.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 space-y-2">
            <span className="font-label-sm text-label-sm font-semibold text-primary block uppercase tracking-wider">
              Dataset C (Next-Listing Delay) Research Negative Result
            </span>
            <p className="text-on-surface-variant">
              Research experiment Dataset C evaluated predicting daily hearing gap intervals. Out-of-time evaluation yielded a negative coefficient of determination ($R^2 = -1.7032$). Micro-temporal scheduling cannot be consistently predicted from administrative metadata. Consequently, Dataset C is <strong className="text-on-surface">strictly excluded</strong> from production UI workflows.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
