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
      <div className="card-glass p-12 text-center text-slate-400">
        <FileText className="w-10 h-10 text-slate-600 mx-auto mb-3" />
        <p className="text-sm font-semibold text-slate-300">No Case Records Found</p>
        <p className="text-xs text-slate-500 mt-1">Try clearing your active filters or submit a new case prediction.</p>
      </div>
    );
  }

  return (
    <div className="card-glass overflow-hidden border-slate-800 flex flex-col">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/60 text-[11px] font-semibold uppercase tracking-wider text-slate-400">
              <th className="py-3.5 px-4">Case ID / Filing Code</th>
              <th className="py-3.5 px-4">Court Establishment</th>
              <th className="py-3.5 px-4">Case Type</th>
              <th className="py-3.5 px-4">State & District</th>
              <th className="py-3.5 px-4">Filing Date</th>
              <th className="py-3.5 px-4">Risk Evaluation</th>
              <th className="py-3.5 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs">
            {cases.map((item) => {
              const latestPred = item.latest_prediction;
              const displayId = item.ddl_case_id || item.id.substring(0, 8);

              return (
                <tr 
                  key={item.id} 
                  className="hover:bg-slate-800/40 transition-colors cursor-pointer group"
                  onClick={() => onSelectCase(item)}
                >
                  <td className="py-3.5 px-4 font-mono font-semibold text-blue-400">
                    {displayId}
                  </td>
                  <td className="py-3.5 px-4 font-medium text-slate-200">
                    <div>{item.court_str || `Court ${item.court_no}`}</div>
                    <div className="text-[10px] text-slate-400 font-mono">Court #{item.court_no}</div>
                  </td>
                  <td className="py-3.5 px-4 text-slate-300">
                    <span className="capitalize font-medium">{item.type_name}</span>
                    <span className="block text-[10px] text-slate-400 capitalize">{item.case_category || item.case_type_str}</span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-300">
                    <div>{item.state_str || `State ${item.state_code}`}</div>
                    <div className="text-[10px] text-slate-400">{item.district_str || `Dist ${item.dist_code}`}</div>
                  </td>
                  <td className="py-3.5 px-4 text-slate-400 font-mono">
                    {formatDate(item.created_at)}
                  </td>
                  <td className="py-3.5 px-4">
                    {latestPred ? (
                      <RiskBadge band={latestPred.risk_band} score={latestPred.risk_score} showScore size="sm" />
                    ) : (
                      <span className="text-slate-500 italic text-[11px]">Pending</span>
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectCase(item);
                      }}
                      className="inline-flex items-center space-x-1.5 bg-slate-800 group-hover:bg-blue-600 group-hover:text-white text-slate-300 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors"
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
      <div className="p-4 border-t border-slate-800 bg-slate-950/40 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400">
        <div>
          Showing <span className="font-semibold text-slate-200">{(page - 1) * pageSize + 1}</span> to{' '}
          <span className="font-semibold text-slate-200">{Math.min(page * pageSize, total)}</span> of{' '}
          <span className="font-semibold text-slate-200">{total}</span> records
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 text-slate-200 transition-colors"
            aria-label="Previous Page"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="px-3 py-1 bg-slate-850 rounded-md font-mono font-medium text-slate-300">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= totalPages}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 text-slate-200 transition-colors"
            aria-label="Next Page"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
