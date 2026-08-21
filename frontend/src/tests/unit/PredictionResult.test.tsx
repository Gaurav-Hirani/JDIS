import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { RiskScoreGauge } from '../../components/prediction/RiskScoreGauge';
import { SHAPChart } from '../../components/prediction/SHAPChart';
import { DurationCard } from '../../components/prediction/DurationCard';

describe('Prediction Result & Explanation UI Components', () => {
  it('should render RiskScoreGauge with score, band, and calibrated probability (Case A)', () => {
    render(
      <RiskScoreGauge
        riskScore={81}
        riskBand="Very High"
        calibratedProbability={0.8129}
        rawProbability={0.8494}
        modelVersion="v1.0-config-d"
      />
    );

    expect(screen.getByText('81')).toBeInTheDocument();
    expect(screen.getAllByText('Very High').length).toBeGreaterThan(0);
    expect(screen.getByText('81.29%')).toBeInTheDocument();
    expect(screen.getByText('84.94%')).toBeInTheDocument();
  });

  it('should render RiskScoreGauge with score, band, and calibrated probability (Case B)', () => {
    render(
      <RiskScoreGauge
        riskScore={45}
        riskBand="Moderate"
        calibratedProbability={0.4500}
        rawProbability={0.5000}
        modelVersion="v1.0-config-d"
      />
    );

    expect(screen.getByText('45')).toBeInTheDocument();
    expect(screen.getAllByText('Moderate').length).toBeGreaterThan(0);
    expect(screen.getByText('45.00%')).toBeInTheDocument();
    expect(screen.getByText('50.00%')).toBeInTheDocument();
  });

  it('should render DurationCard with predicted duration and limitation notice', () => {
    render(
      <DurationCard
        predictedDurationDays={540}
        limitationsFlag="Systematically underpredicts extreme outliers (>5 years)."
      />
    );

    expect(screen.getByText(/540 days/)).toBeInTheDocument();
    expect(screen.getByText(/Model Limitation Notice:/)).toBeInTheDocument();
  });

  it('should render SHAPChart with human-readable feature descriptions and non-causal governance disclaimer', () => {
    const mockShapItems = [
      {
        feature_name: 'type_name',
        contribution: 2.0657,
        direction: 'positive' as const,
        feature_group: 'Basic Case',
        human_readable_description: 'Granular case type identifier',
      },
      {
        feature_name: 'ddl_filing_judge_id',
        contribution: -1.0135,
        direction: 'negative' as const,
        feature_group: 'Judge Attributes',
        human_readable_description: 'Filing judge historical assignment ID',
      },
    ];

    render(
      <SHAPChart
        explanations={mockShapItems}
        summaryNarrative="Primary drivers push delay risk higher."
      />
    );

    expect(screen.getByText('Why This Prediction?')).toBeInTheDocument();
    expect(screen.getByText('type_name')).toBeInTheDocument();
    expect(screen.getByText('Granular case type identifier')).toBeInTheDocument();
    expect(screen.getByText('ddl_filing_judge_id')).toBeInTheDocument();
    expect(screen.getByText(/Non-Causal Governance Notice:/)).toBeInTheDocument();
  });
});
