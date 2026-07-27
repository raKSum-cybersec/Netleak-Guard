"""
Monitor Engine - real live traffic sniffing.

Uses scapy when available and privileges allow raw socket access. If
either condition fails, this engine says so explicitly rather than
silently returning canned data.
"""

import os
import sys
from rich.console import Console
from rich.table import Table

try:
    from scapy.all import sniff, IP, TCP, UDP, DNS, DNSQR
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


def _has_capture_privileges() -> bool:
    if sys.platform.startswith("linux") or sys.platform == "darwin":
        return os.geteuid() == 0
    # Windows: raw capture generally requires Npcap + admin; we can't
    # cheaply verify admin here, so we let scapy itself fail loudly.
    return True


class MonitorEngine:
    """
    Live packet capture and lightweight protocol inspection focused on
    leakage-relevant signals: plaintext DNS queries, unencrypted HTTP
    headers, and unexpected outbound destinations.
    """

    def __init__(self, console: Console):
        self.console = console
        self.active_sniffing = False
        self.captured = []  # list[dict] populated during run_live_monitor

    def capability_check(self) -> tuple[bool, str]:
        if not SCAPY_AVAILABLE:
            return False, (
                "scapy is not installed. Run `pip install scapy` to enable live capture."
            )
        if not _has_capture_privileges():
            return False, (
                "Raw packet capture requires elevated privileges. "
                "Re-run with sudo/administrator to capture live traffic."
            )
        return True, ""

    def _handle_packet(self, pkt) -> dict | None:
        entry = None
        if pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
            try:
                qname = pkt[DNSQR].qname.decode(errors="ignore")
            except Exception:
                qname = "<unreadable>"
            entry = {"vector": "DNS Query", "severity": "MEDIUM", "payload": f"lookup for {qname}"}
        elif pkt.haslayer(TCP) and pkt.haslayer(IP):
            sport, dport = pkt[TCP].sport, pkt[TCP].dport
            if dport == 80 or sport == 80:
                entry = {
                    "vector": "Cleartext HTTP", "severity": "HIGH",
                    "payload": f"{pkt[IP].src}:{sport} -> {pkt[IP].dst}:{dport} (unencrypted)",
                }
        elif pkt.haslayer(UDP) and pkt.haslayer(IP):
            entry = {
                "vector": "UDP Flow", "severity": "LOW",
                "payload": f"{pkt[IP].src} -> {pkt[IP].dst}:{pkt[UDP].dport}",
            }

        if entry:
            self.captured.append(entry)
        return entry

    def run_live_monitor(self, duration_sec: int = 10, interface: str | None = None):
        ok, reason = self.capability_check()
        if not ok:
            self.console.print(f"[danger][-][/danger] Live capture unavailable: {reason}")
            self.console.print(
                "[warning][!] Falling back to connection-level inspection only "
                "(no packet payloads). Use `inspect` for that view.[/warning]"
            )
            return []

        self.captured = []
        self.console.print(
            f"[info][*][/info] Capturing live traffic for {duration_sec}s "
            f"on interface [accent]{interface or 'default'}[/accent]... (Ctrl+C to stop early)"
        )
        self.active_sniffing = True
        try:
            sniff(
                prn=self._handle_packet,
                timeout=duration_sec,
                iface=interface,
                store=False,
            )
        except KeyboardInterrupt:
            self.console.print("\n[warning][!] Capture halted by operator choice.[/warning]")
        except PermissionError:
            self.console.print(
                "[danger][-][/danger] Permission denied opening raw socket. Re-run elevated."
            )
        finally:
            self.active_sniffing = False

        self.console.print(f"[success][+][/success] Capture complete. {len(self.captured)} relevant frames flagged.")
        return self.captured

    def render_findings(self) -> Table:
        table = Table(title="Identified Network Leakage Vectors", header_style="bold red")
        table.add_column("Leak Profiler", style="red")
        table.add_column("Risk Severity", style="bold yellow")
        table.add_column("Payload Footprint Detail", style="white")
        if not self.captured:
            table.add_row("-", "-", "No leakage-relevant traffic observed in this window.")
        for leak in self.captured:
            table.add_row(leak["vector"], leak["severity"], leak["payload"])
        return table
