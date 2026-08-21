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
    <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm p-6 space-y-4">
      <div>
        <h3 className="font-headline-sm text-headline-sm text-primary font-bold">Risk Band Distribution</h3>
        <p className="font-body-md text-body-md text-on-surface-variant">
          Proportions of filing predictions across low, moderate, high, and very high risk bands
        </p>
      </div>

      {!hasData ? (
        <div className="p-8 text-center font-body-sm text-body-sm text-on-surface-variant">
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
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="#ffffff" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    borderColor: '#e2e8f0',
                    borderRadius: '8px',
                    fontSize: '12px',
                    color: '#0f172a',
                    boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)'
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
                    <span className="font-label-sm text-label-sm text-on-surface font-medium px-1">{value} Risk</span>
                  )}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-4 border-t border-outline-variant/50 text-center">
            {data.map((item, idx) => {
              const theme = getRiskTheme(item.risk_band);
              return (
                <div key={idx} className="p-3 rounded-md bg-surface-container-low border border-outline-variant/50">
                  <span className="font-label-sm text-label-sm font-semibold uppercase tracking-wider block text-on-surface-variant">
                    {item.risk_band}
                  </span>
                  <span className={`text-base font-bold font-data-mono ${theme.textClass}`}>
                    {item.count} <span className="font-body-sm text-body-sm text-on-surface-variant">({item.percentage.toFixed(0)}%)</span>
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
