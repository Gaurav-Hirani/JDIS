import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { fetchAnalyticsSummary, fetchRiskDistribution } from '../api/analytics';
import { fetchCases } from '../api/cases';
import { AnalyticsSummary, RiskDistributionItem } from '../types/analytics';
import { CaseRecord } from '../types/case';
import { StatCard } from '../components/common/StatCard';
import { RiskDistChart } from '../components/analytics/RiskDistChart';
import { RiskBadge } from '../components/common/RiskBadge';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { formatDate, formatDurationDays } from '../utils/formatters';
import { 
  FolderCheck, 
  ShieldAlert, 
  Activity, 
  Clock, 
  ArrowRight
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [riskDist, setRiskDist] = useState<RiskDistributionItem[]>([]);
  const [recentCases, setRecentCases] = useState<CaseRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumRes, distRes, casesRes] = await Promise.all([
        fetchAnalyticsSummary(),
        fetchRiskDistribution(),
        fetchCases({ page: 1, page_size: 5 }),
      ]);
      setSummary(sumRes);
      setRiskDist(distRes);
      setRecentCases(casesRes.items || []);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to JDIS backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return <LoadingState message="Fetching system analytics and recent case predictions..." />;
  }

  if (error || !summary) {
    return <ErrorState message={error || 'Unable to load dashboard data'} onRetry={loadData} />;
  }

  return (
    <>
      {/* Hero Section */}
      <section className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-outline-variant pb-stack-md">
        <div>
          <h1 className="font-display-lg text-display-lg text-primary mb-2">Judicial Delay Intelligence</h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">
            Monitor delay risk, case workload, and model-driven insights across the judicial system.
          </p>
        </div>
        <div className="flex items-center gap-2 bg-surface-container-low px-4 py-2 rounded border border-outline-variant/50 shrink-0">
          <span className="w-2.5 h-2.5 rounded-full bg-primary-fixed-dim inline-block animate-pulse"></span>
          <span className="font-data-mono text-data-mono text-on-surface-variant">ML System Online | Model v1.0-config-d</span>
        </div>
      </section>

      {/* KPI Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter mt-stack-lg">
        <StatCard
          title="Total Registered Cases"
          value={summary.total_cases.toLocaleString()}
          subtitle={`Across ${summary.total_predictions.toLocaleString()} total predictions`}
          icon={FolderCheck}
          accentColor="text-primary"
        />
        <StatCard
          title="High Risk Cases"
          value={summary.high_risk_cases_count.toLocaleString()}
          subtitle={`${summary.high_risk_cases_percentage.toFixed(1)}% of filing portfolio`}
          icon={ShieldAlert}
          accentColor="text-error"
        />
        <StatCard
          title="Average Risk Score"
          value={summary.average_risk_score.toFixed(2)}
          subtitle="Calibrated empirical mean score"
          icon={Activity}
          accentColor="text-secondary"
        />
        <StatCard
          title="Predicted Delay Duration"
          value={formatDurationDays(summary.average_predicted_duration_days)}
          subtitle="Estimated time to resolution"
          icon={Clock}
          accentColor="text-primary"
        />
      </section>

      {/* Main Grid: Risk Distribution & Recent Predictions Stream */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-gutter mt-stack-lg">
        {/* Risk Distribution Chart (takes 1 col) */}
        <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg p-4 flex flex-col lg:col-span-1 shadow-sm h-full">
          <h3 className="font-headline-sm text-headline-sm text-primary mb-4">Risk Distribution</h3>
          <div className="flex-1 flex flex-col items-center justify-center min-h-[300px]">
             <RiskDistChart data={riskDist} />
          </div>
        </div>

        {/* Recent Case Predictions Stream (takes 2 cols) */}
        <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg p-4 flex flex-col lg:col-span-2 shadow-sm">
          <div className="flex items-center justify-between border-b border-outline-variant pb-3 mb-4">
            <div>
              <h3 className="font-headline-sm text-headline-sm text-primary">Recent Filing Predictions</h3>
              <p className="font-body-md text-body-md text-on-surface-variant">Latest case evaluations processed by backend</p>
            </div>
            <Link to="/cases" className="font-label-md text-label-md text-secondary hover:text-primary transition-colors flex items-center gap-1">
              View All <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {recentCases.length === 0 ? (
            <div className="flex-1 flex items-center justify-center p-8">
              <p className="font-body-md text-body-md text-on-surface-variant text-center">No recent case predictions registered yet.</p>
            </div>
          ) : (
            <div className="space-y-3 flex-1 overflow-y-auto">
              {recentCases.map((item) => {
                const pred = item.latest_prediction;
                return (
                  <div
                    key={item.id}
                    onClick={() => navigate(`/cases/${item.id}`)}
                    className="p-3.5 rounded bg-surface-container-lowest border border-outline-variant/50 hover:border-outline hover:bg-surface-container-low transition-colors cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center space-x-2">
                        <span className="font-data-mono text-data-mono text-primary font-bold">
                          #{item.ddl_case_id || item.id.substring(0, 8)}
                        </span>
                        <span className="font-label-md text-label-md text-on-surface capitalize">
                          {item.type_name}
                        </span>
                      </div>
                      <p className="font-label-sm text-label-sm text-on-surface-variant">
                        {item.court_str || `Court #${item.court_no}`} • {formatDate(item.created_at)}
                      </p>
                    </div>

                    {pred ? (
                      <RiskBadge band={pred.risk_band} score={pred.risk_score} showScore size="sm" />
                    ) : (
                      <span className="font-label-sm text-label-sm text-outline">Pending</span>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          <div className="pt-4 mt-4 border-t border-outline-variant">
            <Link
              to="/analytics"
              className="font-label-md text-label-md text-secondary hover:text-primary transition-colors flex items-center justify-center gap-1 py-1"
            >
              <span>Explore Court & Case-Type Analytics</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>
    </>
  );
};
