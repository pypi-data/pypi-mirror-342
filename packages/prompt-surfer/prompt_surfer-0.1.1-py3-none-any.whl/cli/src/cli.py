import os
import logging
from dotenv import load_dotenv
from rich.console import Console
from rich.theme import Theme
from cli.src.prompt_composer import PromptComposer
from cli.src.tracing import setup_prompt_tracing
from cli.src.tracing_config import configure_tracing

# Configure logging - reduce verbosity for most modules
logging.basicConfig(
    level=logging.WARNING,  # Set default level to WARNING to reduce noise
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Set specific loggers to appropriate levels
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai.agents").setLevel(logging.WARNING)
logging.getLogger("cli.src.tracing").setLevel(logging.WARNING)
logging.getLogger("cli.src.tracing_config").setLevel(logging.WARNING)
logging.getLogger("cli.src.utils").setLevel(logging.WARNING)

# Only show errors for these modules
logging.getLogger("agents.tracing").setLevel(logging.ERROR)

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment if available
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# API key will be handled in the TUI if not found

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
})

console = Console(theme=custom_theme)

HEADER = "AI Prompt Generator"

def main():
    try:
        # Ensure the OpenAI API key is set in the environment for tracing
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            console.print("[warning]No OpenAI API key found in environment. Tracing may not work properly.[/warning]")
        else:
            # Configure tracing with the API key silently
            configure_tracing()

        # Initialize prompt tracing silently
        setup_prompt_tracing()

        composer = PromptComposer()
        # Don't print header here - it will be part of the retro UI
        composer.run()
    except KeyboardInterrupt:
        console.print("\n[info]Exiting.[/info]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {str(e)}[/bold red]")

if __name__ == "__main__":
    main()