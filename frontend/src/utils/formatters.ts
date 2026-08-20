// Formatting utilities for probabilities, dates, days to years, numbers

export function formatProbability(value?: number): string {
  if (value === undefined || value === null) return 'N/A';
  return `${(value * 100).toFixed(2)}%`;
}

export function formatDurationDays(days?: number): string {
  if (days === undefined || days === null) return 'N/A';
  if (days < 30) return `${Math.round(days)} days`;
  const years = (days / 365.25).toFixed(1);
  return `${Math.round(days)} days (~${years} yrs)`;
}

export function formatDate(dateString?: string): string {
  if (!dateString) return 'N/A';
  try {
    const d = new Date(dateString);
    return d.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return dateString;
  }
}

export function formatNumber(num?: number): string {
  if (num === undefined || num === null) return 'N/A';
  return new Intl.NumberFormat('en-US').format(num);
}
