import random

BANNERS = [
    # Option 1: Cyberpunk Neon Tech
    """
    [bold cyan]    _   _  _____ _____  _      _____  ___   _   _ [/bold cyan]
    [bold cyan]   | \\ | || ___|_   _|| |    |  ___|/ _ \\ | | | |[/bold cyan]
    [bold blue]   |  \\| || |__   | |  | |    | |__ / /_\\ \\| | | |[/bold blue]
    [bold blue]   | . ` ||  __|  | |  | |    |  __||  _  || | | |[/bold blue]
    [bold magenta]   | |\\  || |___  | |  | |____| |___| | | || |_| |[/bold magenta]
    [bold magenta]   \\_| \\_/\\____/  \\_/  \\_____/\\____/\\_| |_/ \\___/ [/bold magenta]
          [bold white] ─── Security Footprint & Network Leak Guard ─── [/bold white]
            [bold dark_goldenrod]      By: raKSum & Gemini (Partnership Mode) [/bold dark_goldenrod]
    """,

    # Option 2: Retro Radar/Terminal
    """
    [bold green]  ______________________________________________________ [/bold green]
    [bold green] / [bold white]▲  NETLEAK GUARD V0.1.0[/bold white]                            \\ [/bold green]
    [bold green]|  ──────────────────────────────────────────────────  |[/bold green]
    [bold green]|  [bold white]Monitoring Mode : ACTIVE[/bold white]                            |[/bold green]
    [bold green]|  [bold white]Defensive Shields: STANDBY[/bold white]                          |[/bold green]
    [bold green]|  [bold white]Created by      : raKSum & Gemini[/bold white]                  |[/bold green]
    [bold green] \\______________________________________________________/ [/bold green]
    """,

    # Option 3: Heavy Industrial Block
    """
    [bold red]  ███╗   ██╗███████╗████████╗██╗     ███████╗ █████╗ ██╗  ██╗[/bold red]
    [bold red]  ████╗  ██║██╔════╝╚══██╔══╝██║     ██╔════╝██╔══██╗██║ ██╔╝[/bold red]
    [bold yellow]  ██╔██╗ ██║█████╗     ██║   ██║     █████╗  ███████║█████╔╝ [/bold yellow]
    [bold yellow]  ██║╚██╗██║██╔══╝     ██║   ██║     ██╔══╝  ██╔══██║██╔═██╗ [/bold yellow]
    [bold magenta]  ██║ ╚████║███████╗   ██║   ███████╗███████╗██║  ██║██║  ██╗[/bold magenta]
    [bold magenta]  ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝[/bold magenta]
          [bold white]  🚨 NETWORK TELEMETRY SHIELDING & DECOY CONTROL 🚨  [/bold white]
    """,

    # Option 4: Minimalist & Clean
    """
    [bold violet]   ┌────────────────────────────────────────────────────────┐[/bold violet]
    [bold violet]   │ [/bold violet][bold white]netleak-guard[/bold white] [bold grey]v0.1.0[/bold grey]                                   [bold violet]│[/bold violet]
    [bold violet]   │ [/bold violet][bold cyan]An active CLI tracking defense framework. [/bold cyan]              [bold violet]│[/bold violet]
    [bold violet]   │ [/bold violet][bold blue]Engineered via collaboration: raKSum & Gemini[/bold blue]           [bold violet]│[/bold violet]
    [bold violet]   └────────────────────────────────────────────────────────┘[/bold violet]
    """
]

def show_random_banner(console):
    console.print(random.choice(BANNERS))