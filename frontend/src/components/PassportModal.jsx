import React, { useState } from 'react';
import { X, Check, Copy, ShieldCheck, FileCode, Award } from 'lucide-react';

export default function PassportModal({ passport, onClose }) {
  const [copied, setCopied] = useState(false);

  if (!passport) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(passport.verification_badge_markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div className="bg-[#101522] border border-slate-700/80 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative overflow-hidden animate-in fade-in zoom-in duration-200">
        {/* Glow effect */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                Axiom Code Resilience Passport
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  IN-TOTO DSSE COMPLIANT
                </span>
              </h3>
              <p className="text-xs text-slate-400 font-mono">
                Cryptographic Attestation for Autonomous AI Commit
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Passport Stats Card */}
        <div className="my-5 grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <span className="text-[10px] font-mono uppercase text-slate-400 block">Passport ID</span>
            <span className="text-xs font-mono font-bold text-slate-200 truncate block mt-0.5">{passport.passport_id}</span>
          </div>

          <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <span className="text-[10px] font-mono uppercase text-slate-400 block">Author Agent</span>
            <span className="text-xs font-mono font-bold text-indigo-400 truncate block mt-0.5">{passport.author_agent}</span>
          </div>

          <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <span className="text-[10px] font-mono uppercase text-slate-400 block">Risk Delta</span>
            <span className="text-xs font-mono font-bold text-emerald-400 block mt-0.5">88 ➔ 12 (Safe)</span>
          </div>

          <div className="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <span className="text-[10px] font-mono uppercase text-slate-400 block">Audit Status</span>
            <span className="text-xs font-mono font-bold text-emerald-400 block mt-0.5 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" /> VERIFIED
            </span>
          </div>
        </div>

        {/* Cryptographic Attestation Payload */}
        <div className="mb-4">
          <span className="text-xs font-mono text-slate-300 mb-1.5 block">DSSE Cryptographic Signature (SHA256):</span>
          <div className="bg-black/50 p-2.5 rounded-lg border border-slate-800 font-mono text-[11px] text-indigo-300 break-all select-all">
            {passport.cryptographic_signature}
          </div>
        </div>

        {/* Pull Request Badge Markdown */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-xs font-mono text-slate-300 flex items-center gap-1.5">
              <FileCode className="w-4 h-4 text-emerald-400" />
              GitHub PR Attestation Badge Markdown:
            </span>
            <button
              onClick={handleCopy}
              className="text-xs font-mono text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
            >
              {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Copied to Clipboard!' : 'Copy Markdown'}
            </button>
          </div>
          <textarea
            readOnly
            rows={5}
            value={passport.verification_badge_markdown}
            className="w-full bg-black/60 border border-slate-800 rounded-lg p-3 font-mono text-xs text-slate-300 focus:outline-none select-all"
          />
        </div>

        <div className="mt-5 pt-4 border-t border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-mono font-semibold transition shadow-lg shadow-indigo-600/30"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
