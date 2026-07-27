"""
Limit Engine - real, reversible firewall/rate-limit control.

Every rule this engine applies is recorded in StateManager so it can be
listed honestly in `status` and torn down again with `limit revert`.
Destructive actions require explicit confirmation from the caller
(handled in commands.py) before anything touches the system.
"""

import subprocess
import sys
from rich.console import Console

from netleak.state import StateManager

# Common background telemetry/analytics hosts worth loopback-routing.
# Kept small and explicit on purpose - silently rerouting arbitrary
# domains is the kind of thing that breaks things in surprising ways.
TELEMETRY_HOSTS = [
    "telemetry.microsoft.com",
    "watson.telemetry.microsoft.com",
    "google-analytics.com",
    "app-measurement.com",
]

HOSTS_FILE = "/etc/hosts" if not sys.platform == "win32" else r"C:\Windows\System32\drivers\etc\hosts"


class LimitEngine:
    """
    Manages outbound footprint mitigation via platform-specific firewall,
    rate limit, and port blocking controls.
    """

    def __init__(self, console: Console, state: StateManager | None = None):
        self.console = console
        self.state = state or StateManager()

    def _run(self, cmd: list[str]) -> bool:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode != 0:
                self.console.print(f"[danger][-][/danger] Command failed: {' '.join(cmd)}")
                if result.stderr:
                    self.console.print(f"[danger]    {result.stderr.strip()}[/danger]")
                return False
            return True
        except FileNotFoundError:
            self.console.print(f"[danger][-][/danger] Required tool not found for command: {cmd[0]}")
            return False
        except PermissionError:
            self.console.print("[danger][-][/danger] Permission denied. Re-run elevated (sudo/administrator).")
            return False

    def configure_rate_limit(self, ports: list[int], limit_req_per_min: int = 60) -> bool:
        platform = sys.platform
        self.console.print(
            f"[info][*][/info] Applying [accent]{limit_req_per_min} req/min[/accent] limit on ports {ports}."
        )

        applied_any = False
        if platform.startswith("linux"):
            for port in ports:
                set_rule = ["iptables", "-I", "INPUT", "-p", "tcp", "--dport", str(port),
                            "-m", "state", "--state", "NEW", "-m", "recent", "--set"]
                update_rule = ["iptables", "-I", "INPUT", "-p", "tcp", "--dport", str(port),
                               "-m", "state", "--state", "NEW", "-m", "recent", "--update",
                               "--seconds", "60", "--hitcount", str(limit_req_per_min), "-j", "DROP"]
                if self._run(set_rule) and self._run(update_rule):
                    self.state.add_rate_limit_rule(port, "linux", " ".join(update_rule))
                    self.console.print(f"[success][+][/success] iptables rule active on port {port}.")
                    applied_any = True

        elif platform == "win32":
            for port in ports:
                rule_name = f"NetLeakGuard_Limit_{port}"
                cmd = ["netsh", "advfirewall", "firewall", "add", "rule",
                       f"name={rule_name}", "dir=in", "action=block", "protocol=TCP",
                       f"localport={port}"]
                if self._run(cmd):
                    self.state.add_rate_limit_rule(port, "win32", rule_name)
                    self.console.print(f"[success][+][/success] Windows Firewall rule '{rule_name}' created.")
                    applied_any = True
        else:
            self.console.print(
                "[warning][!] Platform not natively supported for kernel-level firewall hooks. "
                "No rules were applied.[/warning]"
            )
            return False

        return applied_any

    def revert_rate_limits(self) -> int:
        """Remove every rule this engine has applied, tracked via StateManager."""
        rules = self.state.clear_rate_limit_rules()
        if not rules:
            self.console.print("[warning][!] No active NetLeak Guard rate-limit rules to revert.[/warning]")
            return 0

        reverted = 0
        for entry in rules:
            if entry["platform"] == "linux":
                del_cmd = ["iptables", "-D"] + entry["rule"].split()[1:]
                if self._run(del_cmd):
                    reverted += 1
            elif entry["platform"] == "win32":
                del_cmd = ["netsh", "advfirewall", "firewall", "delete", "rule",
                           f"name={entry['rule']}"]
                if self._run(del_cmd):
                    reverted += 1

        self.console.print(f"[success][+][/success] Reverted {reverted}/{len(rules)} rate-limit rule(s).")
        return reverted

    def isolate_port_telemetry(self, disable_common_telemetry: bool = True) -> bool:
        if not disable_common_telemetry:
            return False

        self.console.print(
            f"[info][*][/info] Redirecting {len(TELEMETRY_HOSTS)} known telemetry hosts to loopback "
            f"via [accent]{HOSTS_FILE}[/accent]."
        )
        try:
            with open(HOSTS_FILE, "r") as f:
                current = f.read()

            marker = "# --- NetLeak Guard telemetry block ---"
            if marker in current:
                self.console.print("[warning][!] Telemetry block already present in hosts file.[/warning]")
                self.state.set_telemetry_isolated(True)
                return True

            block_lines = "\n".join(f"127.0.0.1 {host}" for host in TELEMETRY_HOSTS)
            addition = f"\n{marker}\n{block_lines}\n# --- end NetLeak Guard block ---\n"

            with open(HOSTS_FILE, "a") as f:
                f.write(addition)

            self.state.set_telemetry_isolated(True)
            self.console.print("[success][+][/success] Telemetry hosts routed to 127.0.0.1.")
            return True
        except PermissionError:
            self.console.print(
                f"[danger][-][/danger] Cannot write to {HOSTS_FILE} - permission denied. "
                "Re-run elevated to isolate telemetry."
            )
            return False
        except OSError as e:
            self.console.print(f"[danger][-][/danger] Failed to update hosts file: {e}")
            return False
