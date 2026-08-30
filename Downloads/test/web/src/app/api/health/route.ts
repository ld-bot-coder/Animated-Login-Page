import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  const ok = Boolean(process.env.OLLAMA_API_KEY) || Boolean(process.env.FEATHERLESS_API_KEY) || Boolean(process.env.OPENROUTER_API_KEY);
  return NextResponse.json(
    {
      status: ok ? "ok" : "degraded",
      provider: process.env.OLLAMA_API_KEY ? "ollama" : process.env.FEATHERLESS_API_KEY ? "featherless" : process.env.OPENROUTER_API_KEY ? "openrouter" : "none",
      uptime: Math.round(process.uptime()),
      ts: new Date().toISOString(),
    },
    { status: 200 }
  );
}