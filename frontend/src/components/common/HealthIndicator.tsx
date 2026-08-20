import React, { useEffect, useState } from 'react';
import { fetchHealthStatus } from '../../api/health';
import { HealthCheckResponse } from '../../types/api';
import { Activity, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';

export const HealthIndicator: React.FC = () => {
  const [health, setHealth] = useState<HealthCheckResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<boolean>(false);

  const checkStatus = async () => {
    setLoading(true);
    setError(false);
    try {
      const data = await fetchHealthStatus();
      setHealth(data);
    } catch {
      setError(true);
      setHealth(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 30000); // refresh every 30s
    return () => clearInterval(interval);
  }, []);

  if (loading && !health) {
    return (
      <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700">
        <RefreshCw className="w-3.5 h-3.5 animate-spin text-slate-400" />
        <span>Checking backend...</span>
      </div>
    );
  }

  if (error || !health) {
    return (
      <button 
        onClick={checkStatus} 
        title="Backend Offline - Click to retry"
        className="flex items-center space-x-2 text-xs text-rose-400 bg-rose-950/40 hover:bg-rose-900/50 px-3 py-1.5 rounded-full border border-rose-800/60 transition-colors"
      >
        <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
        <span>Backend Disconnected</span>
      </button>
    );
  }

  return (
    <div className="flex items-center space-x-2 text-xs bg-emerald-950/40 px-3 py-1.5 rounded-full border border-emerald-800/60 text-emerald-300">
      <span className="relative flex h-2 w-2">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
      </span>
      <span className="font-medium">Backend Online</span>
      <span className="text-slate-400 text-[10px]">({health.model_version})</span>
    </div>
  );
};
