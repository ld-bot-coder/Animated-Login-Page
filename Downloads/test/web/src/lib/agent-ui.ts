// Client-side agent display metadata: label, icon name, accent color.
// Icons resolved in components via @phosphor-icons/react.

import type { AgentId } from "./types";

export interface AgentUi {
  label: string;
  short: string;
  accent: string; // tailwind text/border color token
  hex: string;
  model: string; // display-only Ollama model shown per agent role
}

export const AGENT_UI: Record<AgentId, AgentUi> = {
  triage: { label: "Triage Agent", short: "Triage", accent: "triage", hex: "#D8443C", model: "llama3.3:70b" },
  management: { label: "Management Agent", short: "Management", accent: "mgmt", hex: "#0E8C7F", model: "deepseek-r1:70b" },
  investigation: { label: "Investigation Agent", short: "Investigation", accent: "invest", hex: "#2E6FA3", model: "gemma3:27b" },
  documentation: { label: "Documentation Agent", short: "Documentation", accent: "doc", hex: "#3F8A54", model: "qwen3:32b" },
  observer: { label: "Observer", short: "Audit", accent: "observer", hex: "#B0891E", model: "mistral:24b" },
};

export const PIPELINE: AgentId[] = [
  "triage",
  "management",
  "investigation",
  "documentation",
  "observer",
];

export const SAMPLE_CASE =
  '67yo female, sudden onset severe headache 10/10 "worst of my life", neck stiffness, photophobia, fever 38.9°C, GCS 14. BP 158/94, HR 102, RR 20, SpO2 97% on air. No known allergies. No prior headache history.';
