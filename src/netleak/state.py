"""
Persistent state tracking for NetLeak Guard.

Every engine that makes a real change to the system (firewall rules,
honeytoken watchers, telemetry redirection) records that change here so
that `status` reflects what has actually happened in this environment,
rather than a hardcoded "ACTIVE" string.

State lives at ~/.netleak/state.json.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path.home() / ".netleak"
STATE_FILE = STATE_DIR / "state.json"

_DEFAULT_STATE = {
    "rate_limit_rules": [],      # list of {"port": int, "platform": str, "rule": str}
    "telemetry_isolated": False,
    "honeytokens": [],           # list of {"path": str, "watching": bool}
    "header_obfuscation_generated": False,
    "last_monitor_scan": None,
}


class StateManager:
    def __init__(self):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self._state = self._load()

    def _load(self) -> dict:
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)
                merged = dict(_DEFAULT_STATE)
                merged.update(data)
                return merged
            except (json.JSONDecodeError, OSError):
                pass
        return dict(_DEFAULT_STATE)

    def _save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self._state, f, indent=2)

    # --- rate limiting -----------------------------------------------
    def add_rate_limit_rule(self, port: int, platform: str, rule: str):
        self._state["rate_limit_rules"].append({
            "port": port, "platform": platform, "rule": rule,
            "applied_at": datetime.now(timezone.utc).isoformat(),
        })
        self._save()

    def clear_rate_limit_rules(self):
        rules = self._state["rate_limit_rules"]
        self._state["rate_limit_rules"] = []
        self._save()
        return rules

    def set_telemetry_isolated(self, value: bool):
        self._state["telemetry_isolated"] = value
        self._save()

    # --- prevent -------------------------------------------------------
    def add_honeytoken(self, path: str, watching: bool):
        self._state["honeytokens"].append({"path": path, "watching": watching})
        self._save()

    def set_header_obfuscation_generated(self, value: bool):
        self._state["header_obfuscation_generated"] = value
        self._save()

    # --- monitor ---------------------------------------------------------
    def record_monitor_scan(self):
        self._state["last_monitor_scan"] = datetime.now(timezone.utc).isoformat()
        self._save()

    @property
    def snapshot(self) -> dict:
        return dict(self._state)
