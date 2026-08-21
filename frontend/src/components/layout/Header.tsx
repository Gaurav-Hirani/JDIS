import React from 'react';
import { HealthIndicator } from '../common/HealthIndicator';
import { Menu, Search, Wifi, Bell, UserCircle } from 'lucide-react';
import { useLocation } from 'react-router-dom';

interface HeaderProps {
  onToggleMobileMenu?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleMobileMenu }) => {
  const location = useLocation();
  
  // Format pathname to title
  const getTitle = () => {
    const path = location.pathname.split('/')[1] || 'Dashboard';
    return path.charAt(0).toUpperCase() + path.slice(1).replace('-', ' ');
  };

  return (
    <header className="bg-surface border-b border-outline-variant flex justify-between items-center w-full h-16 px-gutter max-w-full sticky top-0 z-30">
      <div className="flex items-center gap-4 h-full">
        <button
          onClick={onToggleMobileMenu}
          className="md:hidden text-primary p-2 hover:bg-surface-container-high rounded-md transition-colors"
          aria-label="Toggle Navigation Menu"
        >
          <Menu className="w-6 h-6" />
        </button>
        <span className="font-headline-sm text-headline-sm font-black text-primary md:hidden">
          JDIS
        </span>
        <div className="hidden md:flex gap-6 h-full items-center">
          <span className="text-primary font-bold border-b-2 border-primary h-full flex items-center px-2 font-label-md text-label-md">
            {getTitle()}
          </span>
        </div>
      </div>

      <div className="flex-1 max-w-md mx-6 hidden md:block">
        <div className="relative focus-within:ring-2 focus-within:ring-secondary rounded-lg">
          <Search className="absolute left-3 top-2.5 w-5 h-5 text-on-surface-variant" />
          <input 
            className="w-full bg-surface-container-high border-none rounded-lg pl-10 pr-4 py-2 text-on-surface font-body-md focus:outline-none placeholder-on-surface-variant" 
            placeholder="Search cases, courts..." 
            type="text" 
          />
        </div>
      </div>

      <div className="flex items-center gap-2 text-primary">
        <div className="hidden lg:flex items-center gap-4 mr-4">
          <HealthIndicator />
        </div>
        
        <button className="p-2 hover:bg-surface-container-high transition-all rounded-full flex items-center justify-center">
          <Wifi className="w-5 h-5" />
        </button>
        <button className="p-2 hover:bg-surface-container-high transition-all rounded-full flex items-center justify-center relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-error rounded-full"></span>
        </button>
        <button className="p-2 hover:bg-surface-container-high transition-all rounded-full flex items-center justify-center ml-2">
          <UserCircle className="w-6 h-6" />
        </button>
      </div>
    </header>
  );
};
