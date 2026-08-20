import React from 'react';
import { RiskDistributionItem } from '../../types/analytics';
import { getRiskTheme } from '../../utils/risk';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface RiskDistChartProps {
  data: RiskDistributionItem[];
}

export const RiskDistChart: React.FC<RiskDistChartProps> = ({ data }) => {
  const hasData = data && data.length > 0;

  const chartData = hasData
    ? data.map((item) => {
        const theme = getRiskTheme(item.risk_band);
        return {
          name: item.risk_band,
          value: item.count,
          percentage: item.percentage,
          color: theme.hex,
        };
      })
    : [];

  return (
    <div className="card-glass p-6 space-y-4">
      <div>
        <h3 className="text-base font-bold text-slate-100">Risk Band Distribution</h3>
        <p className="text-xs text-slate-400">
          Proportions of filing predictions across low, moderate, high, and very high risk bands
        </p>
      </div>

      {!hasData ? (
        <div className="p-8 text-center text-xs text-slate-400">
          No risk distribution analytics available yet.
        </div>
      ) : (
        <>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="#0f172a" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: '#334155',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: '#f8fafc',
                  }}
                  formatter={(val: any, name: any, item: any) => [
                    `${val} cases (${item.payload.percentage.toFixed(1)}%)`,
                    `Risk Band: ${name}`,
                  ]}
                />
                <Legend
                  verticalAlign="bottom"
                  height={36}
                  formatter={(value: string) => (
                    <span className="text-xs text-slate-300 font-medium px-1">{value} Risk</span>
                  )}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-800 text-center">
            {data.map((item, idx) => {
              const theme = getRiskTheme(item.risk_band);
              return (
                <div key={idx} className="p-2 rounded-lg bg-slate-950/40 border border-slate-850">
                  <span className="text-[10px] font-semibold uppercase tracking-wider block text-slate-400">
                    {item.risk_band}
                  </span>
                  <span className={`text-base font-bold font-mono ${theme.textClass}`}>
                    {item.count} <span className="text-xs font-normal text-slate-400">({item.percentage.toFixed(0)}%)</span>
                  </span>
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
};
