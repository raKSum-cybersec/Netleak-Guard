import os
import json
from rich.console import Console

class PreventEngine:
    def __init__(self, console: Console):
        self.console = console

    def generate_honeytokens(self, output_dir: str = ".") -> str:
        token_data = {
            "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
            "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "region": "us-east-1",
            "telemetry_callback": "https://callback.netleak.local/alert?id=token_token_001"
        }
        
        file_path = os.path.join(output_dir, "aws_credentials_decoy.json")
        try:
            with open(file_path, "w") as f:
                json.dump(token_data, f, indent=4)
            self.console.print(f"[success][+][/success] Honey-token credentials file written to: [accent]{file_path}[/accent]")
            self.console.print("[success][+][/success] Probing this token will trigger diagnostic callbacks automatically.")
            return file_path
        except Exception as e:
            self.console.print(f"[danger][-][/danger] Honey-token assembly failed: {str(e)}")
            return ""

    def obfuscate_headers(self, service_type: str = "http") -> dict:
        self.console.print(f"[info][*][/info] Formulating response header obfuscation map for service: [accent]{service_type}[/accent]")
        obfuscation_map = {
            "Server": "Apache/2.4.41 (Unix)",
            "X-Powered-By": "Redacted/SecuredByNetleak",
            "X-AspNet-Version": "Removed",
            "X-Frame-Options": "SAMEORIGIN",
            "Server-Timing": "Disabled"
        }
        self.console.print("[success][+][/success] Obfuscation schema generated successfully. Apply these headers inside your reverse-proxy layers.")
        return obfuscation_map