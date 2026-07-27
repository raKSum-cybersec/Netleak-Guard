from rich.theme import Theme
from rich.console import Console

NETLEAK_THEME = Theme({
    "info": "cyan bold",
    "warning": "yellow bold",
    "danger": "red bold",
    "success": "green bold",
    "header": "magenta bold",
    "accent": "bold violet",
})

console = Console(theme=NETLEAK_THEME)