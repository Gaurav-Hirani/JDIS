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
    <div className="card-glass p-6 space-y-4">
      <div className="flex items-center space-x-3">
        <div className="p-2 bg-blue-600/20 text-blue-400 rounded-lg border border-blue-500/30">
          <Layers className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-base font-bold text-slate-100">Delay Risk Propensity by Case Type</h3>
          <p className="text-xs text-slate-400">Average JDIS Risk Score breakdown across granular procedural case types</p>
        </div>
      </div>

      {!hasData ? (
        <div className="p-8 text-center text-xs text-slate-400">
          No case-type analytics available yet.
        </div>
      ) : (
        <div className="h-64 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey="name"
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: '#334155' }}
              />
              <YAxis
                stroke="#64748b"
                fontSize={11}
                domain={[0, 100]}
                tickLine={false}
                axisLine={{ stroke: '#334155' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '8px',
                  fontSize: '12px',
                  color: '#f8fafc',
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
