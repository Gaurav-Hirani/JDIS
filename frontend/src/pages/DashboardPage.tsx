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
  FilePlus2, 
  ArrowRight,
  Sparkles
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
    <div className="space-y-8">
      {/* Executive Welcome & Action Header */}
      <div className="card-glass p-6 border-blue-900/40 bg-gradient-to-r from-slate-900 via-slate-900 to-blue-950/40 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 mb-1">
            <Sparkles className="w-5 h-5 text-blue-400" />
            <h2 className="text-xl font-bold text-slate-100">JDIS Executive Delay Dashboard</h2>
          </div>
          <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
            Real-time filing stage delay risk monitoring and empirical XGBoost model predictions across district court establishments.
          </p>
        </div>

        <Link
          to="/prediction/new"
          className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs px-5 py-3 rounded-lg shadow-lg shadow-blue-500/25 transition-all shrink-0"
        >
          <FilePlus2 className="w-4 h-4" />
          <span>New Filing Prediction</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Primary System KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Registered Cases"
          value={summary.total_cases}
          subtitle={`Across ${summary.total_predictions} total predictions`}
          icon={FolderCheck}
          accentColor="text-blue-400"
        />
        <StatCard
          title="High Risk Cases"
          value={summary.high_risk_cases_count}
          subtitle={`${summary.high_risk_cases_percentage.toFixed(1)}% of filing portfolio`}
          icon={ShieldAlert}
          accentColor="text-rose-400"
        />
        <StatCard
          title="Average JDIS Risk Score"
          value={`${summary.average_risk_score.toFixed(1)} / 100`}
          subtitle="Calibrated empirical mean score"
          icon={Activity}
          accentColor="text-amber-400"
        />
        <StatCard
          title="Avg Predicted Duration"
          value={formatDurationDays(summary.average_predicted_duration_days)}
          subtitle="Estimated time to resolution"
          icon={Clock}
          accentColor="text-indigo-400"
        />
      </div>

      {/* Main Grid: Risk Distribution & Recent Predictions Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Risk Distribution Chart */}
        <RiskDistChart data={riskDist} />

        {/* Recent Case Predictions Stream */}
        <div className="card-glass p-6 space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
              <div>
                <h3 className="text-base font-bold text-slate-100">Recent Filing Predictions</h3>
                <p className="text-xs text-slate-400">Latest case evaluations processed by backend</p>
              </div>
              <Link to="/cases" className="text-xs text-blue-400 hover:text-blue-300 font-semibold">
                View All →
              </Link>
            </div>

            {recentCases.length === 0 ? (
              <p className="text-xs text-slate-500 text-center py-8">No recent case predictions registered yet.</p>
            ) : (
              <div className="space-y-3">
                {recentCases.map((item) => {
                  const pred = item.latest_prediction;
                  return (
                    <div
                      key={item.id}
                      onClick={() => navigate(`/cases/${item.id}`)}
                      className="p-3.5 rounded-xl bg-slate-950/40 border border-slate-800/80 hover:border-slate-700 transition-colors cursor-pointer flex items-center justify-between gap-3"
                    >
                      <div className="space-y-0.5">
                        <div className="flex items-center space-x-2">
                          <span className="font-mono font-bold text-xs text-blue-400">
                            #{item.ddl_case_id || item.id.substring(0, 8)}
                          </span>
                          <span className="text-xs font-semibold text-slate-200 capitalize">
                            {item.type_name}
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-400">
                          {item.court_str || `Court #${item.court_no}`} • {formatDate(item.created_at)}
                        </p>
                      </div>

                      {pred ? (
                        <RiskBadge band={pred.risk_band} score={pred.risk_score} showScore size="sm" />
                      ) : (
                        <span className="text-xs text-slate-500">Pending</span>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-slate-800">
            <Link
              to="/analytics"
              className="text-xs text-slate-400 hover:text-slate-200 flex items-center justify-center space-x-1 py-1"
            >
              <span>Explore Court & Case-Type Analytics</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
