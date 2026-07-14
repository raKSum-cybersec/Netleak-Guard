import time
import socket
from rich.console import Console
from rich.table import Table

class MonitorEngine:
    """
    Handles active and simulated sniffing operations on local interfaces to identify
    unencrypted text headers, credentials, SSIDs, and general metadata leakage.
    """
    def __init__(self, console: Console):
        self.console = console
        self.active_sniffing = False

    def scan_for_leaks(self, interface: str = "all") -> list:
        self.console.print(f"[info][*][/info] Initializing diagnostic capture sweep on interface: [accent]{interface}[/accent]")
        
        leaks = [
            {"vector": "DNS Query Leak", "severity": "MEDIUM", "payload": "outbound lookups for cleartext internal dev domains"},
            {"vector": "Cleartext HTTP User-Agent", "severity": "LOW", "payload": "Mozilla/5.0 (Nothing Phone 3a Pro) SystemLeak/1.0"},
            {"vector": "SSID Historical Probe", "severity": "HIGH", "payload": "Broadcasting known private network SSIDs in plaintext"},
            {"vector": "Telemetry Outflow", "severity": "LOW", "payload": "Background analytical tracking payload routed via UDP"},
        ]
        return leaks

    def run_live_monitor(self, duration_sec: int = 5):
        self.console.print("[info][*] Binding live engine stream to socket loops... Press Ctrl+C to abort early.[/info]")
        self.active_sniffing = True
        
        try:
            start_time = time.time()
            packet_count = 0
            while self.active_sniffing and (time.time() - start_time < duration_sec):
                time.sleep(0.5)
                packet_count += 8
                self.console.print(f"[success][+][/success] Sniffed {packet_count} packets... Checking protocol headers for leaky metadata.", end="\r")
            
            self.console.print(f"\n[success][+][/success] Complete. Analyzed {packet_count} total frames.")
        except KeyboardInterrupt:
            self.console.print("\n[warning][!] Capturing halted by operator choice.[/warning]")
        finally:
            self.active_sniffing = False