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
          className="fixed inset-0 bg-on-surface/50 backdrop-blur-sm z-40 md:hidden"
          onClick={onCloseMobile}
        />
      )}

      <nav className={`
        bg-primary dark:bg-on-primary-fixed text-on-primary dark:text-primary-fixed 
        shadow-md docked h-full w-64 left-0 fixed top-0 flex flex-col z-50
        transition-transform duration-200 ease-in-out
        ${mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        {/* Sidebar Header */}
        <div className="p-gutter flex items-center justify-between gap-4 border-b border-surface-tint/30 pb-6 pt-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white rounded-md flex items-center justify-center p-1 shrink-0">
              <Scale className="w-6 h-6 text-primary" />
            </div>
            <div>
              <div className="font-headline-md text-headline-md font-bold leading-tight">JDIS</div>
              <div className="font-label-md text-label-md text-on-primary/70 leading-none mt-1">Judicial Intelligence</div>
            </div>
          </div>
          {onCloseMobile && (
            <button onClick={onCloseMobile} className="md:hidden text-on-primary/70 hover:text-white p-1 rounded-md hover:bg-white/10 transition-colors">
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Navigation Links */}
        <div className="flex-1 overflow-y-auto py-stack-md flex flex-col gap-unit px-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onCloseMobile}
                className={({ isActive }) => `
                  flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-150 mx-2
                  ${isActive 
                    ? 'bg-primary-container text-on-primary-container font-bold scale-[0.98]' 
                    : 'text-on-primary-container/70 hover:text-on-primary hover:bg-primary-fixed-dim/20 font-medium'}
                `}
              >
                <Icon className="w-5 h-5 shrink-0" />
                <span className="font-label-md text-label-md">{item.label}</span>
              </NavLink>
            );
          })}
        </div>

        {/* Footer Disclaimer */}
        <div className="p-gutter border-t border-surface-tint/30 flex flex-col gap-unit">
          <p className="font-label-sm text-label-sm text-on-primary-container/80 mb-2 uppercase tracking-wider">
            Decision Support System
          </p>
          <p className="text-[10px] leading-relaxed text-on-primary/50 font-body-md">
            JDIS provides associational delay estimates for judicial backlog management. Not a guarantee of outcome.
          </p>
        </div>
      </nav>
    </>
  );
};
