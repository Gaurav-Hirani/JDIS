import React from 'react';
import { FolderOpen } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No Records Found',
  description = 'No matching case records or prediction results were found in the system.',
  actionLabel,
  onAction,
}) => {
  return (
    <div className="card-glass p-12 text-center flex flex-col items-center justify-center my-4">
      <div className="p-3 bg-slate-800 rounded-full text-slate-400 mb-4">
        <FolderOpen className="w-8 h-8" />
      </div>
      <h4 className="text-base font-semibold text-slate-200 mb-1">{title}</h4>
      <p className="text-xs text-slate-400 max-w-sm mb-6">{description}</p>
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors shadow-md"
        >
          <span>{actionLabel}</span>
        </button>
      )}
    </div>
  );
};
