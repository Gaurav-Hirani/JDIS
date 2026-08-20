import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  height?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ 
  message = 'Loading data from JDIS backend...',
  height = 'h-64'
}) => {
  return (
    <div className={`card-glass ${height} flex flex-col items-center justify-center p-8 text-center`}>
      <Loader2 className="w-8 h-8 text-blue-500 animate-spin mb-3" />
      <p className="text-sm font-medium text-slate-300">{message}</p>
      <p className="text-xs text-slate-500 mt-1">Connecting to ML serving engine</p>
    </div>
  );
};
