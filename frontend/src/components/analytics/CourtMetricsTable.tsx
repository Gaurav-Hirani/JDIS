import React from 'react';
import { CourtAnalyticsItem } from '../../types/analytics';
import { Building2 } from 'lucide-react';

interface CourtMetricsTableProps {
  courts: CourtAnalyticsItem[];
}

export const CourtMetricsTable: React.FC<CourtMetricsTableProps> = ({ courts }) => {
  const hasData = courts && courts.length > 0;

  return (
    <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm overflow-hidden flex flex-col space-y-4 p-6">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-primary-container text-on-primary-container rounded-lg border border-primary/20 shrink-0">
          <Building2 className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h3 className="font-headline-sm text-headline-sm font-bold text-primary">Court Establishments Risk Analytics</h3>
          <p className="font-body-md text-body-md text-on-surface-variant">Aggregated caseload volume and high-risk case ratio by court establishment</p>
        </div>
      </div>

      {!hasData ? (
        <div className="p-8 text-center font-body-sm text-body-sm text-on-surface-variant">
          No court-level analytics data currently registered.
        </div>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-outline-variant/50">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-outline-variant bg-surface-container-low font-label-sm text-label-sm font-semibold uppercase tracking-wider text-on-surface-variant">
                <th className="py-3 px-4">Court Establishment</th>
                <th className="py-3 px-4">Total Filed Cases</th>
                <th className="py-3 px-4">High Risk Ratio %</th>
                <th className="py-3 px-4">Avg JDIS Risk Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant/50 font-body-sm text-body-sm">
              {courts.map((court, idx) => {
                const displayName = court.court_str || court.court_identifier || `Court #${court.court_no || 'N/A'}`;
                const avgScore = court.average_risk_score ?? 0;
                const highRiskPct = court.high_risk_percentage ?? 0;

                return (
                  <tr key={idx} className="hover:bg-surface-container-low transition-colors">
                    <td className="py-3 px-4 font-semibold text-on-surface">
                      {displayName}
                    </td>
                    <td className="py-3 px-4 font-data-mono text-on-surface">
                      {court.case_count}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <span className="font-data-mono font-bold text-error w-12">
                          {highRiskPct.toFixed(1)}%
                        </span>
                        <div className="flex-1 max-w-[100px] bg-surface-container-highest rounded-full h-1.5 overflow-hidden">
                          <div
                            className="bg-error h-full rounded-full"
                            style={{ width: `${Math.min(highRiskPct, 100)}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 font-data-mono font-bold text-on-surface">
                      {avgScore.toFixed(1)} <span className="text-on-surface-variant font-normal">/ 100</span>
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
