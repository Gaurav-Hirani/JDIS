import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LayoutShell } from './components/layout/LayoutShell';
import { DashboardPage } from './pages/DashboardPage';
import { NewPredictionPage } from './pages/NewPredictionPage';
import { PredictionResultPage } from './pages/PredictionResultPage';
import { CaseManagementPage } from './pages/CaseManagementPage';
import { CaseDetailPage } from './pages/CaseDetailPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { AboutPage } from './pages/AboutPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <LayoutShell>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/prediction/new" element={<NewPredictionPage />} />
          <Route path="/prediction/:id" element={<PredictionResultPage />} />
          <Route path="/cases" element={<CaseManagementPage />} />
          <Route path="/cases/:id" element={<CaseDetailPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </LayoutShell>
    </BrowserRouter>
  );
};

export default App;
