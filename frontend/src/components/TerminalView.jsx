import React from 'react';
import { Terminal, Shield, Zap, RefreshCw, CheckCircle, XCircle } from 'lucide-react';

export default function TerminalView({ fuzzResponse, onRemediate, isRemediating, isRemediated }) {
  if (!fuzzResponse) return null;

  return (
    <div className="bg-[#0e131f] border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
      {/* Terminal Header */}
      <div className="bg-[#161c2d] px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1.5">
            <div className="w-3 h-3 rounded-full bg-rose-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-amber-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-emerald-500/80"></div>
          </div>
          <span className="text-xs font-mono text-slate-400 pl-2 flex items-center gap-1.5">
            <Terminal className="w-3.5 h-3.5 text-indigo-400" />
            axiom-adversarial-sandbox::pytest-runner [Python 3.14]
          </span>
        </div>

        <div className="flex items-center space-x-3">
          <span className={`text-xs font-mono px-2 py-0.5 rounded-full ${
            fuzzResponse.all_secured
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
              : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
          }`}>
            {fuzzResponse.passed_tests} PASSED / {fuzzResponse.failed_tests} FAILED
          </span>

          {!isRemediated && fuzzResponse.failed_tests > 0 && (
            <button
              onClick={onRemediate}
              disabled={isRemediating}
              className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono font-semibold transition-all duration-200 shadow ${
                isRemediating
                  ? 'bg-indigo-900/50 text-indigo-300 cursor-not-allowed'
                  : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30'
              }`}
            >
              <Zap className={`w-3.5 h-3.5 ${isRemediating ? 'animate-spin' : ''}`} />
              {isRemediating ? 'IBM BOB REMEDIATING...' : 'TRIGGER IBM BOB AUTO-PATCH'}
            </button>
          )}
        </div>
      </div>

      {/* Terminal Body */}
      <div className="p-4 font-mono text-xs overflow-x-auto max-h-[380px] space-y-1">
        <pre className="text-slate-300 whitespace-pre-wrap leading-relaxed">
          {fuzzResponse.terminal_logs}
        </pre>
      </div>

      {/* Test Case Cards */}
      <div className="bg-[#111726] border-t border-slate-800 p-4">
        <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
          <span>Synthesized Invariant Test Executions</span>
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {fuzzResponse.test_results.map((test) => (
            <div
              key={test.test_id}
              className={`p-3 rounded-lg border text-xs font-mono ${
                test.passed
                  ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-300'
                  : 'bg-rose-950/30 border-rose-500/40 text-rose-200'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-bold flex items-center gap-1">
                  {test.passed ? <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> : <XCircle className="w-3.5 h-3.5 text-rose-400" />}
                  {test.test_id}
                </span>
                <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
                  test.passed ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                }`}>
                  {test.passed ? 'PASSED' : 'EXPLOIT TRIGGERED'}
                </span>
              </div>
              <p className="text-[11px] font-semibold text-slate-200 truncate">{test.name}</p>
              <p className="text-[10px] text-slate-400 mt-1 truncate">Target: {test.invariant_targeted}</p>
              <div className="mt-2 text-[10px] bg-black/40 p-1.5 rounded border border-slate-800/80">
                <span className="text-slate-400 block">Actual Outcome:</span>
                <span className="text-slate-300 truncate block">{test.actual_result}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
