import React from 'react';
import { CaseRecord } from '../../types/case';
import { RiskBadge } from '../common/RiskBadge';
import { formatDate } from '../../utils/formatters';
import { Eye, ChevronLeft, ChevronRight, FileText } from 'lucide-react';

interface CaseTableProps {
  cases: CaseRecord[];
  total: number;
  page: number;
  pageSize: number;
  onPageChange: (newPage: number) => void;
  onSelectCase: (record: CaseRecord) => void;
}

export const CaseTable: React.FC<CaseTableProps> = ({
  cases,
  total,
  page,
  pageSize,
  onPageChange,
  onSelectCase,
}) => {
  const totalPages = Math.max(Math.ceil(total / pageSize), 1);

  if (!cases || cases.length === 0) {
    return (
      <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg p-12 text-center text-on-surface-variant shadow-sm">
        <FileText className="w-10 h-10 text-outline mx-auto mb-3" />
        <p className="font-label-md text-label-md font-semibold text-primary">No Case Records Found</p>
        <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">Try clearing your active filters or submit a new case prediction.</p>
      </div>
    );
  }

  return (
    <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-lg shadow-sm overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-outline-variant bg-surface-container-low font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">
              <th className="py-3.5 px-4">Case ID / Filing Code</th>
              <th className="py-3.5 px-4">Court Establishment</th>
              <th className="py-3.5 px-4">Case Type</th>
              <th className="py-3.5 px-4">State & District</th>
              <th className="py-3.5 px-4">Filing Date</th>
              <th className="py-3.5 px-4">Risk Evaluation</th>
              <th className="py-3.5 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant/50 font-body-sm text-body-sm">
            {cases.map((item) => {
              const latestPred = item.latest_prediction;
              const displayId = item.ddl_case_id || item.id.substring(0, 8);

              return (
                <tr 
                  key={item.id} 
                  className="hover:bg-surface-container-low transition-colors cursor-pointer group"
                  onClick={() => onSelectCase(item)}
                >
                  <td className="py-3.5 px-4 font-data-mono font-semibold text-secondary">
                    {displayId}
                  </td>
                  <td className="py-3.5 px-4 font-medium text-on-surface">
                    <div>{item.court_str || `Court ${item.court_no}`}</div>
                    <div className="font-data-mono text-on-surface-variant">Court #{item.court_no}</div>
                  </td>
                  <td className="py-3.5 px-4 text-on-surface">
                    <span className="capitalize font-medium block">{item.type_name}</span>
                    <span className="block font-label-sm text-label-sm text-on-surface-variant capitalize mt-0.5">{item.case_category || item.case_type_str}</span>
                  </td>
                  <td className="py-3.5 px-4 text-on-surface">
                    <div>{item.state_str || `State ${item.state_code}`}</div>
                    <div className="font-label-sm text-label-sm text-on-surface-variant">{item.district_str || `Dist ${item.dist_code}`}</div>
                  </td>
                  <td className="py-3.5 px-4 text-on-surface-variant font-data-mono">
                    {formatDate(item.created_at)}
                  </td>
                  <td className="py-3.5 px-4">
                    {latestPred ? (
                      <RiskBadge band={latestPred.risk_band} score={latestPred.risk_score} showScore size="sm" />
                    ) : (
                      <span className="text-outline italic font-label-sm text-label-sm">Pending</span>
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectCase(item);
                      }}
                      className="inline-flex items-center gap-1.5 bg-surface-container-high group-hover:bg-primary group-hover:text-on-primary text-on-surface px-3 py-1.5 rounded-md font-label-sm text-label-sm font-semibold transition-colors shadow-sm"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Details</span>
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="p-4 border-t border-outline-variant bg-surface-container-low flex flex-col sm:flex-row items-center justify-between gap-3 font-body-sm text-body-sm text-on-surface-variant">
        <div>
          Showing <span className="font-semibold text-primary">{(page - 1) * pageSize + 1}</span> to{' '}
          <span className="font-semibold text-primary">{Math.min(page * pageSize, total)}</span> of{' '}
          <span className="font-semibold text-primary">{total}</span> records
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1}
            className="p-2 rounded-md bg-surface-container-high hover:bg-outline-variant disabled:opacity-40 disabled:hover:bg-surface-container-high text-on-surface transition-colors"
            aria-label="Previous Page"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="px-3 py-1 bg-surface-container-highest rounded-md font-data-mono font-medium text-on-surface">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages}
            className="p-2 rounded-md bg-surface-container-high hover:bg-outline-variant disabled:opacity-40 disabled:hover:bg-surface-container-high text-on-surface transition-colors"
            aria-label="Next Page"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
