import React, { useState, useEffect } from 'react';
import {
  Shield, AlertTriangle, CheckCircle, Zap, Flame, Award, GitPullRequest,
  RefreshCw, Code, Layers, FileText, ChevronRight, Terminal as TerminalIcon
} from 'lucide-react';

import BlastRadiusGraph from './components/BlastRadiusGraph';
import InvariantList from './components/InvariantList';
import TerminalView from './components/TerminalView';
import PassportModal from './components/PassportModal';

export default function App() {
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState('billing_transfer');
  const [analysisData, setAnalysisData] = useState(null);
  const [fuzzData, setFuzzData] = useState(null);
  const [isRemediated, setIsRemediated] = useState(false);
  const [isFuzzing, setIsFuzzing] = useState(false);
  const [isRemediating, setIsRemediating] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard'); // 'dashboard' or 'code_diff'
  const [remediationDiff, setRemediationDiff] = useState(null);
  const [passport, setPassport] = useState(null);
  const [showPassport, setShowPassport] = useState(false);

  // Load scenarios on mount
  useEffect(() => {
    fetch('/api/scenarios')
      .then((res) => res.json())
      .then((data) => {
        setScenarios(data);
      })
      .catch((err) => console.error('Failed to load scenarios:', err));
  }, []);

  // Run initial analysis whenever scenario changes
  useEffect(() => {
    setIsRemediated(false);
    setFuzzData(null);
    setRemediationDiff(null);

    fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id: selectedScenario }),
    })
      .then((res) => res.json())
      .then((data) => {
        setAnalysisData(data);
      })
      .catch((err) => console.error('Analyze failed:', err));
  }, [selectedScenario]);

  // Execute Adversarial Fuzzing
  const handleRunFuzz = () => {
    setIsFuzzing(true);
    fetch('/api/fuzz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scenario_id: selectedScenario,
        code_mode: isRemediated ? 'hardened' : 'vulnerable',
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setFuzzData(data);
        setIsFuzzing(false);
      })
      .catch((err) => {
        console.error('Fuzz failed:', err);
        setIsFuzzing(false);
      });
  };

  // Trigger IBM Bob Remediation Loop
  const handleRemediate = () => {
    setIsRemediating(true);
    fetch('/api/remediate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_id: selectedScenario }),
    })
      .then((res) => res.json())
      .then((data) => {
        setRemediationDiff(data);
        setIsRemediated(true);
        setIsRemediating(false);

        // Auto-re-run fuzz suite to prove it's defended
        fetch('/api/fuzz', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            scenario_id: selectedScenario,
            code_mode: 'hardened',
          }),
        })
          .then((res) => res.json())
          .then((fuzzRes) => {
            setFuzzData(fuzzRes);
          });
      })
      .catch((err) => {
        console.error('Remediate failed:', err);
        setIsRemediating(false);
      });
  };

  // Load and open Passport
  const handleOpenPassport = () => {
    fetch(`/api/passport/${selectedScenario}`)
      .then((res) => res.json())
      .then((data) => {
        setPassport(data);
        setShowPassport(true);
      });
  };

  const currentScenarioObj = scenarios.find((s) => s.id === selectedScenario);

  return (
    <div className="min-h-screen bg-[#0a0e17] text-slate-100 flex flex-col font-['Plus_Jakarta_Sans',sans-serif]">
      {/* Top Navbar */}
      <header className="border-b border-slate-800/80 bg-[#0d121f]/90 backdrop-blur-md sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-blue-500 flex items-center justify-center shadow-lg shadow-indigo-600/30">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-base tracking-tight text-white font-mono">AXIOM</span>
              <span className="text-[10px] font-mono uppercase bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 px-2 py-0.5 rounded-full font-bold">
                v2.0 Enterprise
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-mono">
              Adversarial Invariant & Blast-Radius Firewall for AI Devs
            </p>
          </div>
        </div>

        {/* Center: Scenario Selector */}
        <div className="flex items-center space-x-2 bg-slate-900/80 p-1.5 rounded-xl border border-slate-800">
          <span className="text-xs font-mono text-slate-400 pl-2">Target Scenario:</span>
          <select
            value={selectedScenario}
            onChange={(e) => setSelectedScenario(e.target.value)}
            className="bg-black/60 text-slate-200 text-xs font-mono rounded-lg px-3 py-1.5 border border-slate-700/80 focus:outline-none focus:border-indigo-500"
          >
            {scenarios.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </div>

        {/* Right Action: Resilience Passport */}
        <div className="flex items-center space-x-3">
          <button
            onClick={handleOpenPassport}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-mono font-semibold transition shadow-lg ${
              isRemediated
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-600/30'
                : 'bg-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Award className="w-4 h-4" />
            {isRemediated ? 'VIEW RESILIENCE PASSPORT' : 'EXPORT ATTESTATION'}
          </button>
        </div>
      </header>

      {/* Breadcrumb / PR Context Strip */}
      <div className="bg-[#0e1322] border-b border-slate-800 px-6 py-2.5 flex items-center justify-between text-xs font-mono text-slate-400">
        <div className="flex items-center space-x-4">
          <span className="flex items-center gap-1.5 text-slate-300">
            <GitPullRequest className="w-3.5 h-3.5 text-indigo-400" />
            PR #104: feat(billing): AI-assisted wallet transfer endpoint
          </span>
          <span className="text-slate-600">|</span>
          <span>Target: <code className="text-indigo-300">{currentScenarioObj?.target_file}</code></span>
          <span className="text-slate-600">|</span>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            AI Dev Partner: <strong className="text-slate-200 font-semibold">IBM Bob 2.0</strong>
          </span>
        </div>

        {/* View Toggle */}
        <div className="flex items-center space-x-1 bg-black/40 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-3 py-1 rounded text-xs font-mono transition ${
              activeTab === 'dashboard' ? 'bg-indigo-600 text-white font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Auditor View
          </button>
          <button
            onClick={() => setActiveTab('code_diff')}
            className={`px-3 py-1 rounded text-xs font-mono transition ${
              activeTab === 'code_diff' ? 'bg-indigo-600 text-white font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Code & Unified Diff
          </button>
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Top Pipeline Flow Bar */}
        <div className="bg-[#111827]/70 border border-slate-800 rounded-xl p-4 flex items-center justify-between font-mono text-xs shadow-lg">
          <div className="flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-[11px] border border-indigo-500/40">1</span>
            <span className="text-slate-300 font-semibold">IBM Bob Generates Code</span>
            <ChevronRight className="w-4 h-4 text-slate-600 ml-2" />
          </div>

          <div className="flex items-center gap-2">
            <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-[11px] border border-amber-500/40">2</span>
            <span className="text-slate-300 font-semibold">Axiom Mines Unstated Invariants</span>
            <ChevronRight className="w-4 h-4 text-slate-600 ml-2" />
          </div>

          <div className="flex items-center gap-2">
            <span className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-[11px] border ${
              fuzzData ? 'bg-rose-500/20 text-rose-400 border-rose-500/40' : 'bg-slate-800 text-slate-500 border-slate-700'
            }`}>3</span>
            <span className={fuzzData ? 'text-slate-300 font-semibold' : 'text-slate-500'}>Adversarial Fuzzing Triggered</span>
            <ChevronRight className="w-4 h-4 text-slate-600 ml-2" />
          </div>

          <div className="flex items-center gap-2">
            <span className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-[11px] border ${
              isRemediated ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40' : 'bg-slate-800 text-slate-500 border-slate-700'
            }`}>4</span>
            <span className={isRemediated ? 'text-emerald-300 font-bold' : 'text-slate-500'}>Self-Healing Patch Verified</span>
          </div>
        </div>

        {activeTab === 'dashboard' ? (
          <>
            {/* 1. Topology & Blast Radius Graph */}
            {analysisData && (
              <BlastRadiusGraph
                blastRadius={analysisData.blast_radius}
                isRemediated={isRemediated}
              />
            )}

            {/* 2. Invariant & Ghost Assumption Matrix */}
            {analysisData && (
              <InvariantList
                invariants={analysisData.detected_invariants}
                isRemediated={isRemediated}
                onRunFuzz={handleRunFuzz}
                isFuzzing={isFuzzing}
              />
            )}

            {/* 3. Live Adversarial Execution Sandbox */}
            <TerminalView
              fuzzResponse={fuzzData}
              onRemediate={handleRemediate}
              isRemediating={isRemediating}
              isRemediated={isRemediated}
            />
          </>
        ) : (
          /* Code & Unified Diff View */
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-[#111827] border border-slate-800 rounded-xl p-5 shadow-2xl">
              <h3 className="font-mono text-xs uppercase tracking-wider text-rose-400 font-bold mb-3 flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
                Vulnerable Code (IBM Bob Initial Generation)
              </h3>
              <pre className="bg-black/60 p-4 rounded-lg font-mono text-xs text-slate-300 overflow-x-auto leading-relaxed border border-slate-800/80">
                {currentScenarioObj?.vulnerable_code}
              </pre>
            </div>

            <div className="bg-[#111827] border border-slate-800 rounded-xl p-5 shadow-2xl">
              <h3 className="font-mono text-xs uppercase tracking-wider text-emerald-400 font-bold mb-3 flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                Hardened Code (Axiom Zero-Trust Remediation)
              </h3>
              <pre className="bg-black/60 p-4 rounded-lg font-mono text-xs text-slate-300 overflow-x-auto leading-relaxed border border-slate-800/80">
                {currentScenarioObj?.hardened_code}
              </pre>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#0d121f] py-4 px-6 text-center text-xs font-mono text-slate-500">
        AXIOM SENTINEL v2.0 • Built for the IBM Bob 2.0 Hackathon on lablab.ai • Zero-Trust AI Invariant Verification
      </footer>

      {/* Passport Modal */}
      {showPassport && (
        <PassportModal passport={passport} onClose={() => setShowPassport(false)} />
      )}
    </div>
  );
}
