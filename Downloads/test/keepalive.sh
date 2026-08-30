#!/bin/sh
set -e

# MedPulse keep-alive. Render pays per minute a build is running, so this image
# is a thin curl wrapper that fetches the health endpoint of the web service
# once and exits. The cron job (every 5 min) keeps the free instance awake.

URL="$HEALTH_URL"
if [ -z "$URL" ]; then
  echo "keepalive: HEALTH_URL unset — nothing to ping" >&2
  exit 1
fi

echo "keepalive: pinging $URL"
curl -fsS -m 20 -o /dev/null -w "keepalive: HTTP %{http_code} in %{time_total}s\n" "$URL" || {
  echo "keepalive: ping failed" >&2
  exit 1
}