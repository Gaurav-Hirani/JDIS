import React from 'react';
import { AlertOctagon, RefreshCw } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Unable to connect to the JDIS backend',
  message = 'Failed to fetch data from the API endpoint. Please ensure the FastAPI server is running.',
  onRetry,
}) => {
  return (
    <div className="card-glass p-8 border-rose-900/50 bg-rose-950/20 text-center flex flex-col items-center justify-center my-4">
      <div className="p-3 bg-rose-900/40 rounded-full text-rose-400 mb-4">
        <AlertOctagon className="w-8 h-8" />
      </div>
      <h4 className="text-base font-semibold text-rose-200 mb-1">{title}</h4>
      <p className="text-xs text-rose-300/80 max-w-md mb-6">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center space-x-2 bg-rose-800 hover:bg-rose-700 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors shadow-md"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Connection</span>
        </button>
      )}
    </div>
  );
};
