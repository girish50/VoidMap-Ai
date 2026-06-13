import React, { useEffect } from 'react';
import { useAnalysisStore } from '../store/useAnalysisStore';
import { ShieldCheck, Database, Layers, Sun, Moon } from 'lucide-react';

export default function Navbar() {
  const { apiHealth, checkApiHealth, theme, setTheme } = useAnalysisStore();

  useEffect(() => {
    checkApiHealth();
    // Poll health status every 8 seconds
    const interval = setInterval(checkApiHealth, 8000);
    return () => clearInterval(interval);
  }, []);

  const isPostgresOk = apiHealth?.relational_db_postgres === 'Connected';
  const isNeo4jOk = apiHealth?.graph_db_neo4j?.includes('Connected');

  return (
    <header className="border-b border-border-color bg-card/75 backdrop-blur-md sticky top-0 z-50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <div className="flex items-center space-x-3">
          <span className="text-2xl font-extrabold tracking-wider bg-gradient-to-r from-brand-primary to-brand-purple bg-clip-text text-transparent void-glow">
            🌌 VOIDMAP AI
          </span>
          <span className="text-[10px] text-brand-primary px-2 py-0.5 border border-brand-primary/30 rounded-full bg-brand-primary/5 uppercase font-medium tracking-widest hidden sm:inline-block">
            Engine v1.0
          </span>
        </div>

        {/* Diagnostic Badges & Theme Toggle */}
        <div className="flex items-center space-x-4 text-xs">
          
          {/* Relational Status */}
          <div className="flex items-center space-x-1.5 px-3 py-1 bg-bg border border-border-color rounded-lg">
            <Database className="w-3.5 h-3.5 text-brand-primary" />
            <span className="text-text-muted hidden md:inline">PostgreSQL:</span>
            <span className={`font-semibold ${isPostgresOk ? 'text-brand-success' : 'text-brand-primary'}`}>
              {isPostgresOk ? 'Connected' : 'SQLite Local'}
            </span>
          </div>

          {/* Graph Status */}
          <div className="flex items-center space-x-1.5 px-3 py-1 bg-bg border border-border-color rounded-lg">
            <Layers className="w-3.5 h-3.5 text-brand-purple" />
            <span className="text-text-muted hidden md:inline">Neo4j Graph:</span>
            <span className={`font-semibold ${isNeo4jOk ? 'text-brand-success' : 'text-brand-warning'}`}>
              {isNeo4jOk ? 'Connected' : 'NetworkX Local'}
            </span>
          </div>

          {/* Light/Dark Toggle */}
          <button
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            className="p-1.5 rounded-lg border border-border-color bg-card text-text-muted hover:text-text-main transition-colors duration-200 focus:outline-none focus:ring-1 focus:ring-brand-primary cursor-pointer"
            title={theme === 'dark' ? 'Activate Light Theme' : 'Activate Dark Theme'}
          >
            {theme === 'dark' ? (
              <Sun className="w-4 h-4 text-amber-500 hover:scale-110 transition-transform" />
            ) : (
              <Moon className="w-4 h-4 text-brand-primary hover:scale-110 transition-transform" />
            )}
          </button>
          
        </div>
      </div>
    </header>
  );
}
