import { describe, it, expect } from 'vitest';
import { getRiskTheme } from '../../utils/risk';
import { formatProbability, formatDurationDays } from '../../utils/formatters';

describe('Risk Utilities & Theme Mapping', () => {
  it('should map Low risk band to emerald green styling and CheckCircle2 icon', () => {
    const theme = getRiskTheme('Low');
    expect(theme.band).toBe('Low');
    expect(theme.hex).toBe('#10b981');
    expect(theme.badgeClass).toContain('emerald');
  });

  it('should map Moderate risk band to amber styling', () => {
    const theme = getRiskTheme('Moderate');
    expect(theme.band).toBe('Moderate');
    expect(theme.hex).toBe('#f59e0b');
    expect(theme.badgeClass).toContain('amber');
  });

  it('should map High risk band to orange styling', () => {
    const theme = getRiskTheme('High');
    expect(theme.band).toBe('High');
    expect(theme.hex).toBe('#f97316');
    expect(theme.badgeClass).toContain('orange');
  });

  it('should map Very High risk band to crimson red styling', () => {
    const theme = getRiskTheme('Very High');
    expect(theme.band).toBe('Very High');
    expect(theme.hex).toBe('#ef4444');
    expect(theme.badgeClass).toContain('rose');
  });

  it('should format calibrated probability as percentage', () => {
    expect(formatProbability(0.8129)).toBe('81.29%');
    expect(formatProbability(0.0006)).toBe('0.06%');
    expect(formatProbability(undefined)).toBe('N/A');
  });

  it('should format duration days to human readable string', () => {
    expect(formatDurationDays(540)).toContain('540 days (~1.5 yrs)');
    expect(formatDurationDays(15)).toBe('15 days');
    expect(formatDurationDays(undefined)).toBe('N/A');
  });
});
