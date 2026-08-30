import type { Config } from "tailwindcss";

// Palette: Clinical mint-white base + deep medical teal ink/accent.
// Light, clean healthcare theme with red urgency accents.
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        cream: {
          DEFAULT: "#F2F8F6", // clinical mint-white base
          deep: "#E6F1EE", // slightly deeper for surfaces/lines
          soft: "#F8FCFB", // lighter for raised cards
        },
        navy: {
          DEFAULT: "#0D4A45", // deep medical teal ink + accent
          soft: "#14605A",
          line: "#CCDFDA", // hairline on mint
        },
        // Per-agent accents, tuned to sit on the clinical mint base.
        triage: "#D8443C", // urgency red
        mgmt: "#0E8C7F", // care-planning teal
        invest: "#2E6FA3", // diagnostic blue
        doc: "#3F8A54", // EHR green
        observer: "#B0891E", // audit amber
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "ui-monospace", "monospace"],
      },
      keyframes: {
        shimmer: { "100%": { transform: "translateX(100%)" } },
        breathe: {
          "0%, 100%": { opacity: "0.35" },
          "50%": { opacity: "1" },
        },
      },
      animation: {
        shimmer: "shimmer 1.6s infinite",
        breathe: "breathe 2s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
