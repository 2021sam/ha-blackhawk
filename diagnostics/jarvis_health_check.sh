#!/bin/sh

cd /root/homeassistant || exit 1

HA_URL="${HA_URL:-http://homeassistant.local:8123}"
JARVIS_URL="${JARVIS_URL:-http://localhost:8001}"

mkdir -p diagnostics/logs

LOG="diagnostics/logs/jarvis_$(date +%Y%m%d_%H%M%S).log"

check_url() {
    name="$1"
    url="$2"

    response=$(curl -sS --max-time 8 \
        -o /dev/null -w '%{http_code}' "$url" 2>/dev/null)
    rc=$?

    if [ "$rc" -eq 0 ] &&
       [ "$response" -ge 200 ] &&
       [ "$response" -lt 300 ]; then
        echo "PASS: $name (HTTP $response)"
    else
        echo "FAIL: $name (HTTP $response, curl exit $rc)"
    fi
}

{
    echo "=================================="
    echo " JARVIS HEALTH CHECK"
    echo " $(date)"
    echo "=================================="

    check_url "Home Assistant" "$HA_URL/"
    check_url "Jarvis API" "$JARVIS_URL/health"

    echo
    echo "--- Yamaha receivers ---"

    python3 - <<'PY'
import json
import urllib.request

path = ".storage/core.config_entries"

with open(path) as f:
    data = json.load(f)

for entry in data["data"]["entries"]:
    if entry.get("domain") != "yamaha_musiccast":
        continue

    host = entry.get("data", {}).get("host")
    if not host:
        continue

    url = (
        f"http://{host}/YamahaExtendedControl/"
        "v1/system/getDeviceInfo"
    )

    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            device = json.load(response)

        model = device.get("model_name", "Unknown")
        code = device.get("response_code")

        if code == 0:
            print(f"PASS: Yamaha {model} ({host})")
        else:
            print(f"FAIL: Yamaha {model} ({host}), code {code}")

    except Exception as exc:
        print(f"FAIL: Yamaha ({host}): {exc}")
PY

    echo
    echo "--- Recent Jarvis/Assist errors ---"

    ha core logs --lines 100 2>/dev/null |
        grep -iE 'jarvis|assist_pipeline|tts_proxy|failed to cast' |
        tail -10 || true

    echo
    echo "Diagnostics complete."

} 2>&1 | tee "$LOG"

echo "Saved diagnostic log: $LOG"
