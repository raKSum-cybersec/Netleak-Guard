# 🛡️ NetLeak Guard

An interactive, multi-module Command Line Interface (CLI) application architecture engineered to detect, isolate, and mitigate structural data footprints and protocol-level network leakage vectors. 

Co-developed as a collaborative partnership between **raKSum** and **Gemini (AI Systems Architect)**, NetLeak Guard brings professional-grade, Metasploit-like interactive shell controls to automated network tracking protection.

---

## 👥 Authors & Collaborators
* **raKSum** — Lead Developer & Security Architect
* **Gemini** — AI Collaborator & Systems Engineering Support

---

## 🔑 Privilege Requirements

**Most of NetLeak Guard's real functionality requires root (Linux/macOS) or Administrator (Windows) privileges.** The console will launch and run without elevation, but the following commands need it to actually do anything:

| Command | Needs root/admin? | Why |
| :--- | :--- | :--- |
| `inspect ports` / `inspect live` | Partial | Works unprivileged, but processes you don't own show as `[access denied]` — run elevated to resolve every PID. |
| `monitor start` | **Yes** | Raw packet capture (via `scapy`) requires opening raw sockets, which the OS restricts to elevated processes. |
| `limit apply` / `limit revert` | **Yes** | Modifies live firewall rules (`iptables` / Windows Firewall) and writes to the system hosts file. |
| `prevent deploy` | No | Writes a decoy file and watches it in userspace — no elevation needed. |

If a command needs privileges it doesn't have, NetLeak Guard will tell you explicitly (e.g. *"Raw packet capture requires elevated privileges"*) rather than silently doing nothing or faking results.

**Run elevated:**
```bash
# Linux / macOS
sudo netleak

# Windows (from an Administrator PowerShell/Command Prompt)
netleak
```

⚠️ Because `limit apply` edits real firewall rules and your hosts file, only run it elevated when you actually intend to apply those changes — the console will ask for confirmation first either way.

---

## 🚀 Core Architectural Engines

All engines act on real, live system state — no simulated output.

### 1. 🧭 Inspect Engine (`inspect`)
* **Process ↔ Port ↔ Connection Map:** Uses `psutil` to show exactly which process owns which local/remote socket, live.
* **Snapshot or Streaming:** `inspect ports` for a one-shot view, `inspect live [seconds]` for a continuously refreshing table.

### 2. 🔍 Monitor Engine (`monitor`)
* **Live Protocol Sniffing:** Uses `scapy` to capture real traffic and flag plaintext DNS queries, unencrypted HTTP flows, and outbound UDP telemetry.
* **Requires elevated privileges** (root/administrator) and `scapy` installed for raw socket access — the engine will tell you plainly if it can't capture rather than fabricating results.

### 3. ⚡ Limit Engine (`limit`)
* **Host Rate-Limiting:** Applies real `iptables` rules (Linux) or Windows Firewall rules to throttle hostile scanning — with a confirmation prompt before anything touches your firewall, and `limit revert` to remove exactly what was added.
* **Telemetry Deflection:** Appends known background analytics hosts to your hosts file, routed to loopback.

### 4. 🛡️ Prevent Engine (`prevent`)
* **Honey-Token Decoys:** Deploys mock AWS credential files watched in real time via `watchdog` — opening/reading the decoy triggers an in-console alert.
* **Fingerprint Obfuscation:** Generates a header obfuscation map (`Server`, `X-Powered-By`, etc.) for you to apply in your reverse-proxy config.

`status` reflects only what has actually been applied in the current environment (tracked in `~/.netleak/state.json`), not hardcoded "ACTIVE" flags.

---

## 🎛️ Persistent Interactive Interface

NetLeak Guard features a custom-built non-exiting console modeled directly after tools like `msfconsole`. It uses `prompt_toolkit` to maintain a stable command processor loop while allowing dynamic navigation inside specific sub-engines.

### Console Commands Reference

| Command | Operational Context | Description |
| :--- | :--- | :--- |
| `help` or `?` | Global / Sub-module | Draws the master structural action matrix. |
| `status` | Global / Sub-module | Shows real, live-tracked defense state — not simulated flags. |
| `use <module>`| Global | Shifts the console context string into a selected engine (`monitor`, `limit`, `prevent`, `inspect`). |
| `back` | Sub-module | Pops back up to the root console space (`netleak >`). |
| `inspect ports` | Inspect Context | One-shot snapshot of every process and the ports/connections it owns. |
| `inspect live [seconds]` | Inspect Context | Continuously refreshing process/port/connection view. |
| `monitor start [seconds]`| Monitor Context | Live packet capture and leak-relevant traffic flagging (needs `scapy` + root/admin). |
| `limit apply`  | Limit Context   | Applies real firewall rate-limit rules and isolates telemetry hosts (prompts for confirmation). |
| `limit revert`  | Limit Context   | Removes every rule this session applied. |
| `prevent deploy`| Prevent Context | Creates a watched canary honey-token and exports the header obfuscation map. |
| `exit` / `quit` | Global / Sub-module | Stops file watchers, flushes standard logs, and terminates safely. |

---

## 📂 Project Repository Tree

```text
netleak-guard/
├── .gitignore             # Git indexing exclusions (prevents tracking caches/local honey-tokens)
├── LICENSE                # MIT Open-Source Authorization
├── pyproject.toml         # Hatchling build configuration & package dependency manifest
├── README.md              # Project Onboarding & Operations Manual
└── src/
    └── netleak/
        ├── cli.py         # Persistent command execution loop & cursor state management
        ├── commands.py    # Submodule context routers & console operations
        ├── state.py       # Persistent, honest state tracking (~/.netleak/state.json)
        ├── __init__.py    # Version initialization metadata
        ├── engines/
        │   ├── __init__.py
        │   ├── inspect.py # Real psutil-based process/port/connection mapping
        │   ├── limit.py   # Real iptables/netsh rate-limiting & telemetry isolation
        │   ├── monitor.py # Real scapy-based live packet capture
        │   └── prevent.py # Watched honey-tokens & fingerprint camouflage maps
        └── ui/
            ├── __init__.py
            ├── banners.py       # Random ASCII splash art (static + pyfiglet-generated)
            ├── banner_art/      # Hand-authored .txt banner files, edit freely
            └── styles.py        # Rich UI style color mapping profiles
```
## ⚙️ Installation & Environment Setup

### 📋 Prerequisites
* **Python Configuration:** Python 3.10 or higher.
* **System Privileges:** See [🔑 Privilege Requirements](#-privilege-requirements) above — `monitor start` and `limit apply`/`limit revert` require root/Administrator; `inspect` and `prevent` work unprivileged.

### 📦 Mandatory Library Dependencies
The system relies on these runtime frameworks:
1. **`prompt_toolkit`** — Manages cursor preservation, live multi-level inputs, and command-history retrieval logs without resetting shell loops.
2. **`rich`** — Renders color-coded terminal telemetry, structured tables, loader icons, and multi-stage progress bars.
3. **`psutil`** — Powers the `inspect` engine's real process ↔ port ↔ connection mapping.
4. **`scapy`** — Powers the `monitor` engine's live packet capture (needs root/admin — see [🔑 Privilege Requirements](#-privilege-requirements)).
5. **`watchdog`** — Watches honey-token decoy files for real access events in the `prevent` engine.
6. **`pyfiglet`** — Generates procedural ASCII splash art variety on boot.

All are installed automatically via `pip install -e .` below.

### 🔧 Step-by-Step Deployment

1. **Clone the Upstream Repository:**
   
   ```bash
   git clone [https://github.com/raKSum/netleak-guard.git](https://github.com/raKSum/netleak-guard.git)
   cd netleak-guard
   ```

2. **Isolate Your Python Workspace Environment**
    
    ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Perform a Clean Package Injection (Development/Editable Mode):**
Using editable installation ensures that code modifications update the system execution pathways instantly without requiring re-installation:
    
    ```bash
    pip install --upgrade pip
    pip install -e .
    ```
4. **Launch the Engine Workspace:**
    ```bash
    netleak
    ```

## ⚖️ License
Distributed under the MIT License. See LICENSE inside the repository root for more information.