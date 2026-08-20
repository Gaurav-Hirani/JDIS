import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: {
    value: string;
    positive?: boolean;
  };
  accentColor?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  accentColor = 'text-blue-400',
}) => {
  return (
    <div className="card-glass p-5 flex flex-col justify-between hover:border-slate-700 transition-colors">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">{title}</p>
          <h3 className="text-2xl font-bold text-slate-100 mt-2 font-mono">{value}</h3>
        </div>
        <div className={`p-2.5 rounded-lg bg-slate-800/80 ${accentColor}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      {(subtitle || trend) && (
        <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between text-xs text-slate-400">
          {subtitle && <span>{subtitle}</span>}
          {trend && (
            <span className={trend.positive ? 'text-emerald-400 font-medium' : 'text-rose-400 font-medium'}>
              {trend.value}
            </span>
          )}
        </div>
      )}
    </div>
  );
};
