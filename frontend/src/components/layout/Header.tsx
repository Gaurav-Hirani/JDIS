import React from 'react';
import { HealthIndicator } from '../common/HealthIndicator';
import { Scale, Info, Menu } from 'lucide-react';

interface HeaderProps {
  onToggleMobileMenu?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleMobileMenu }) => {
  return (
    <header className="bg-slate-900/90 border-b border-slate-800 sticky top-0 z-30 backdrop-blur px-4 lg:px-8 py-3.5 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <button
          onClick={onToggleMobileMenu}
          className="lg:hidden text-slate-400 hover:text-slate-200 p-1.5 rounded-lg bg-slate-800"
          aria-label="Toggle Navigation Menu"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="flex items-center space-x-2">
          <div className="p-1.5 bg-blue-600/20 rounded-lg text-blue-400 border border-blue-500/30">
            <Scale className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-100 leading-none">JDIS</h1>
            <p className="text-[10px] text-slate-400 font-medium tracking-tight">Judicial Delay Intelligence System</p>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        {/* Subtle Decision-Support Badge */}
        <div className="hidden md:flex items-center space-x-1.5 text-[11px] text-slate-400 bg-slate-800/60 px-3 py-1.5 rounded-md border border-slate-700/50">
          <Info className="w-3.5 h-3.5 text-blue-400" />
          <span>Administrative Decision-Support System</span>
        </div>

        {/* Live GET /health Indicator */}
        <HealthIndicator />
      </div>
    </header>
  );
};
