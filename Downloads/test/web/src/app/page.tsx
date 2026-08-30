"use client";

import { useState } from "react";
import { Console } from "@/components/Console";
import { AGENT_UI } from "@/lib/agent-ui";
import { Plus, Pause, CheckCircle, CircleNotch, WarningCircle } from "@phosphor-icons/react";

interface Session {
  id: string;
  title: string;
  status: string;
}

export default function Home() {
  const [sessions, setSessions] = useState<Session[]>([
    { id: "default", title: "New Case", status: "Idle" }
  ]);
  const [activeSessionId, setActiveSessionId] = useState("default");

  const handleNewSession = () => {
    const id = Math.random().toString(36).substring(2, 9);
    setSessions((s) => [...s, { id, title: "New Case", status: "Idle" }]);
    setActiveSessionId(id);
  };

  const updateSession = (id: string, updates: Partial<Session>) => {
    setSessions((s) =>
      s.map((session) => (session.id === id ? { ...session, ...updates } : session))
    );
  };

  return (
    <div className="flex h-[100dvh] overflow-hidden bg-[#FAFBFA]">
      {/* Sidebar for Sessions */}
      <aside className="w-64 flex-shrink-0 border-r border-navy/10 bg-white p-4 flex flex-col gap-4 overflow-hidden">
        <div className="flex items-center gap-2 mb-2 px-2">
          <StarMark />
          <span className="font-bold tracking-tight text-navy">Cases</span>
        </div>
        
        <button
          onClick={handleNewSession}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-navy px-4 py-2.5 text-sm font-medium text-white transition hover:bg-navy/90 active:scale-[0.98]"
        >
          <Plus size={16} weight="bold" />
          New Cascade
        </button>

        <div className="flex flex-col gap-2 overflow-y-auto pb-4 mt-2 pr-1">
          {sessions.map((session) => (
            <button
              key={session.id}
              onClick={() => setActiveSessionId(session.id)}
              className={`flex flex-col gap-1.5 rounded-xl border p-3 text-left transition-all ${
                activeSessionId === session.id
                  ? "border-navy/20 bg-cream-soft/60 shadow-sm"
                  : "border-transparent bg-transparent hover:bg-navy/5"
              }`}
            >
              <div className="w-full truncate text-sm font-medium text-navy">
                {session.title || "New Case"}
              </div>
              <div className="flex items-center gap-1.5 text-xs font-medium text-navy/60">
                {session.status === "Running" && (
                  <CircleNotch className="animate-spin text-triage" size={12} weight="bold" />
                )}
                {session.status === "Paused" && <Pause size={12} weight="fill" className="text-amber-500" />}
                {session.status === "Done" && <CheckCircle size={12} weight="fill" className="text-emerald-500" />}
                {session.status === "Error" && <WarningCircle size={12} weight="fill" className="text-red-500" />}
                {session.status}
              </div>
            </button>
          ))}
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto min-w-0">
        <div className="mx-auto max-w-[1480px] px-5 py-8 md:px-8">
          {/* Header — asymmetric, premium brand header with star mark & active protocol board */}
          <header className="mb-8 flex flex-col gap-5 border-b border-navy/10 pb-6 md:flex-row md:items-center md:justify-between">
            <div>
              <div className="mb-2 flex items-center gap-2.5">
                <StarMark />
                <span className="font-mono text-[10px] font-semibold uppercase tracking-[0.25em] text-navy/45">
                  Clinical AI System
                </span>
                <span className="h-1 w-1 rounded-full bg-navy/20" />
                <span className="flex items-center gap-1 font-mono text-[10px] font-semibold uppercase tracking-[0.2em] text-emerald-600">
                  <span className="relative flex h-1.5 w-1.5">
                    <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
                  </span>
                  active protocol
                </span>
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-navy">
                MedPulse Console
              </h1>
              <p className="mt-1 text-sm text-navy/60">
                Autonomous multi-agent clinical coordination and human-in-the-loop safety guardrails.
              </p>
            </div>

            {/* Live connected agent roster grid */}
            <div className="flex flex-wrap items-center gap-2 rounded-2xl border border-navy-line bg-cream-soft/40 p-2 md:gap-3">
              <div className="flex flex-wrap gap-1.5">
                <div className="flex items-center gap-1.5 rounded-lg border border-triage/15 bg-triage/[0.04] px-2.5 py-1 text-navy">
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-triage" />
                  <div className="flex flex-col">
                    <span className="font-mono text-[9px] font-medium leading-none text-navy/50 uppercase">Triage</span>
                    <span className="font-sans text-[11px] font-semibold leading-tight text-triage">{AGENT_UI.triage.model}</span>
                  </div>
                </div>
                <div className="flex items-center gap-1.5 rounded-lg border border-mgmt/15 bg-mgmt/[0.04] px-2.5 py-1 text-navy">
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-mgmt" />
                  <div className="flex flex-col">
                    <span className="font-mono text-[9px] font-medium leading-none text-navy/50 uppercase">Planning</span>
                    <span className="font-sans text-[11px] font-semibold leading-tight text-mgmt">{AGENT_UI.management.model}</span>
                  </div>
                </div>
                <div className="flex items-center gap-1.5 rounded-lg border border-invest/15 bg-invest/[0.04] px-2.5 py-1 text-navy">
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-invest" />
                  <div className="flex flex-col">
                    <span className="font-mono text-[9px] font-medium leading-none text-navy/50 uppercase">Tests</span>
                    <span className="font-sans text-[11px] font-semibold leading-tight text-invest">{AGENT_UI.investigation.model}</span>
                  </div>
                </div>
                <div className="flex items-center gap-1.5 rounded-lg border border-doc/15 bg-doc/[0.04] px-2.5 py-1 text-navy">
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-doc" />
                  <div className="flex flex-col">
                    <span className="font-mono text-[9px] font-medium leading-none text-navy/50 uppercase">EHR Note</span>
                    <span className="font-sans text-[11px] font-semibold leading-tight text-doc">{AGENT_UI.documentation.model}</span>
                  </div>
                </div>
                <div className="flex items-center gap-1.5 rounded-lg border border-observer/15 bg-observer/[0.04] px-2.5 py-1 text-navy">
                  <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-observer" />
                  <div className="flex flex-col">
                    <span className="font-mono text-[9px] font-medium leading-none text-navy/50 uppercase">Auditor</span>
                    <span className="font-sans text-[11px] font-semibold leading-tight text-observer">{AGENT_UI.observer.model}</span>
                  </div>
                </div>
              </div>
              <div className="hidden border-l border-navy/10 pl-3 md:block">
                <div className="font-mono text-[9px] font-medium uppercase leading-none tracking-wider text-navy/40">
                  platform
                </div>
                <div className="text-sm font-bold tracking-tight text-navy">Ollama · Band SDK</div>
              </div>
            </div>
          </header>

          {sessions.map((session) => (
            <Console
              key={session.id}
              isActive={activeSessionId === session.id}
              onStatusChange={(status) => updateSession(session.id, { status })}
              onTitleChange={(title) => updateSession(session.id, { title })}
            />
          ))}
        </div>
      </main>
    </div>
  );
}

function StarMark() {
  // Medical cross mark — the brand's clinical identity.
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true" className="shrink-0">
      <rect x="8.5" y="1.5" width="7" height="21" rx="1.5" fill="#0D4A45" />
      <rect x="1.5" y="8.5" width="21" height="7" rx="1.5" fill="#0D4A45" />
    </svg>
  );
}
