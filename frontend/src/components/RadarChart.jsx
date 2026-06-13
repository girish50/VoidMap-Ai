import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { AlertCircle, Skull } from 'lucide-react';
import { useAnalysisStore } from '../store/useAnalysisStore';

export default function FailureDNAMap({ failureDna }) {
  const { theme } = useAnalysisStore();
  const hasData = Array.isArray(failureDna) && failureDna.length > 0;

  if (!hasData) {
    return (
      <div className="flex flex-col items-center justify-center h-80 bg-bg border border-border-color rounded-xl">
        <span className="text-text-muted text-sm">Select or analyze a proposal to view Failure DNA comparisons.</span>
      </div>
    );
  }

  // Format dataset for Recharts bar chart mapping
  const chartData = failureDna.map(item => ({
    name: item.name.split(" ")[0] + " " + (item.name.split(" ")[1] || ""), // Shorten name
    fullName: item.name,
    "Similarity Proximity": Math.round(item.similarity * 100),
  }));

  // Theme-aware red color spectrum mapping for failure cases
  const colors = theme === 'dark' 
    ? ["#F43F5E", "#E11D48", "#BE123C"] 
    : ["#DC2626", "#E11D48", "#B91C1C"];

  const axisStroke = theme === 'dark' ? '#8892B0' : '#64748B';

  return (
    <div className="space-y-6">
      
      {/* Chart Panel */}
      <div className="glass-card p-5 bg-card/40">
        <h4 className="font-extrabold text-xs text-text-main tracking-widest uppercase mb-4 flex items-center space-x-2">
          <Skull className="w-3.5 h-3.5 text-brand-danger" />
          <span>Historical Failure DNA Mapping Proximity (%)</span>
        </h4>
        
        <div className="w-full h-48 text-xs font-mono">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              layout="vertical"
              margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
            >
              <XAxis 
                type="number" 
                domain={[0, 100]} 
                stroke={axisStroke}
                fontSize={10}
              />
              <YAxis 
                dataKey="name" 
                type="category" 
                stroke={axisStroke}
                fontSize={10}
                width={80}
              />
              <Tooltip 
                cursor={{ fill: 'rgba(99, 102, 241, 0.05)' }}
                contentStyle={{ 
                  background: 'var(--card)', 
                  border: '1px solid var(--border-color)', 
                  color: 'var(--text-main)', 
                  fontSize: '11px', 
                  borderRadius: '6px' 
                }}
              />
              <Bar dataKey="Similarity Proximity" radius={[0, 4, 4, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Collapse Lessons Feed */}
      <div className="space-y-3">
        {failureDna.map((item, idx) => (
          <div key={idx} className="glass-card p-5 border-l-2 border-brand-danger bg-gradient-to-r from-brand-danger/5 to-transparent">
            
            {/* Header */}
            <div className="flex items-start justify-between space-x-4 mb-2.5">
              <div>
                <h4 className="font-extrabold text-sm text-text-main tracking-wide">
                  {item.name}
                </h4>
                <span className="text-[9px] px-1.5 py-0.5 rounded bg-bg border border-border-color text-text-muted font-medium uppercase mt-1 inline-block">
                  Domain Match: {item.domain}
                </span>
              </div>
              <span className="text-xs font-mono font-extrabold text-brand-danger px-2.5 py-1 bg-brand-danger/10 border border-brand-danger/20 rounded-lg">
                {Math.round(item.similarity * 100)}% Proximity
              </span>
            </div>

            {/* Content summary */}
            <p className="text-xs text-text-muted leading-relaxed text-justify mb-3">
              <strong className="text-text-main">What Happened:</strong> "{item.summary}"
            </p>

            {/* Overlapping Gaps list */}
            {Array.isArray(item.matched_gaps) && item.matched_gaps.length > 0 && (
              <div className="mb-3">
                <span className="text-[10px] text-brand-danger uppercase font-bold tracking-wider block mb-1">
                  Overlapping Gaps in Your Design:
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {item.matched_gaps.map((gap, i) => (
                    <span key={i} className="text-[9px] px-2 py-0.5 rounded-full bg-brand-danger/5 border border-brand-danger/25 text-brand-danger font-semibold">
                      ❌ {gap}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Academic Lesson Learned */}
            <div className="bg-bg p-3.5 border border-border-color rounded-lg text-xs leading-relaxed text-text-main flex items-start space-x-2">
              <AlertCircle className="w-4.5 h-4.5 text-brand-primary shrink-0 mt-0.5" />
              <div>
                <strong className="text-brand-primary font-bold block mb-0.5 uppercase text-[9px] tracking-wider">Historical System Prevention Lesson:</strong>
                <span className="italic text-text-muted">"{item.lesson}"</span>
              </div>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}
