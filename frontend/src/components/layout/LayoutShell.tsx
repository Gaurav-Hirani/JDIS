import React, { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

interface LayoutShellProps {
  children: React.ReactNode;
}

export const LayoutShell: React.FC<LayoutShellProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#0b1329] text-slate-100 flex flex-col">
      <Header onToggleMobileMenu={() => setMobileOpen(true)} />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} />
        <main className="flex-1 overflow-y-auto p-4 lg:p-8 max-w-7xl mx-auto w-full">
          {children}
        </main>
      </div>
    </div>
  );
};
