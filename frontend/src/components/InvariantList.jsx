import React from 'react';
import { AlertCircle, CheckCircle2, Flame, ShieldAlert, Cpu } from 'lucide-react';

export default function InvariantList({ invariants, isRemediated, onRunFuzz, isFuzzing }) {
  if (!invariants || invariants.length === 0) return null;

  const getSeverityBadge = (sev) => {
    switch (sev) {
      case 'CRITICAL':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      case 'HIGH':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      default:
        return 'bg-blue-500/20 text-blue-300 border-blue-500/40';
    }
  };

  return (
    <div className="bg-[#111827]/90 border border-slate-800 rounded-xl p-5 shadow-2xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div>
          <h3 className="font-semibold text-slate-100 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-indigo-400" />
            Ghost Assumption & Invariant Audit
            <span className="text-xs px-2.5 py-0.5 rounded-full font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              {invariants.length} Assumptions Extracted
            </span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Unstated behavioral dependencies silently introduced by the AI Dev Partner.
          </p>
        </div>

        <button
          onClick={onRunFuzz}
          disabled={isFuzzing}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold font-mono tracking-wider transition-all duration-200 shadow-lg ${
            isFuzzing
              ? 'bg-slate-800 text-slate-400 cursor-not-allowed'
              : 'bg-rose-600 hover:bg-rose-500 text-white shadow-rose-600/30'
          }`}
        >
          <Flame className={`w-4 h-4 ${isFuzzing ? 'animate-spin' : ''}`} />
          {isFuzzing ? 'ATTACKING ASSUMPTIONS...' : 'EXECUTE ADVERSARIAL FUZZ'}
        </button>
      </div>

      <div className="space-y-3">
        {invariants.map((inv) => {
          return (
            <div
              key={inv.id}
              className={`p-4 rounded-xl border transition-all duration-200 ${
                isRemediated
                  ? 'bg-emerald-950/10 border-emerald-500/30'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-2.5">
                  <div className={`p-1.5 rounded-lg ${isRemediated ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`}>
                    {isRemediated ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-slate-200">{inv.title}</h4>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${getSeverityBadge(inv.severity)}`}>
                        {inv.severity}
                      </span>
                      <span className="text-[10px] font-mono text-slate-400 uppercase">
                        Category: {inv.category}
                      </span>
                      {inv.line_number && (
                        <span className="text-[10px] font-mono text-indigo-400 bg-indigo-950/40 px-2 py-0.5 rounded border border-indigo-800/40">
                          Target Line: #{inv.line_number}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <span className={`text-[10px] font-mono px-2.5 py-1 rounded-full uppercase tracking-wider ${
                  isRemediated
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                    : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                }`}>
                  {isRemediated ? 'DEFENDED & SECURED' : 'VULNERABILITY LIVE'}
                </span>
              </div>

              {/* Assumption Details */}
              <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-black/30 p-2.5 rounded-lg border border-slate-800">
                  <span className="text-[10px] uppercase font-mono tracking-wider text-slate-400 block mb-1">
                    Silent AI Assumption:
                  </span>
                  <p className="text-slate-300 font-mono text-[11px] leading-relaxed">
                    "{inv.implicit_assumption}"
                  </p>
                </div>

                <div className="bg-rose-950/20 p-2.5 rounded-lg border border-rose-900/30">
                  <span className="text-[10px] uppercase font-mono tracking-wider text-rose-400 block mb-1">
                    Exploit / Crash Scenario:
                  </span>
                  <p className="text-rose-200 font-mono text-[11px] leading-relaxed">
                    {inv.exploit_scenario}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
