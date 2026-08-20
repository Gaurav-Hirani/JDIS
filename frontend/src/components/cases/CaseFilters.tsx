import React from 'react';
import { RiskBand } from '../../types/prediction';
import { Search, Filter, RotateCcw } from 'lucide-react';

interface CaseFiltersProps {
  search: string;
  onSearchChange: (value: string) => void;
  stateCode: string;
  onStateCodeChange: (value: string) => void;
  courtNo: string;
  onCourtNoChange: (value: string) => void;
  typeName: string;
  onTypeNameChange: (value: string) => void;
  riskBand: RiskBand | '';
  onRiskBandChange: (value: RiskBand | '') => void;
  onReset: () => void;
}

export const CaseFilters: React.FC<CaseFiltersProps> = ({
  search,
  onSearchChange,
  stateCode,
  onStateCodeChange,
  courtNo,
  onCourtNoChange,
  typeName,
  onTypeNameChange,
  riskBand,
  onRiskBandChange,
  onReset,
}) => {
  return (
    <div className="card-glass p-4 space-y-3 border-slate-800">
      <div className="flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Search input */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search by case ID or court..."
            className="w-full bg-slate-950 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Filter controls */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {/* Risk Band Select */}
          <div className="flex items-center space-x-1.5 bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-300">
            <Filter className="w-3.5 h-3.5 text-slate-500" />
            <select
              value={riskBand}
              onChange={(e) => onRiskBandChange(e.target.value as RiskBand | '')}
              className="bg-transparent text-xs text-slate-200 focus:outline-none cursor-pointer"
            >
              <option value="" className="bg-slate-900">All Risk Bands</option>
              <option value="Low" className="bg-slate-900">Low Risk (0-20)</option>
              <option value="Moderate" className="bg-slate-900">Moderate Risk (21-50)</option>
              <option value="High" className="bg-slate-900">High Risk (51-80)</option>
              <option value="Very High" className="bg-slate-900">Very High Risk (81-100)</option>
            </select>
          </div>

          {/* State Code Input */}
          <input
            type="text"
            value={stateCode}
            onChange={(e) => onStateCodeChange(e.target.value)}
            placeholder="State Code"
            className="w-24 bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-100 placeholder-slate-500 font-mono focus:outline-none focus:border-blue-500"
          />

          {/* Court No Input */}
          <input
            type="text"
            value={courtNo}
            onChange={(e) => onCourtNoChange(e.target.value)}
            placeholder="Court No"
            className="w-24 bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-100 placeholder-slate-500 font-mono focus:outline-none focus:border-blue-500"
          />

          {/* Reset button */}
          <button
            onClick={onReset}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition-colors"
            title="Reset Filters"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
