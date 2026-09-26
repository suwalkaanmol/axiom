import React from 'react';
import { Database, Globe, Server, Radio, Mail, AlertTriangle, ShieldCheck, ArrowRight } from 'lucide-react';

export default function BlastRadiusGraph({ blastRadius, isRemediated }) {
  if (!blastRadius || !blastRadius.nodes) return null;

  const getNodeIcon = (type) => {
    switch (type) {
      case 'database':
        return <Database className="w-5 h-5" />;
      case 'external_api':
        return <Globe className="w-5 h-5" />;
      case 'queue':
        return <Radio className="w-5 h-5" />;
      case 'service':
        return <Server className="w-5 h-5" />;
      case 'client':
        return <Globe className="w-5 h-5" />;
      default:
        return <Server className="w-5 h-5" />;
    }
  };

  return (
    <div className="bg-[#111827]/90 border border-slate-800 rounded-xl p-5 shadow-2xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg ${isRemediated ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
            {isRemediated ? <ShieldCheck className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
          </div>
          <div>
            <h3 className="font-semibold text-slate-100 flex items-center gap-2">
              System Topology & Blast Radius
              <span className={`text-xs px-2 py-0.5 rounded-full font-mono ${
                isRemediated ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
              }`}>
                {isRemediated ? 'Risk Score: 12/100 (Safe)' : `Risk Score: ${blastRadius.risk_score}/100 (Critical)`}
              </span>
            </h3>
            <p className="text-xs text-slate-400">
              {isRemediated 
                ? 'All downstream contracts secured against invariant breaches.' 
                : '2 dependency tiers vulnerable to unstated AI assumptions.'}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-rose-500"></span> Vulnerable</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-amber-500"></span> Impacted</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-emerald-500"></span> Secured</span>
        </div>
      </div>

      {/* Topology Nodes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-4">
        {blastRadius.nodes.map((node) => {
          const isCritical = !isRemediated && node.status === 'critical';
          const isImpacted = !isRemediated && node.status === 'impacted';
          const isSafe = isRemediated || node.status === 'safe';

          return (
            <div
              key={node.id}
              className={`p-4 rounded-xl border transition-all duration-300 relative ${
                isCritical
                  ? 'bg-rose-950/20 border-rose-500/60 node-critical'
                  : isImpacted
                  ? 'bg-amber-950/20 border-amber-500/50'
                  : 'bg-slate-900/60 border-slate-800 node-safe'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2.5">
                  <div className={`p-2 rounded-lg ${
                    isCritical ? 'bg-rose-500/20 text-rose-400' :
                    isImpacted ? 'bg-amber-500/20 text-amber-400' :
                    'bg-emerald-500/20 text-emerald-400'
                  }`}>
                    {getNodeIcon(node.type)}
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-slate-200">{node.label}</h4>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400">{node.type}</span>
                  </div>
                </div>

                <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full ${
                  isCritical ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' :
                  isImpacted ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                  'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                }`}>
                  {isRemediated ? 'SECURED' : node.status.toUpperCase()}
                </span>
              </div>

              <p className="mt-3 text-xs text-slate-400 font-mono leading-relaxed bg-black/30 p-2 rounded-lg border border-slate-800/80">
                {node.details}
              </p>
            </div>
          );
        })}
      </div>

      {/* Impact Summary Banner */}
      <div className={`mt-4 p-3 rounded-lg border flex items-center gap-3 text-xs font-mono ${
        isRemediated 
          ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-300' 
          : 'bg-rose-950/30 border-rose-500/40 text-rose-300'
      }`}>
        <ArrowRight className="w-4 h-4 shrink-0" />
        <span>{blastRadius.impact_summary}</span>
      </div>
    </div>
  );
}
