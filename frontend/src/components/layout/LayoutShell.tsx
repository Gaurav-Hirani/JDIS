import React, { useState } from 'react';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

interface LayoutShellProps {
  children: React.ReactNode;
}

export const LayoutShell: React.FC<LayoutShellProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="bg-surface text-on-surface h-screen overflow-hidden flex font-body-md">
      <Sidebar mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} />
      
      <div className="flex-1 flex flex-col md:ml-64 h-full">
        <Header onToggleMobileMenu={() => setMobileOpen(true)} />
        <main className="flex-1 overflow-y-auto p-gutter md:p-container-padding bg-background">
          <div className="max-w-[1440px] mx-auto flex flex-col gap-stack-lg">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
