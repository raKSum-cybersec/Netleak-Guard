import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from netleak.ui.banners import show_random_banner
from netleak.ui.styles import console
from netleak.commands import CommandProcessor

def main():
    show_random_banner(console)
    
    console.print("[success][+][/success] Control subsystem online. Interactive session established safely.")
    console.print("[info][*][/info] Systems Engineering: [accent]raKSum & Gemini[/accent] live partnership mode.")
    console.print("[info][*][/info] Type [accent]help[/accent] or [accent]?[/accent] to review control matrices.\n")
    
    session = PromptSession(history=InMemoryHistory())
    processor = CommandProcessor(console)
    
    while True:
        try:
            prompt_str = f"netleak({processor.context}) > " if processor.context else "netleak > "
            user_input = session.prompt(prompt_str).strip()
            
            if not user_input:
                continue
                
            should_continue = processor.execute(user_input)
            if not should_continue:
                break
                
        except (KeyboardInterrupt, EOFError):
            console.print("\n[warning][!] Interactive loop interrupted by OS signal. Safely flushing state logs.[/warning]")
            break

if __name__ == "__main__":
    main()