# 🛡️ NetLeak Guard

An interactive, multi-module Command Line Interface (CLI) application architecture engineered to detect, isolate, and mitigate structural data footprints and protocol-level network leakage vectors. 

Co-developed as a collaborative partnership between **raKSum** and **Gemini (AI Systems Architect)**, NetLeak Guard brings professional-grade, Metasploit-like interactive shell controls to automated network tracking protection.

---

## 👥 Authors & Collaborators
* **raKSum** — Lead Developer & Security Architect
* **Gemini** — AI Collaborator & Systems Engineering Support

---

## 🚀 Core Architectural Engines

### 1. 🔍 Monitor Engine (`monitor`)
* **Live Protocol Sniffing:** Scans active network interfaces for cleartext sensitive structures, credentials, or API tokens.
* **Footprint Profiling:** Evaluates out-of-band leakage vulnerabilities including broadcasted SSID history and cleartext browser user-agents.

### 2. ⚡ Limit Engine (`limit`)
* **Host Rate-Limiting:** Implements host-level port throttling constraints to disrupt hostile network scanning and topology enumeration.
* **Telemetry Deflection:** Maps known background analytical endpoints to loopback addresses to stop passive software tracing leaks.

### 3. 🛡️ Prevent Engine (`prevent`)
* **Honey-Token Decoys:** Deploys fake configuration layers (e.g., mock AWS/Database credentials) rigged with callback webhooks to alert you when unauthorized files are read.
* **Fingerprint Obfuscation:** Generates signature manipulation arrays for reverse proxies to obscure operating system flags and server headers (`Server`, `X-Powered-By`).

---

## 🎛️ Persistent Interactive Interface

NetLeak Guard features a custom-built non-exiting console modeled directly after tools like `msfconsole`. It uses `prompt_toolkit` to maintain a stable command processor loop while allowing dynamic navigation inside specific sub-engines.

### Console Commands Reference

| Command | Operational Context | Description |
| :--- | :--- | :--- |
| `help` or `?` | Global / Sub-module | Draws the master structural action matrix. |
| `status` | Global / Sub-module | Dynamically evaluates structural rules, decoy health, and active rule sets. |
| `use <module>`| Global | Shifts the console context string into a selected engine (`monitor`, `limit`, `prevent`). |
| `back` | Sub-module | Pops back up to the root console space (`netleak >`). |
| `monitor start`| Monitor Context | Fires up the interactive packet analysis and metadata parser streams. |
| `limit apply`  | Limit Context   | Provisions system firewall restrictions and isolates telemetry pipelines. |
| `prevent deploy`| Prevent Context | Creates canary honey-tokens and exports application header maps. |
| `exit` / `quit` | Global / Sub-module | Flushes standard logs, tears down test files, and terminates safely. |

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
        ├── __init__.py    # Version initialization metadata
        ├── engines/
        │   ├── __init__.py
        │   ├── limit.py   # Rate-limiting engines & firewall rules
        │   ├── monitor.py # Sniffing operations & protocol trace inspectors
        │   └── prevent.py # Decoy deployment & fingerprint camouflage maps
        └── ui/
            ├── __init__.py
            ├── banners.py # Cypher-themed ASCII splash graphics
            └── styles.py  # Rich UI style color mapping profiles
```
## ⚙️ Installation & Environment Setup

### 📋 Prerequisites
* **Python Configuration:** Python 3.10 or higher.
* **System Privileges:** Root/Administrator access may be required if binding directly to lower-level raw network sockets (`monitor`) or adjusting OS kernel firewall tables (`limit`).

### 📦 Mandatory Library Dependencies
The system relies on two critical runtime visual frameworks:
1. **`prompt_toolkit`** — Manages cursor preservation, live multi-level inputs, and command-history retrieval logs without resetting shell loops.
2. **`rich`** — Renders color-coded terminal telemetry, structured tables, loader icons, and multi-stage progress bars.

### 🔧 Step-by-Step Deployment

1. **Clone the Upstream Repository:**
   ```bash
   git clone [https://github.com/raKSum/netleak-guard.git](https://github.com/raKSum/netleak-guard.git)
   cd netleak-guard
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
### Perform a Clean Package Injection (Development/Editable Mode):
Using editable installation ensures that code modifications update the system execution pathways instantly without requiring re-installation:
    ```bash
    pip install --upgrade pip
    pip install -e .
    ```
## ⚖️ License
Distributed under the MIT License. See LICENSE inside the repository root for more information.