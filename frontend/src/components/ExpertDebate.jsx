import React, { useState } from 'react';
import { Shield, ShieldAlert, Scale, Landmark, UserCheck, Eye, Compass, MessageSquare, ChevronDown, ChevronUp } from 'lucide-react';
import { useAnalysisStore } from '../store/useAnalysisStore';

export default function ExpertDebate({ expertReviews, boardDisagreements }) {
  const { theme } = useAnalysisStore();
  const [activeTab, setActiveTab] = useState('boardroom'); // 'boardroom' or 'clashes'
  const [expandedReview, setExpandedReview] = useState(null); // Accordion state for experts

  const hasReviews = Array.isArray(expertReviews) && expertReviews.length > 0;

  if (!hasReviews) {
    return (
      <div className="flex flex-col items-center justify-center h-80 bg-card border border-border-color rounded-2xl">
        <MessageSquare className="w-8 h-8 text-brand-purple/40 animate-pulse mb-2" />
        <span className="text-text-muted text-xs tracking-wider uppercase font-bold">Awaiting Boardroom Activation...</span>
      </div>
    );
  }

  // Agent profiles with customized icons and colors adapted to light/dark themes
  const getAgentMetadata = (name) => {
    const isDark = theme === 'dark';
    const metadata = {
      "Compliance Officer": {
        title: "Chief Compliance Officer & Lawyer",
        initials: "⚖️ LY",
        colorClass: isDark 
          ? "bg-amber-500/10 border-amber-500/30 text-amber-400" 
          : "bg-amber-50 border-amber-300 text-amber-700",
        icon: <Scale className="w-4 h-4" />
      },
      "Red Team Attacker": {
        title: "Security Engineer & Red Teamer",
        initials: "🕷️ SEC",
        colorClass: isDark 
          ? "bg-rose-500/10 border-rose-500/30 text-rose-400" 
          : "bg-rose-50 border-rose-300 text-rose-700",
        icon: <ShieldAlert className="w-4 h-4" />
      },
      "System Reliability Engineer": {
        title: "Principal DevOps & SRE",
        initials: "⚙️ SRE",
        colorClass: isDark 
          ? "bg-cyan-500/10 border-cyan-500/30 text-cyan-400" 
          : "bg-cyan-50 border-cyan-300 text-cyan-700",
        icon: <Shield className="w-4 h-4" />
      },
      "VC Investor": {
        title: "Venture Capital Partner & PM",
        initials: "💼 VC",
        colorClass: isDark 
          ? "bg-indigo-500/10 border-indigo-500/30 text-indigo-400" 
          : "bg-indigo-50 border-indigo-300 text-indigo-700",
        icon: <Landmark className="w-4 h-4" />
      },
      "Ethicist": {
        title: "AI Safety & Ethics Advisor",
        initials: "👁️ ETH",
        colorClass: isDark 
          ? "bg-purple-500/10 border-purple-500/30 text-purple-400" 
          : "bg-purple-50 border-purple-300 text-purple-700",
        icon: <Eye className="w-4 h-4" />
      }
    };

    return metadata[name] || {
      title: "Senior Technical Advisor",
      initials: "👤 AD",
      colorClass: isDark 
        ? "bg-brand-primary/10 border-brand-primary/30 text-brand-primary" 
        : "bg-blue-50 border-blue-300 text-blue-700",
      icon: <UserCheck className="w-4 h-4" />
    };
  };

  const handleToggleReview = (idx) => {
    setExpandedReview(expandedReview === idx ? null : idx);
  };

  return (
    <div className="space-y-6">
      
      {/* Tabs Menu Selector */}
      <div className="flex border-b border-border-color">
        <button
          onClick={() => setActiveTab('boardroom')}
          className={`pb-3 px-4 text-xs font-black tracking-widest uppercase transition-all duration-200 border-b-2 -mb-[2px] cursor-pointer ${
            activeTab === 'boardroom'
              ? 'border-brand-purple text-brand-purple void-glow'
              : 'border-transparent text-text-muted hover:text-text-main'
          }`}
        >
          Executive Boardroom
        </button>
        <button
          onClick={() => setActiveTab('clashes')}
          className={`pb-3 px-4 text-xs font-black tracking-widest uppercase transition-all duration-200 border-b-2 -mb-[2px] cursor-pointer ${
            activeTab === 'clashes'
              ? 'border-brand-purple text-brand-purple void-glow'
              : 'border-transparent text-text-muted hover:text-text-main'
          }`}
        >
          Adversarial Debates Clashes
        </button>
      </div>

      {/* Critiques Layout (COLLAPSIBLE STACKED REVIEW PANELS) */}
      {activeTab === 'boardroom' && (
        <div className="space-y-3">
          {expertReviews.map((review, idx) => {
            const meta = getAgentMetadata(review.expert_name);
            const isExpanded = expandedReview === idx;

            // Generate a clean summary review tag based on name and rating
            let summaryStatus = "Review pending";
            let statusColor = "text-text-muted";
            if (review.rating >= 8) {
              summaryStatus = "Concerned";
              statusColor = "text-brand-danger";
            } else if (review.rating >= 5) {
              summaryStatus = "Cautionary";
              statusColor = "text-brand-warning";
            } else {
              summaryStatus = "Approved";
              statusColor = "text-brand-success";
            }

            return (
              <div 
                key={idx} 
                onClick={() => handleToggleReview(idx)}
                className={`glass-card p-4 border border-border-color bg-card hover:border-brand-purple/40 transition-all duration-200 cursor-pointer shadow-sm ${
                  isExpanded ? 'ring-1 ring-brand-purple/20' : ''
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {/* Avatar Icon */}
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center border font-mono font-bold text-xs ${meta.colorClass}`}>
                      {meta.icon}
                    </div>
                    <div>
                      <h4 className="font-extrabold text-xs text-text-main tracking-wide uppercase flex items-center space-x-2">
                        <span>{review.expert_name}</span>
                        <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded bg-bg uppercase border border-border-color ${statusColor}`}>
                          {summaryStatus}
                        </span>
                      </h4>
                      <span className="text-[9px] text-text-muted uppercase font-semibold">
                        {meta.title}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    <div className="px-2 py-0.5 rounded bg-bg border border-border-color text-[9px] font-bold text-text-main font-mono">
                      Rating: <span className={review.rating >= 8 ? 'text-brand-danger' : 'text-brand-success'}>{review.rating}/10</span>
                    </div>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-text-muted" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-text-muted" />
                    )}
                  </div>
                </div>

                {/* Collapsible Critique Area */}
                <div className={`transition-all duration-300 overflow-hidden ${
                  isExpanded ? 'max-h-96 mt-4 pt-4 border-t border-border-color/60 opacity-100' : 'max-h-0 opacity-0'
                }`}>
                  <p className="text-xs text-text-muted leading-relaxed text-justify italic font-medium pl-3 border-l-2 border-brand-purple">
                    "{review.critique}"
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Chat Bubble Dialogue Clashes */}
      {activeTab === 'clashes' && (
        <div className="space-y-6 bg-bg/80 p-5 border border-border-color rounded-2xl max-h-[500px] overflow-y-auto">
          {Array.isArray(boardDisagreements) && boardDisagreements.length > 0 ? (
            boardDisagreements.map((dis, idx) => (
              <div key={idx} className="space-y-4">
                
                {/* Debate Topic Tag */}
                <div className="flex items-center space-x-2 bg-brand-purple/10 border border-brand-purple/20 px-3 py-1.5 rounded-full w-fit text-[10px] font-bold text-brand-purple uppercase tracking-widest mx-auto shadow-sm">
                  <Compass className="w-3.5 h-3.5" />
                  <span>Clash Debate: {dis.clash}</span>
                </div>

                {/* Styled Chat Bubble Thread */}
                <div className="space-y-4 pt-2">
                  {dis.dialogue.split("The ").map((part, i) => {
                    if (!part.trim()) return null;
                    const speakerMatch = part.match(/^([A-Za-z\s]+)(urges:|fires back:|responds:|warns:|objects:|objects to:)\s*(.*)/i);
                    
                    if (speakerMatch) {
                      const speaker = speakerMatch[1].trim();
                      const tone = speakerMatch[2].trim();
                      const message = speakerMatch[3].trim().replace(/"$/, ''); // strip trailing quote
                      
                      const meta = getAgentMetadata(speaker);
                      const isInvestor = speaker.toLowerCase().includes('investor');

                      return (
                        <div 
                          key={i} 
                          className={`flex items-start space-x-3 max-w-[85%] ${
                            isInvestor ? 'ml-auto flex-row-reverse space-x-reverse' : 'mr-auto'
                          }`}
                        >
                          {/* Chat Avatar */}
                          <div className={`w-8 h-8 rounded-full border flex items-center justify-center shrink-0 font-mono font-bold text-[10px] bg-card ${meta.colorClass}`}>
                            {meta.initials.split(" ")[1] || meta.initials}
                          </div>

                          {/* Speech Bubble */}
                          <div className={`p-4 rounded-2xl border text-xs leading-relaxed shadow-sm ${
                            isInvestor 
                              ? 'bg-brand-purple/10 border-brand-purple/30 text-text-main rounded-tr-none' 
                              : 'bg-card border-border-color text-text-muted rounded-tl-none'
                          }`}>
                            <div className="flex items-center space-x-1.5 mb-1 text-[10px] font-bold uppercase tracking-wider">
                              <span className={isInvestor ? 'text-brand-purple' : 'text-text-main'}>{speaker}</span>
                              <span className="text-[8px] text-text-muted lowercase italic">({tone})</span>
                            </div>
                            <p className="text-[11px] leading-relaxed">"{message}"</p>
                          </div>
                        </div>
                      );
                    }
                    return (
                      <div key={i} className="text-center text-[10px] text-text-muted italic">
                        "{part}"
                      </div>
                    );
                  })}
                </div>
                
                {idx < boardDisagreements.length - 1 && (
                  <hr className="border-border-color/40 my-6" />
                )}
              </div>
            ))
          ) : (
            <div className="text-center text-xs text-text-muted">No primary conflicts registered. Board consensus is unified.</div>
          )}
        </div>
      )}
      
    </div>
  );
}
