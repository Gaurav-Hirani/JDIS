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
  accentColor = 'text-primary',
}) => {
  return (
    <div className="bg-surface-container-lowest border border-outline-variant/50 p-4 rounded-lg shadow-sm flex flex-col hover:border-outline transition-colors">
      <div className="text-on-surface-variant font-label-md text-label-md mb-2 flex justify-between items-center uppercase tracking-wider">
        <span>{title}</span>
        <Icon className={`w-5 h-5 ${accentColor}`} />
      </div>
      <div className={`font-headline-md text-headline-md mb-1 ${accentColor}`}>{value}</div>
      {(subtitle || trend) && (
        <div className="text-surface-tint font-label-sm text-label-sm flex items-center gap-1 mt-1">
          {subtitle && <span>{subtitle}</span>}
          {trend && (
            <span className={trend.positive ? 'text-risk-low' : 'text-risk-veryHigh'}>
              • {trend.value}
            </span>
          )}
        </div>
      )}
    </div>
  );
};
