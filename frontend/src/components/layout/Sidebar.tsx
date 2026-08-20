import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FilePlus2, 
  FolderGit2, 
  BarChart3, 
  BookOpenCheck,
  Scale,
  X
} from 'lucide-react';

interface SidebarProps {
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ mobileOpen, onCloseMobile }) => {
  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'New Prediction', path: '/prediction/new', icon: FilePlus2 },
    { label: 'Cases Repository', path: '/cases', icon: FolderGit2 },
    { label: 'Analytics', path: '/analytics', icon: BarChart3 },
    { label: 'Methodology & About', path: '/about', icon: BookOpenCheck },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {mobileOpen && (
        <div 
          className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-40 lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      <aside className={`
        fixed lg:static inset-y-0 left-0 z-50
        w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between
        transform transition-transform duration-200 ease-in-out
        ${mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div>
          {/* Sidebar Header */}
          <div className="p-6 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-600 rounded-xl text-white shadow-lg shadow-blue-500/20">
                <Scale className="w-5 h-5" />
              </div>
              <div>
                <span className="font-bold text-slate-100 text-lg tracking-tight block">JDIS Platform</span>
                <span className="text-[10px] text-slate-400 font-medium tracking-wider uppercase">Filing Analytics</span>
              </div>
            </div>
            {onCloseMobile && (
              <button 
                onClick={onCloseMobile} 
                className="lg:hidden text-slate-400 hover:text-white p-1"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>

          {/* Navigation Links */}
          <nav className="p-4 space-y-1.5">
            <p className="px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Main Menu</p>
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={onCloseMobile}
                  className={({ isActive }) => `
                    flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all duration-150
                    ${isActive 
                      ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm' 
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'}
                  `}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Footer Disclaimer */}
        <div className="p-4 m-4 rounded-xl bg-slate-850/80 border border-slate-800 text-xs text-slate-400">
          <p className="font-semibold text-slate-300 mb-1">Decision Support System</p>
          <p className="text-[11px] leading-relaxed text-slate-400">
            JDIS provides associational delay estimates for judicial backlog management. Not a guarantee of outcome.
          </p>
        </div>
      </aside>
    </>
  );
};
