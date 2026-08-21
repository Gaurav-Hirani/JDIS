import React from 'react';
import { CaseTypeAnalyticsItem } from '../../types/analytics';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Layers } from 'lucide-react';

interface CaseTypeBarChartProps {
  caseTypes: CaseTypeAnalyticsItem[];
}

export const CaseTypeBarChart: React.FC<CaseTypeBarChartProps> = ({ caseTypes }) => {
  const hasData = caseTypes && caseTypes.length > 0;

  const chartData = hasData
    ? caseTypes.map((item) => ({
        name: item.type_name,
        total: item.case_count,
        highRiskPct: item.high_risk_percentage ?? 0,
        avgScore: item.average_risk_score ?? 0,
      }))
    : [];

  return (
    <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm p-6 space-y-4">
      <div className="flex items-center gap-3">
        <div className="p-2 bg-primary-container text-on-primary-container rounded-lg border border-primary/20 shrink-0">
          <Layers className="w-5 h-5 text-primary" />
        </div>
        <div>
          <h3 className="font-headline-sm text-headline-sm font-bold text-primary">Delay Risk Propensity by Case Type</h3>
          <p className="font-body-md text-body-md text-on-surface-variant">Average JDIS Risk Score breakdown across granular procedural case types</p>
        </div>
      </div>

      {!hasData ? (
        <div className="p-8 text-center font-body-sm text-body-sm text-on-surface-variant">
          No case-type analytics available yet.
        </div>
      ) : (
        <div className="h-64 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
              <XAxis
                dataKey="name"
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: '#cbd5e1' }}
              />
              <YAxis
                stroke="#64748b"
                fontSize={11}
                domain={[0, 100]}
                tickLine={false}
                axisLine={false}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#ffffff',
                  borderColor: '#e2e8f0',
                  borderRadius: '8px',
                  fontSize: '12px',
                  color: '#0f172a',
                  boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)'
                }}
                formatter={(value: any) => [`Avg Risk Score: ${Number(value).toFixed(1)} / 100`, 'Risk Metrics']}
              />
              <Bar dataKey="avgScore" radius={[4, 4, 0, 0]}>
                {chartData.map((entry, index) => {
                  const color = entry.avgScore > 80 ? '#ef4444' : entry.avgScore > 50 ? '#f97316' : entry.avgScore > 20 ? '#f59e0b' : '#10b981';
                  return <Cell key={`cell-${index}`} fill={color} />;
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};
