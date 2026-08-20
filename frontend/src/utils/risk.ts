import { RiskBand } from '../types/prediction';

export interface RiskTheme {
  band: RiskBand;
  badgeClass: string;
  textClass: string;
  bgClass: string;
  borderClass: string;
  hex: string;
  iconName: string;
  description: string;
}

export function getRiskTheme(band: RiskBand): RiskTheme {
  switch (band) {
    case 'Low':
      return {
        band: 'Low',
        badgeClass: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30',
        textClass: 'text-emerald-400',
        bgClass: 'bg-emerald-500',
        borderClass: 'border-emerald-500',
        hex: '#10b981',
        iconName: 'CheckCircle2',
        description: 'Low probability of severe delay (0-20 score range)',
      };
    case 'Moderate':
      return {
        band: 'Moderate',
        badgeClass: 'bg-amber-500/10 text-amber-400 border border-amber-500/30',
        textClass: 'text-amber-400',
        bgClass: 'bg-amber-500',
        borderClass: 'border-amber-500',
        hex: '#f59e0b',
        iconName: 'AlertTriangle',
        description: 'Moderate probability of severe delay (21-50 score range)',
      };
    case 'High':
      return {
        band: 'High',
        badgeClass: 'bg-orange-500/10 text-orange-400 border border-orange-500/30',
        textClass: 'text-orange-400',
        bgClass: 'bg-orange-500',
        borderClass: 'border-orange-500',
        hex: '#f97316',
        iconName: 'AlertCircle',
        description: 'High probability of severe delay (51-80 score range)',
      };
    case 'Very High':
    default:
      return {
        band: 'Very High',
        badgeClass: 'bg-rose-500/10 text-rose-400 border border-rose-500/30',
        textClass: 'text-rose-400',
        bgClass: 'bg-rose-500',
        borderClass: 'border-rose-500',
        hex: '#ef4444',
        iconName: 'ShieldAlert',
        description: 'Very High probability of severe delay (81-100 score range)',
      };
  }
}
