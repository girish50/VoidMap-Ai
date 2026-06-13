import React from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-bg text-text-main font-sans selection:bg-brand-primary/30 selection:text-white">
      <Navbar />
      <main className="pb-16">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
