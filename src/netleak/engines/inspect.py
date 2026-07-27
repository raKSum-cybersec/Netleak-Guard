"""
Inspect Engine — real process <-> port <-> connection mapping.

Answers the original design question directly: "which service is opening
which port, and who is it talking to." No simulated data — everything
here comes from psutil reading live OS state.
"""

import time
import psutil
from rich.console import Console
from rich.table import Table
from rich.live import Live


class InspectEngine:
    def __init__(self, console: Console):
        self.console = console

    def snapshot(self) -> list[dict]:
        """One-shot read of all inet connections mapped to owning processes."""
        rows = []
        for conn in psutil.net_connections(kind="inet"):
            proc_name, proc_user = "-", "-"
            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    proc_name = proc.name()
                    proc_user = proc.username()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    proc_name = "[access denied]"

            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "-"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "-"

            rows.append({
                "pid": conn.pid or "-",
                "process": proc_name,
                "user": proc_user,
                "local": laddr,
                "remote": raddr,
                "status": conn.status,
            })
        # Surface active outbound connections first — that's what's "leaking"
        rows.sort(key=lambda r: (r["remote"] == "-", r["process"]))
        return rows

    def render_table(self, rows: list[dict]) -> Table:
        table = Table(title="Live Process ↔ Port ↔ Connection Map", header_style="bold magenta")
        table.add_column("PID", style="cyan", justify="right")
        table.add_column("Process", style="white")
        table.add_column("User", style="grey70")
        table.add_column("Local Address", style="green")
        table.add_column("Remote Address", style="yellow")
        table.add_column("State", style="bold blue")
        for r in rows:
            table.add_row(str(r["pid"]), r["process"], r["user"], r["local"], r["remote"], r["status"])
        return table

    def show_snapshot(self):
        needs_root_hint = False
        rows = self.snapshot()
        if any(r["process"] == "[access denied]" for r in rows):
            needs_root_hint = True

        self.console.print(self.render_table(rows))
        if needs_root_hint:
            self.console.print(
                "[warning][!] Some processes are hidden (access denied). "
                "Run with elevated privileges to resolve every PID.[/warning]"
            )

    def run_live_view(self, duration_sec: int = 15, refresh_hz: float = 1.0):
        """Continuously refreshing table, like a lightweight `netstat -c` / btop panel."""
        self.console.print(
            f"[info][*][/info] Streaming live connection map for {duration_sec}s "
            "(Ctrl+C to stop early)..."
        )
        try:
            with Live(console=self.console, refresh_per_second=refresh_hz, transient=False) as live:
                start = time.time()
                while time.time() - start < duration_sec:
                    rows = self.snapshot()
                    live.update(self.render_table(rows))
                    time.sleep(1.0 / refresh_hz)
        except KeyboardInterrupt:
            self.console.print("\n[warning][!] Live view stopped by operator.[/warning]")

    def listening_ports(self) -> list[dict]:
        """Just the services actively listening — 'what's open on this box right now'."""
        return [r for r in self.snapshot() if r["status"] == "LISTEN"]
