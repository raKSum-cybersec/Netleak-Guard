import time
from rich.table import Table
from rich.prompt import Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from netleak.state import StateManager
from netleak.engines.monitor import MonitorEngine
from netleak.engines.limit import LimitEngine
from netleak.engines.prevent import PreventEngine
from netleak.engines.inspect import InspectEngine


class CommandProcessor:
    def __init__(self, console):
        self.console = console
        self.context = ""
        self.state = StateManager()

        self.monitor_engine = MonitorEngine(self.console)
        self.limit_engine = LimitEngine(self.console, self.state)
        self.prevent_engine = PreventEngine(self.console, self.state)
        self.inspect_engine = InspectEngine(self.console)

    def execute(self, user_input: str) -> bool:
        parts = user_input.split()
        if not parts:
            return True

        cmd = parts[0].lower()
        args = parts[1:]

        match cmd:
            case "help" | "?":
                self._show_help()
            case "status":
                self._show_status()
            case "use":
                self._switch_context(args)
            case "back":
                self.context = ""
                self.console.print("[info][*][/info] Context reset to global base root.")
            case "monitor":
                self._handle_monitor(args)
            case "limit":
                self._handle_limit(args)
            case "prevent":
                self._handle_prevent(args)
            case "inspect":
                self._handle_inspect(args)
            case "exit" | "quit":
                self.prevent_engine.stop_watching()
                self.console.print("[danger][*] Disengaging all operational layers. Safe shutdown verified. See you next run.[/danger]")
                return False
            case _:
                self.console.print(f"[danger]--> Error: '{cmd}' command structural breakdown. Type 'help'.[/danger]")
        return True

    def _switch_context(self, args):
        if not args:
            self.console.print("[warning][!] Usage: use [monitor | limit | prevent | inspect][/warning]")
            return
        target = args[0].lower()
        if target in ["monitor", "limit", "prevent", "inspect"]:
            self.context = target
            self.console.print(f"[info][*][/info] Context shifted to module: [accent]{target}[/accent]")
        else:
            self.console.print(f"[danger][-] Module '{target}' does not exist inside our control ecosystem.[/danger]")

    def _show_help(self):
        table = Table(title="Control Command Matrix", header_style="bold magenta")
        table.add_column("Command / Module", style="cyan", no_wrap=True)
        table.add_column("Description / Intent Action", style="white")

        table.add_row("use <module>", "Navigate console context into submodules ('monitor', 'limit', 'prevent', 'inspect')")
        table.add_row("back", "Navigate back up to root context")
        table.add_row("status", "Inspect the real, live-tracked defense state (not simulated)")
        table.add_row("inspect ports", "One-shot snapshot: every process, its PID, and the ports/connections it owns")
        table.add_row("inspect live [seconds]", "Continuously refreshing process/port/connection view")
        table.add_row("monitor start [seconds]", "Live packet capture (requires scapy + elevated privileges)")
        table.add_row("limit apply", "Apply real rate-limiting firewall rules + redirect known telemetry hosts")
        table.add_row("limit revert", "Remove every firewall rule this session has applied")
        table.add_row("prevent deploy", "Deploy a watched honey-token decoy + generate header obfuscation map")
        table.add_row("exit / quit", "Terminate local console session safely")
        self.console.print(table)

    def _handle_inspect(self, args):
        action = args[0].lower() if args else "ports"
        if action == "ports":
            self.inspect_engine.show_snapshot()
        elif action == "live":
            duration = int(args[1]) if len(args) > 1 and args[1].isdigit() else 15
            self.inspect_engine.run_live_view(duration_sec=duration)
        else:
            self.console.print("[warning][!] Try 'inspect ports' or 'inspect live [seconds]'.[/warning]")

    def _handle_monitor(self, args):
        action = args[0].lower() if args else "start"
        if action == "start":
            duration = int(args[1]) if len(args) > 1 and args[1].isdigit() else 10

            ok, reason = self.monitor_engine.capability_check()
            if not ok:
                self.console.print(f"[danger][-][/danger] {reason}")
                return

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40),
                transient=True,
                console=self.console,
            ) as progress:
                progress.add_task("[cyan]Preparing capture session...", total=None)
                time.sleep(0.4)

            self.monitor_engine.run_live_monitor(duration_sec=duration)
            self.state.record_monitor_scan()
            self.console.print(self.monitor_engine.render_findings())
        else:
            self.console.print("[warning][!] Try 'monitor start [seconds]' to capture live traffic.[/warning]")

    def _handle_limit(self, args):
        action = args[0].lower() if args else "apply"
        if action == "apply":
            proceed = Confirm.ask(
                "[warning]This will modify live firewall rules and your hosts file. Continue?[/warning]",
                default=False,
            )
            if not proceed:
                self.console.print("[info][*][/info] Aborted. No changes made.")
                return
            self.limit_engine.configure_rate_limit(ports=[80, 443, 8080], limit_req_per_min=45)
            self.limit_engine.isolate_port_telemetry()
        elif action == "revert":
            self.limit_engine.revert_rate_limits()
        else:
            self.console.print("[warning][!] Try 'limit apply' or 'limit revert'.[/warning]")

    def _handle_prevent(self, args):
        action = args[0].lower() if args else "deploy"
        if action == "deploy":
            self.prevent_engine.generate_honeytokens()
            self.prevent_engine.obfuscate_headers()
        else:
            self.console.print("[warning][!] Try 'prevent deploy' to generate decoys and security schemas.[/warning]")

    def _show_status(self):
        snap = self.state.snapshot

        table = Table(box=None, title="Current Defense Integrity Matrix (live state)", title_justify="left")
        table.add_column("Operational Vector Profile", style="bold cyan")
        table.add_column("Active Safeguard Status", style="green")

        rules = snap["rate_limit_rules"]
        table.add_row(
            "Rate-Limit Firewall Rules",
            f"[success]ACTIVE ({len(rules)} rule(s))[/success]" if rules else "[danger]INACTIVE[/danger]",
        )
        table.add_row(
            "Telemetry Host Isolation",
            "[success]ACTIVE[/success]" if snap["telemetry_isolated"] else "[danger]INACTIVE[/danger]",
        )
        tokens = snap["honeytokens"]
        watched = sum(1 for t in tokens if t["watching"])
        table.add_row(
            "Decoy Honey-Tokens",
            f"[success]{watched}/{len(tokens)} WATCHED[/success]" if tokens else "[danger]NONE DEPLOYED[/danger]",
        )
        table.add_row(
            "Obfuscated Headers Ruleset",
            "[success]CONSTRUCTED[/success]" if snap["header_obfuscation_generated"] else "[danger]NOT GENERATED[/danger]",
        )
        table.add_row(
            "Last Monitor Scan",
            snap["last_monitor_scan"] or "[danger]NEVER RUN[/danger]",
        )
        self.console.print(table)
