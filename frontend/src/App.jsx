import React, { useState } from 'react';
import LandingPage from './LandingPage';
import Dashboard from './Dashboard';
import './index.css';

export default function App() {
  const [showDashboard, setShowDashboard] = useState(false);

  return (
    <div onClick={() => !showDashboard && setShowDashboard(true)}>
      {showDashboard ? <Dashboard /> : <LandingPage />}
    </div>
  );
}