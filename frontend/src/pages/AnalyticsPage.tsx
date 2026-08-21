import React, { useEffect, useState } from 'react';
import { 
  fetchAnalyticsSummary, 
  fetchRiskDistribution, 
  fetchCourtAnalytics, 
  fetchCaseTypeAnalytics 
} from '../api/analytics';
import { 
  AnalyticsSummary, 
  RiskDistributionItem, 
  CourtAnalyticsItem, 
  CaseTypeAnalyticsItem 
} from '../types/analytics';
import { StatCard } from '../components/common/StatCard';
import { RiskDistChart } from '../components/analytics/RiskDistChart';
import { CourtMetricsTable } from '../components/analytics/CourtMetricsTable';
import { CaseTypeBarChart } from '../components/analytics/CaseTypeBarChart';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { formatDurationDays } from '../utils/formatters';
import { BarChart3, FolderCheck, ShieldAlert, Activity, Clock, Info } from 'lucide-react';

export const AnalyticsPage: React.FC = () => {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [riskDist, setRiskDist] = useState<RiskDistributionItem[]>([]);
  const [courts, setCourts] = useState<CourtAnalyticsItem[]>([]);
  const [caseTypes, setCaseTypes] = useState<CaseTypeAnalyticsItem[]>([]);

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadAnalytics = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumRes, distRes, courtRes, typeRes] = await Promise.all([
        fetchAnalyticsSummary(),
        fetchRiskDistribution(),
        fetchCourtAnalytics(),
        fetchCaseTypeAnalytics(),
      ]);
      setSummary(sumRes);
      setRiskDist(distRes);
      setCourts(courtRes);
      setCaseTypes(typeRes);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch judicial analytics from JDIS backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (loading) {
    return <LoadingState message="Aggregating court throughput and delay risk analytics..." />;
  }

  if (error || !summary) {
    return <ErrorState message={error || 'Unable to load analytics'} onRetry={loadAnalytics} />;
  }

  return (
    <div className="space-y-stack-md">
      {/* Header Banner */}
      <div className="bg-surface-container-lowest border border-outline-variant/50 p-6 rounded-lg shadow-sm">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-primary-container text-on-primary-container rounded-lg shrink-0">
            <BarChart3 className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-headline-sm text-headline-sm text-primary font-bold">Judicial System Analytics</h1>
            <p className="font-body-md text-body-md text-on-surface-variant mt-1">
              Empirical administrative delay risk aggregation across courts, case types, and risk bands
            </p>
          </div>
        </div>
      </div>

      {/* Aggregate System KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Evaluated Cases"
          value={summary.total_cases}
          subtitle={`Total Predictions: ${summary.total_predictions}`}
          icon={FolderCheck}
          accentColor="text-secondary"
        />
        <StatCard
          title="High Risk Ratio"
          value={`${summary.high_risk_cases_percentage.toFixed(1)}%`}
          subtitle={`${summary.high_risk_cases_count} High/Very High cases`}
          icon={ShieldAlert}
          accentColor="text-error"
        />
        <StatCard
          title="Average Risk Score"
          value={`${summary.average_risk_score.toFixed(1)} / 100`}
          subtitle="System-wide empirical score"
          icon={Activity}
          accentColor="text-tertiary"
        />
        <StatCard
          title="Average Duration"
          value={formatDurationDays(summary.average_predicted_duration_days)}
          subtitle="Estimated time to disposal"
          icon={Clock}
          accentColor="text-secondary"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RiskDistChart data={riskDist} />
        <CaseTypeBarChart caseTypes={caseTypes} />
      </div>

      {/* Court Metrics Table */}
      <CourtMetricsTable courts={courts} />

      {/* Governance Notice */}
      <div className="p-4 rounded-lg bg-surface-container-low border border-outline-variant/50 flex items-start gap-3 font-body-sm text-body-sm text-on-surface-variant">
        <Info className="w-4 h-4 text-secondary shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong className="text-on-surface">Methodological Note:</strong> Analytics reflect historical administrative delay patterns and active court backlog. Variations between courts indicate operational throughput differences, not judicial culpability or causal performance gaps.
        </p>
      </div>
    </div>
  );
};
