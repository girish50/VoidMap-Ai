import React from 'react';
import { ReactFlow, Background, Controls } from '@xyflow/react';
import { useAnalysisStore } from '../store/useAnalysisStore';
import '@xyflow/react/dist/style.css';

export default function FlowViewer({ treeData }) {
  const { theme } = useAnalysisStore();
  const hasData = treeData && Array.isArray(treeData.nodes) && treeData.nodes.length > 0;

  if (!hasData) {
    return (
      <div className="flex flex-col items-center justify-center h-80 bg-bg border border-border-color rounded-xl">
        <span className="text-text-muted text-xs">Select or analyze a proposal to view consequence pathways.</span>
      </div>
    );
  }

  // Pre-process nodes to attach custom visual styles (2026 Minimal Canvas style)
  const styledNodes = treeData.nodes.map(node => {
    let borderStyle = 'border-border-color';
    let textStyle = 'text-text-main font-medium';
    let bgStyle = 'bg-card';

    if (node.type === 'input') {
      borderStyle = 'border-brand-purple/40';
      bgStyle = 'bg-brand-purple/5';
      textStyle = 'text-brand-purple font-semibold';
    } else if (node.type === 'output') {
      borderStyle = 'border-brand-danger/40';
      bgStyle = 'bg-brand-danger/5';
      textStyle = 'text-brand-danger font-semibold';
    } else if (node.data.label.includes('⚠️') || node.data.label.includes('❌')) {
      borderStyle = 'border-brand-warning/40';
      bgStyle = 'bg-brand-warning/5';
      textStyle = 'text-brand-warning';
    }

    return {
      ...node,
      className: `${borderStyle} ${bgStyle} ${textStyle} px-4 py-3 rounded-lg border text-xs font-sans text-center transition-all duration-300 w-52 shadow-sm`,
      data: {
        label: (
          <div className="flex flex-col items-center justify-center leading-relaxed">
            <span>{node.data.label}</span>
          </div>
        )
      }
    };
  });

  // Pre-process edges to ensure clean flows are active
  const styledEdges = treeData.edges.map(edge => ({
    ...edge,
    style: { 
      stroke: edge.animated ? 'var(--brand-danger)' : 'var(--brand-primary)', 
      strokeWidth: 1.5,
      opacity: 0.7 
    },
    animated: !!edge.animated,
  }));

  const gridColor = theme === 'dark' ? '#1E293B' : '#E2E8F0';

  return (
    <div className="w-full h-[400px] border border-border-color rounded-xl overflow-hidden bg-bg/50 relative">
      
      {/* Visual Canvas Panel */}
      <ReactFlow
        nodes={styledNodes}
        edges={styledEdges}
        fitView
        color="var(--text-main)"
        className="text-text-main"
      >
        <Background color={gridColor} gap={16} size={1} />
        <Controls className="bg-card border border-border-color text-text-main [&>button]:border-border-color [&>button]:bg-card [&>button]:text-text-main [&>button:hover]:bg-bg" />
      </ReactFlow>

      {/* Floating Diagram Legend */}
      <div className="absolute bottom-4 right-4 flex items-center space-x-3 bg-card/95 border border-border-color px-3 py-1.5 rounded-lg text-[10px] text-text-muted font-medium z-10 pointer-events-none shadow-sm">
        <div className="flex items-center space-x-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-brand-purple/10 border border-brand-purple/30"></span>
          <span>Root</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-brand-warning/10 border border-brand-warning/30"></span>
          <span>Gap/Risk</span>
        </div>
        <div className="flex items-center space-x-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-brand-danger/10 border border-brand-danger/30"></span>
          <span>Collapse Output</span>
        </div>
      </div>
      
    </div>
  );
}
