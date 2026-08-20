import React, { useEffect, useState } from 'react';
import { fetchCases } from '../api/cases';
import { CaseRecord } from '../types/case';
import { RiskBand } from '../types/prediction';
import { CaseTable } from '../components/cases/CaseTable';
import { CaseFilters } from '../components/cases/CaseFilters';
import { CaseDetailModal } from '../components/cases/CaseDetailModal';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { FolderGit2, FilePlus2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export const CaseManagementPage: React.FC = () => {
  const [cases, setCases] = useState<CaseRecord[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const pageSize = 15;

  // Filter States
  const [search, setSearch] = useState<string>('');
  const [stateCode, setStateCode] = useState<string>('');
  const [courtNo, setCourtNo] = useState<string>('');
  const [typeName, setTypeName] = useState<string>('');
  const [riskBand, setRiskBand] = useState<RiskBand | ''>('');

  const [selectedCase, setSelectedCase] = useState<CaseRecord | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadCases = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchCases({
        page,
        page_size: pageSize,
        state_code: stateCode || undefined,
        court_no: courtNo || undefined,
        type_name: typeName || undefined,
        risk_band: riskBand || undefined,
        search: search || undefined,
      });
      setCases(res.items || []);
      setTotal(res.total || 0);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch case records from JDIS backend');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCases();
  }, [page, stateCode, courtNo, typeName, riskBand, search]);

  const handleResetFilters = () => {
    setSearch('');
    setStateCode('');
    setCourtNo('');
    setTypeName('');
    setRiskBand('');
    setPage(1);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="card-glass p-6 border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
            <FolderGit2 className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-100">Case Records Repository</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Browse, filter, and inspect registered case filings and historical JDIS risk evaluations
            </p>
          </div>
        </div>

        <Link
          to="/prediction/new"
          className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs px-4 py-2.5 rounded-lg transition-colors shadow-md shrink-0"
        >
          <FilePlus2 className="w-4 h-4" />
          <span>New Filing Record</span>
        </Link>
      </div>

      {/* Filter Toolbar */}
      <CaseFilters
        search={search}
        onSearchChange={setSearch}
        stateCode={stateCode}
        onStateCodeChange={setStateCode}
        courtNo={courtNo}
        onCourtNoChange={setCourtNo}
        typeName={typeName}
        onTypeNameChange={setTypeName}
        riskBand={riskBand}
        onRiskBandChange={setRiskBand}
        onReset={handleResetFilters}
      />

      {/* Main Table or Loading/Error States */}
      {loading ? (
        <LoadingState message="Querying case repository records..." />
      ) : error ? (
        <ErrorState message={error} onRetry={loadCases} />
      ) : (
        <CaseTable
          cases={cases}
          total={total}
          page={page}
          pageSize={pageSize}
          onPageChange={setPage}
          onSelectCase={setSelectedCase}
        />
      )}

      {/* Case Detail Modal Drawer */}
      <CaseDetailModal record={selectedCase} onClose={() => setSelectedCase(null)} />
    </div>
  );
};
