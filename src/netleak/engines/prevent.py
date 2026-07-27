"""
Prevent Engine - honeytoken decoys with real access detection, plus
header obfuscation maps for reverse-proxy layers.

Honeytokens are watched with `watchdog` so that opening/reading the
decoy file actually triggers a local alert, instead of just claiming
it will.
"""

import os
import json
import threading
from rich.console import Console

from netleak.state import StateManager

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


if WATCHDOG_AVAILABLE:
    class _HoneytokenHandler(FileSystemEventHandler):
        def __init__(self, console: Console, token_path: str):
            self.console = console
            self.token_path = os.path.abspath(token_path)

        def on_opened(self, event):
            if os.path.abspath(event.src_path) == self.token_path:
                self.console.print(
                    f"\n[danger][ALERT][/danger] Honey-token accessed: [accent]{event.src_path}[/accent] "
                    "- something just read your decoy credentials."
                )

        def on_modified(self, event):
            if os.path.abspath(event.src_path) == self.token_path:
                self.console.print(
                    f"\n[warning][ALERT][/warning] Honey-token touched: [accent]{event.src_path}[/accent]"
                )


class PreventEngine:
    """
    Applies active defense techniques: honeytoken decoys with real
    filesystem watching, and header obfuscation maps for reverse
    proxies to strip identity-revealing headers.
    """

    def __init__(self, console: Console, state: StateManager | None = None):
        self.console = console
        self.state = state or StateManager()
        self._observer = None

    def generate_honeytokens(self, output_dir: str = ".") -> str:
        token_data = {
            "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
            "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "region": "us-east-1",
            "note": "This is a NetLeak Guard decoy. Access is monitored.",
        }

        file_path = os.path.join(output_dir, "aws_credentials_decoy.json")
        try:
            with open(file_path, "w") as f:
                json.dump(token_data, f, indent=4)
            self.console.print(f"[success][+][/success] Honey-token credentials file written to: [accent]{file_path}[/accent]")

            watching = self._start_watch(file_path)
            self.state.add_honeytoken(file_path, watching)

            if watching:
                self.console.print("[success][+][/success] Live filesystem watch active - accessing this file will alert you here.")
            else:
                self.console.print(
                    "[warning][!] `watchdog` not installed - file was created but is NOT being monitored. "
                    "Run `pip install watchdog` to enable live alerts.[/warning]"
                )
            return file_path
        except OSError as e:
            self.console.print(f"[danger][-][/danger] Honey-token assembly failed: {str(e)}")
            return ""

    def _start_watch(self, file_path: str) -> bool:
        if not WATCHDOG_AVAILABLE:
            return False

        if self._observer is None:
            self._observer = Observer()
            self._observer.start()

        handler = _HoneytokenHandler(self.console, file_path)
        watch_dir = os.path.dirname(os.path.abspath(file_path)) or "."
        self._observer.schedule(handler, watch_dir, recursive=False)
        return True

    def stop_watching(self):
        if self._observer is not None:
            self._observer.stop()
            self._observer.join(timeout=2)
            self._observer = None

    def obfuscate_headers(self, service_type: str = "http") -> dict:
        self.console.print(f"[info][*][/info] Formulating response header obfuscation map for service: [accent]{service_type}[/accent]")

        obfuscation_map = {
            "Server": "Apache/2.4.41 (Unix)",
            "X-Powered-By": "Redacted/SecuredByNetleak",
            "X-AspNet-Version": "Removed",
            "X-Frame-Options": "SAMEORIGIN",
            "Server-Timing": "Disabled",
        }

        self.state.set_header_obfuscation_generated(True)
        self.console.print("[success][+][/success] Obfuscation schema generated. Apply these headers inside your reverse-proxy layer (nginx add_header / Apache Header set).")
        return obfuscation_map
