import React from 'react';
import { CourtAnalyticsItem } from '../../types/analytics';
import { Building2 } from 'lucide-react';

interface CourtMetricsTableProps {
  courts: CourtAnalyticsItem[];
}

export const CourtMetricsTable: React.FC<CourtMetricsTableProps> = ({ courts }) => {
  const hasData = courts && courts.length > 0;

  return (
    <div className="card-glass overflow-hidden border-slate-800 flex flex-col space-y-4 p-6">
      <div className="flex items-center space-x-3">
        <div className="p-2 bg-purple-600/20 text-purple-400 rounded-lg border border-purple-500/30">
          <Building2 className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-base font-bold text-slate-100">Court Establishments Risk Analytics</h3>
          <p className="text-xs text-slate-400">Aggregated caseload volume and high-risk case ratio by court establishment</p>
        </div>
      </div>

      {!hasData ? (
        <div className="p-8 text-center text-xs text-slate-400">
          No court-level analytics data currently registered.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/60 text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                <th className="py-3 px-4">Court Establishment</th>
                <th className="py-3 px-4">Total Filed Cases</th>
                <th className="py-3 px-4">High Risk Ratio %</th>
                <th className="py-3 px-4">Avg JDIS Risk Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {courts.map((court, idx) => {
                const displayName = court.court_str || court.court_identifier || `Court #${court.court_no || 'N/A'}`;
                const avgScore = court.average_risk_score ?? 0;
                const highRiskPct = court.high_risk_percentage ?? 0;

                return (
                  <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 px-4 font-semibold text-slate-200">
                      {displayName}
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-300">
                      {court.case_count}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-2">
                        <span className="font-mono font-bold text-rose-400 w-12">
                          {highRiskPct.toFixed(1)}%
                        </span>
                        <div className="flex-1 max-w-[100px] bg-slate-850 rounded-full h-1.5 overflow-hidden">
                          <div
                            className="bg-rose-500 h-full rounded-full"
                            style={{ width: `${Math.min(highRiskPct, 100)}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-slate-200">
                      {avgScore.toFixed(1)} / 100
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
