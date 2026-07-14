import time
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from netleak.engines.monitor import MonitorEngine
from netleak.engines.limit import LimitEngine
from netleak.engines.prevent import PreventEngine

class CommandProcessor:
    def __init__(self, console):
        self.console = console
        self.context = ""  # Updates context status globally
        
        # Instantiate core system engines
        self.monitor_engine = MonitorEngine(self.console)
        self.limit_engine = LimitEngine(self.console)
        self.prevent_engine = PreventEngine(self.console)

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
            case "exit" | "quit":
                self.console.print("[danger][*] Disengaging all operational layers. Safe shutdown verified. See you next run, raKSum & Gemini![/danger]")
                return False
            case _:
                self.console.print(f"[danger]──> Error: '{cmd}' command structural breakdown. Type 'help'.[/danger]")
        return True

    def _switch_context(self, args):
        if not args:
            self.console.print("[warning][!] Usage: use [monitor | limit | prevent][/warning]")
            return
        target = args[0].lower()
        if target in ["monitor", "limit", "prevent"]:
            self.context = target
            self.console.print(f"[info][*][/info] Context shifted to module: [accent]{target}[/accent]")
        else:
            self.console.print(f"[danger][-] Module '{target}' does not exist inside our control ecosystem.[/danger]")

    def _show_help(self):
        table = Table(title="Control Command Matrix", header_style="bold magenta")
        table.add_column("Command / Module", style="cyan", no_wrap=True)
        table.add_column("Description / Intent Action", style="white")
        
        table.add_row("use <module>", "Navigate console context into specific submodules ('monitor', 'limit', 'prevent')")
        table.add_row("back", "Navigate back up to root context")
        table.add_row("status", "Inspect the global metrics and system defense states")
        table.add_row("monitor start", "Initialize real-time packet analyzer & leak scan loops")
        table.add_row("limit apply", "Apply rate limiting constraints to common background telemetry routes")
        table.add_row("prevent deploy", "Deploy a diagnostic Honey-Token credential decoy & generate HTTP obfuscation maps")
        table.add_row("exit / quit", "Terminate local console sessions safely")
        self.console.print(table)

    def _handle_monitor(self, args):
        action = args[0].lower() if args else "start"
        if action == "start":
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40),
                transient=True,
                console=self.console
            ) as progress:
                task = progress.add_task("[cyan]Listening for leakage vectors on live interfaces...", total=100)
                while not progress.finished:
                    time.sleep(0.015)
                    progress.update(task, advance=2.5)
            
            leaks = self.monitor_engine.scan_for_leaks()
            
            table = Table(title="Identified Network Leakage Vectors", header_style="bold red")
            table.add_column("Leak Profiler", style="red")
            table.add_column("Risk Severity", style="bold yellow")
            table.add_column("Payload Footprint Detail", style="white")
            
            for leak in leaks:
                table.add_row(leak["vector"], leak["severity"], leak["payload"])
                
            self.console.print(table)
            self.monitor_engine.run_live_monitor()
        else:
            self.console.print("[warning][!] Try 'monitor start' to inspect packets.[/warning]")

    def _handle_limit(self, args):
        action = args[0].lower() if args else "apply"
        if action == "apply":
            self.limit_engine.configure_rate_limit(ports=[80, 443, 8080], limit_req_per_min=45)
            self.limit_engine.isolate_port_telemetry()
        else:
            self.console.print("[warning][!] Try 'limit apply' to register firewall constraints.[/warning]")

    def _handle_prevent(self, args):
        action = args[0].lower() if args else "deploy"
        if action == "deploy":
            self.prevent_engine.generate_honeytokens()
            self.prevent_engine.obfuscate_headers()
        else:
            self.console.print("[warning][!] Try 'prevent deploy' to generate decoys and security schemas.[/warning]")

    def _show_status(self):
        table = Table(box=None, title="Current Defense Integrity Matrix", title_justify="left")
        table.add_column("Operational Vector Profile", style="bold cyan")
        table.add_column("Active Safeguard Status", style="green")
        table.add_row("Interface Isolation Rules", "[success]ACTIVE[/success]")
        table.add_row("Decoy Honey-Tokens", "[success]DEPLOYED[/success]")
        table.add_row("Obfuscated Headers Ruleset", "[success]CONSTRUCTED[/success]")
        table.add_row("Telemetry Blocking Mode", "[warning]RECALIBRATING[/warning]")
        self.console.print(table)