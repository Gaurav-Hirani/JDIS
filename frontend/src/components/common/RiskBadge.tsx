import React from 'react';
import { RiskBand } from '../../types/prediction';
import { getRiskTheme } from '../../utils/risk';
import { CheckCircle2, AlertTriangle, AlertCircle, ShieldAlert } from 'lucide-react';

interface RiskBadgeProps {
  band: RiskBand;
  score?: number;
  size?: 'sm' | 'md' | 'lg';
  showScore?: boolean;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ 
  band, 
  score, 
  size = 'md', 
  showScore = false 
}) => {
  const theme = getRiskTheme(band);

  const getIcon = () => {
    switch (band) {
      case 'Low':
        return <CheckCircle2 className={size === 'sm' ? 'w-3 h-3' : size === 'lg' ? 'w-5 h-5' : 'w-4 h-4'} />;
      case 'Moderate':
        return <AlertTriangle className={size === 'sm' ? 'w-3 h-3' : size === 'lg' ? 'w-5 h-5' : 'w-4 h-4'} />;
      case 'High':
        return <AlertCircle className={size === 'sm' ? 'w-3 h-3' : size === 'lg' ? 'w-5 h-5' : 'w-4 h-4'} />;
      case 'Very High':
      default:
        return <ShieldAlert className={size === 'sm' ? 'w-3 h-3' : size === 'lg' ? 'w-5 h-5' : 'w-4 h-4'} />;
    }
  };

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs space-x-1',
    md: 'px-2.5 py-1 text-xs font-semibold space-x-1.5',
    lg: 'px-3.5 py-1.5 text-sm font-bold space-x-2',
  }[size];

  return (
    <span 
      className={`inline-flex items-center rounded-md font-medium tracking-wide shadow-sm ${theme.badgeClass} ${sizeClasses}`}
      title={theme.description}
      aria-label={`Risk Band: ${band}${score !== undefined ? `, Score: ${score}` : ''}`}
    >
      {getIcon()}
      <span>{band}</span>
      {showScore && score !== undefined && (
        <span className="opacity-80 border-l border-current/30 pl-1.5 font-mono">
          {score}/100
        </span>
      )}
    </span>
  );
};
