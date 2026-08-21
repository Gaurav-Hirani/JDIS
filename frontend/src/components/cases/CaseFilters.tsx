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
  const inputClass = "bg-surface border border-outline-variant rounded-md px-3 py-1.5 font-body-sm text-body-sm text-on-surface placeholder-on-surface-variant focus:outline-none focus:border-secondary focus:ring-1 focus:ring-secondary transition-shadow";

  return (
    <div className="bg-surface-container-low border border-outline-variant/50 rounded-lg p-4 space-y-3">
      <div className="flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Search input */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-on-surface-variant absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search by case ID or court..."
            className={`w-full pl-9 pr-3 ${inputClass}`}
          />
        </div>

        {/* Filter controls */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {/* Risk Band Select */}
          <div className={`flex items-center gap-1.5 ${inputClass} px-2.5`}>
            <Filter className="w-3.5 h-3.5 text-on-surface-variant shrink-0" />
            <select
              value={riskBand}
              onChange={(e) => onRiskBandChange(e.target.value as RiskBand | '')}
              className="bg-transparent text-on-surface focus:outline-none cursor-pointer border-none p-0"
            >
              <option value="">All Risk Bands</option>
              <option value="Low">Low Risk (0-20)</option>
              <option value="Moderate">Moderate Risk (21-50)</option>
              <option value="High">High Risk (51-80)</option>
              <option value="Very High">Very High Risk (81-100)</option>
            </select>
          </div>

          {/* State Code Input */}
          <input
            type="text"
            value={stateCode}
            onChange={(e) => onStateCodeChange(e.target.value)}
            placeholder="State Code"
            className={`w-24 font-data-mono ${inputClass}`}
          />

          {/* Court No Input */}
          <input
            type="text"
            value={courtNo}
            onChange={(e) => onCourtNoChange(e.target.value)}
            placeholder="Court No"
            className={`w-24 font-data-mono ${inputClass}`}
          />

          {/* Reset button */}
          <button
            onClick={onReset}
            className="p-2 rounded-md bg-surface-container-high hover:bg-outline-variant text-on-surface transition-colors"
            title="Reset Filters"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
