import os
import sys
import re
from dotenv import load_dotenv
import asyncio
from rich.console import Console
from rich.theme import Theme
from openai import AsyncOpenAI
from datetime import datetime
import questionary
from questionary import Style as QuestionaryStyle, Choice
import json
from cli.src.utils import count_tokens, calculate_prompt_price, get_agent_completion, copy_to_clipboard
from cli.src.agents_config import create_midjourney_agent, create_udio_agent, create_suno_agent
from cli.src.history import PromptHistory

# Load environment variables from .env file
load_dotenv()

class PromptComposer:
    def __init__(self, api_key=None):
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("No OpenAI API key provided. Please set OPENAI_API_KEY environment variable or provide it as a parameter.")

        self.client = AsyncOpenAI(api_key=self.api_key)
        self.models = {
            'gpt-4o-mini': {
                'name': 'GPT-4o mini',
                'description': 'Faster and more cost-effective'
            },
            'gpt-4o-2024-11-20': {
                'name': 'GPT-4o (Nov 2024)',
                'description': 'Powerful and accurate snapshot model'
            },
            'gpt-4.5-preview': {
                'name': 'GPT-4.5 Preview',
                'description': 'Latest preview model with premium capabilities (higher cost)'
            },
            'gpt-4.1-2025-04-14': {
                'name': 'GPT-4.1 (Apr 2025)',
                'description': 'Advanced model with exceptional performance'
            }
        }
        self.current_model = "gpt-4.1-2025-04-14"  # Default model
        self.temperature = 0.8  # Default temperature (higher = more creative)
        self.prompts = {
            'midjourney': self.load_prompt('prompts/midjourney.txt'),
            'udio': self.load_prompt('prompts/udio.txt'),
            'suno': self.load_prompt('prompts/suno.txt')
        }
        # Initialize agents
        self.update_agents()
        # Initialize history handler (not storing history within composer anymore)
        self.history_handler = PromptHistory()
        # Define a retro-cool theme with neon colors
        self.console = Console(theme=Theme({
            "info": "magenta",
            "warning": "yellow",
            "error": "bold red",
            "success": "bold green",
            "header": "bold cyan underline",
            "subheader": "blue",
            "retro_border": "magenta",
            "retro_text": "cyan"
        }))

        # Define custom retro style for questionary
        self.custom_style = QuestionaryStyle([
            ("question", "bold magenta"),
            ("answer", "bold green"),
            ("pointer", "bold cyan"),
            ("highlighted", "bold cyan"),
            ("selected", "bold green"),
            ('separator', 'blue'),
        ])

    def update_agents(self):
        """Update agents with the current model and temperature."""
        self.agents = {
            'midjourney': create_midjourney_agent(model=self.current_model, temperature=self.temperature),
            'udio': create_udio_agent(model=self.current_model, temperature=self.temperature),
            'suno': create_suno_agent(model=self.current_model, temperature=self.temperature)
        }

    @staticmethod
    def load_prompt(file_path: str) -> str:
        full_path = os.path.join(os.path.dirname(__file__), '..', file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: Prompt file not found at {full_path}", file=sys.stderr)
            return ""
        except Exception as e:
            print(f"Error reading prompt file {full_path}: {e}", file=sys.stderr)
            return ""

    async def generate_completion(self, prompt_type: str, question: str) -> str | None:
        try:
            # Calculate input tokens
            system_prompt = self.prompts[prompt_type]
            if not system_prompt:
                self.console.print(f"[error]System prompt for '{prompt_type}' is missing or empty.[/error]")
                return None
            input_tokens = count_tokens(system_prompt + question)

            # Use the Agents SDK instead of direct API calls
            agent = self.agents[prompt_type]
            content = await get_agent_completion(agent, question)

            # Calculate output tokens and price
            output_tokens = count_tokens(content)
            price_info = calculate_prompt_price(input_tokens, output_tokens, self.current_model)

            # Display pricing information in a retro format
            self.console.print("\n╔" + "═" * 60 + "╗", style="retro_border")
            model_info = f"MODEL: {self.models[self.current_model]['name']}"
            token_info = f"TOKENS: {price_info['input_tokens']}in/{price_info['output_tokens']}out"
            cost_info = f"COST: ${price_info['total_cost']:.4f}"
            self.console.print(f"║ [blue]{model_info}[/blue] | [magenta]{token_info}[/magenta] | [green]{cost_info}[/green]" + " " * (60 - len(model_info) - len(token_info) - len(cost_info) - 6) + "║", style="retro_border")
            self.console.print("╚" + "═" * 60 + "╝", style="retro_border")

            return content
        except Exception as e:
            self.console.print(f"[error]API error: {type(e).__name__} - {str(e)}[/error]")
            return None

    def save_output(self, prompt_type: str, question: str, output: str) -> str | None:
        # Create output directory structure if it doesn't exist
        home_dir = os.path.expanduser('~')
        output_dir = os.path.join(home_dir, '.prompt-surfer', 'output', prompt_type)
        os.makedirs(output_dir, exist_ok=True)

        # Create a filename based on timestamp and prompt type
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        # Keep a safe version of the question for context, but don't rely on it for uniqueness
        safe_question_prefix = "".join([c if c.isalnum() else '_' for c in question[:30]]).rstrip('_')
        filename = f"{prompt_type}_{timestamp_str}_{safe_question_prefix}.json"

        file_path = os.path.join(output_dir, filename)

        # Prepare data for JSON storage
        # --- Calculate cost info again or retrieve if stored ---
        # This assumes generate_completion returns cost info or we recalculate it here
        # For simplicity, let's assume we recalculate based on the final output
        try:
            system_prompt = self.prompts[prompt_type]
            input_tokens = count_tokens(system_prompt + question)
            output_tokens = count_tokens(output)
            price_info = calculate_prompt_price(input_tokens, output_tokens, self.current_model)
        except Exception: # Basic fallback if token counting/pricing fails
            price_info = {"error": "Could not calculate cost"}

        data_to_save = {
            "prompt_type": prompt_type,
            "model_used": self.current_model,
            "timestamp_iso": timestamp.isoformat(), # Store timestamp in ISO format
            "question": question,
            "output": output,
            "cost_info": price_info
            # Add other relevant metadata if needed
        }

        # Save data as JSON
        try:
            with open(file_path, "w", encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4) # Use indent for readability
            return file_path
        except Exception as e:
            self.console.print(f"[error]Failed to save output to {file_path}: {str(e)}[/error]")
            return None # Return None on failure

    def run(self):
        # Define constants for menu actions to avoid string comparisons
        ACTION_GEN_MIDJOURNEY = "gen_midjourney"
        ACTION_SELECT_MUSIC = "select_music"
        ACTION_GEN_UDIO = "gen_udio"
        ACTION_GEN_SUNO = "gen_suno"
        ACTION_VIEW_HISTORY = "view_history"
        ACTION_SWITCH_MODEL = "switch_model"
        ACTION_UPDATE_API_KEY = "update_api_key"
        ACTION_QUIT = "quit_app"

        while True:
            # Create a retro-cool ASCII art header
            self.console.print("\n", style="retro_border")
            self.console.print("""
  ██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ████████╗
  ██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝
  ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝   ██║
  ██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██╔═══╝    ██║
  ██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║        ██║
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝
  ██████╗ ██╗     ██╗
  ██╔════╝██║     ██║
  ██║     ██║     ██║
  ██║     ██║     ██║
  ╚██████╗███████╗██║
   ╚═════╝╚══════╝╚═╝
            """, style="retro_text")
            self.console.print("\n═════════════════════════════════════════════════════════", style="retro_border")

            # Use questionary with clearer value mapping
            choices = [
                Choice("Generate Midjourney prompts for image creation", value=ACTION_GEN_MIDJOURNEY),
                Choice("Generate music prompts", value=ACTION_SELECT_MUSIC),
                Choice("View history of previously generated prompts", value=ACTION_VIEW_HISTORY),
                Choice(f"Switch model (Current: {self.models[self.current_model]['name']})", value=ACTION_SWITCH_MODEL),
                Choice("Update OpenAI API key", value=ACTION_UPDATE_API_KEY),
                Choice("Quit the application", value=ACTION_QUIT)
            ]

            selected_action = questionary.select(
                "Select an option:",
                choices=choices,
                style=self.custom_style
            ).ask()

            if selected_action is None: # Handle Ctrl+C
                self.console.print('\n[warning]Exiting application due to user interruption... Goodbye![/warning]')
                break

            # --- Process selected action ---
            if selected_action == ACTION_QUIT:
                self.console.print('[warning]Exiting... Goodbye![/warning]')
                break

            elif selected_action == ACTION_VIEW_HISTORY:
                history_choices = ["midjourney", "udio", "suno"]
                selected_type = questionary.select(
                    "Which history do you want to view interactively?",
                    choices=history_choices,
                    style=self.custom_style
                ).ask()

                # Handle Ctrl+C in history type selection
                if selected_type is None:
                    self.console.print('\n[warning]History selection cancelled.[/warning]')
                    continue # Go back to main menu

                if selected_type:
                    # Reuse existing history handler instance instead of creating a new one
                    self.history_handler.interactive_history(selected_type) # Use self.history_handler
                continue # Go back to main menu

            elif selected_action == ACTION_SWITCH_MODEL:
                # Use questionary.Choice for better value handling
                model_choices = [
                    Choice(f"{value['name']}", value=key)
                    for key, value in self.models.items()
                ]
                # Add a Cancel option
                model_choices.append(Choice("[Cancel]", value=None))

                new_model_key = questionary.select(
                    "Select a model:",
                    choices=model_choices,
                    style=self.custom_style
                ).ask()

                if new_model_key and new_model_key in self.models:
                    self.current_model = new_model_key
                    self.update_agents()
                    self.console.print(f"[success]Switched to model: {self.models[self.current_model]['name']}[/success]")
                elif new_model_key is not None: # User selected something, but it wasn't valid (shouldn't happen with Choice)
                    self.console.print("[error]Invalid model selection.[/error]")
                # If new_model_key is None (Cancel or Ctrl+C), just continue
                continue # Go back to main menu

            elif selected_action == ACTION_UPDATE_API_KEY:
                # Prompt for new API key
                from getpass import getpass
                self.console.print("\n[bold cyan]Enter your new OpenAI API key:[/bold cyan]")
                self.console.print("[dim](Input will be hidden for security)[/dim]")
                new_api_key = getpass("API Key: ")

                if not new_api_key:
                    self.console.print("[warning]No API key entered. Keeping existing key.[/warning]")
                    continue

                # Update the API key
                try:
                    # Test the API key by creating a client
                    test_client = AsyncOpenAI(api_key=new_api_key)
                    # If we get here, the API key format is valid (not checking actual auth yet)
                    self.api_key = new_api_key
                    self.client = test_client

                    # Save to .env file if user wants
                    save_to_env = questionary.confirm(
                        "Save this API key to your .env file for future use?",
                        style=self.custom_style
                    ).ask()

                    if save_to_env:
                        try:
                            # Read existing .env file
                            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
                            env_content = ""
                            if os.path.exists(env_path):
                                with open(env_path, 'r') as f:
                                    env_content = f.read()

                            # Update or add the API key
                            if "OPENAI_API_KEY=" in env_content:
                                # Replace existing key
                                env_content = re.sub(r'OPENAI_API_KEY=.*', f'OPENAI_API_KEY={new_api_key}', env_content)
                            else:
                                # Add new key
                                env_content += f"\nOPENAI_API_KEY={new_api_key}\n"

                            # Write back to .env file
                            with open(env_path, 'w') as f:
                                f.write(env_content)

                            self.console.print("[success]API key saved to .env file.[/success]")
                        except Exception as e:
                            self.console.print(f"[error]Failed to save API key to .env file: {str(e)}[/error]")
                            self.console.print("[info]Your API key is still active for this session.[/info]")

                    self.console.print("[success]API key updated successfully.[/success]")
                except Exception as e:
                    self.console.print(f"[error]Invalid API key format: {str(e)}[/error]")

                continue # Go back to main menu

            elif selected_action == ACTION_SELECT_MUSIC:
                # Submenu for music generation options
                music_choices = [
                    Choice("Generate Udio prompts for music creation", value=ACTION_GEN_UDIO),
                    Choice("Generate Suno AI prompts for instrumental music", value=ACTION_GEN_SUNO),
                    Choice("Back to main menu", value=None)
                ]

                music_action = questionary.select(
                    "Select a music generation option:",
                    choices=music_choices,
                    style=self.custom_style
                ).ask()

                if music_action is None:
                    continue  # Go back to main menu

                # Set selected_action to the chosen music option and continue directly to processing
                selected_action = music_action

                # Immediately process the selected music action
                if selected_action == ACTION_GEN_UDIO:
                    prompt_type = 'udio'
                    prompt_noun = 'music'
                elif selected_action == ACTION_GEN_SUNO:
                    prompt_type = 'suno'
                    prompt_noun = 'instrumental music'
                else:
                    continue  # Invalid selection, go back to main menu

                # Display a retro-styled prompt for user input
                self.console.print("\n╔" + "═" * 60 + "╗", style="retro_border")
                self.console.print(f"║ [bold cyan]ENTER YOUR DESCRIPTION FOR {prompt_noun.upper()} GENERATION:[/bold cyan]" + " " * (60 - 38 - len(prompt_noun)) + "║", style="retro_border")
                self.console.print("╚" + "═" * 60 + "╝", style="retro_border")
                question = questionary.text(
                    f"Describe the {prompt_noun} (or type 'q' to cancel):",
                    style=self.custom_style
                ).ask()

                if question is None:  # Handle Ctrl+C during text input
                    self.console.print('\n[warning]Input cancelled.[/warning]')
                    continue  # Go back to main menu

                # Handle empty input
                if not question:
                    self.console.print('[error]Please provide a description or type \'q\' to cancel.[/error]')
                    continue

                # Check for 'q' specifically
                if question.strip().lower() == 'q':
                    self.console.print('[warning]Generation cancelled.[/warning]')
                    continue  # Go back to main menu

                # --- Generation logic ---
                with self.console.status("[bold green]Generating...[/bold green]"):
                    # Run the async function
                    output = asyncio.run(self.generate_completion(prompt_type, question))

                if output:
                    # Display and save output
                    self.console.print("\n[bold cyan]Generated Output:[/bold cyan]")
                    display_output = re.sub(r'\*\*(.*?)\*\*', r'\1', output)  # Basic cleanup for display
                    display_output = display_output.replace('*', '')
                    self.console.print(display_output.strip())

                    # Save output but don't display the path
                    self.save_output(prompt_type, question, output)

                    # --- Interactive Copy Logic ---
                    variations = re.findall(r'^\s*(\d+)\.\s*(.*?)(?=\n\s*\d+\.|\n*$)', output, re.DOTALL | re.MULTILINE)

                    copy_back_value = '__back__'  # Define constant for back value

                    if variations:
                        # --- Loop for multiple copies ---
                        # Track the current selection index to maintain position
                        current_index = 0
                        while True:
                            self.console.print("\n[bold yellow]Copy a variation? (or go back)[/bold yellow]")
                            variation_choices = [
                                Choice(f"{num}: {text.strip()[:60]}{'...' if len(text.strip()) > 60 else ''}", value=(i, text.strip()))
                                for i, (num, text) in enumerate(variations)
                            ]
                            variation_choices.append(questionary.Separator())
                            variation_choices.append(Choice("Back to Main Menu", value=copy_back_value))

                            # Create a new questionary instance each time with the current index
                            question = questionary.select(
                                "Select variation to copy:",
                                choices=variation_choices,
                                style=self.custom_style,
                                default=variation_choices[current_index].value if current_index < len(variations) else None
                            )
                            selected_variation = question.ask()

                            if selected_variation is None or selected_variation == copy_back_value:
                                break  # Exit copy loop
                            else:
                                # selected_variation is now a tuple of (index, text)
                                index, text = selected_variation
                                copy_to_clipboard(self.console, text, show_success=False)
                                # Update the current index to maintain position
                                current_index = index
                                # Clear the console to reduce clutter
                                self.console.clear()
                                # Re-display the panel with the output
                                self.console.print(display_output.strip())
                    else:
                        # --- Loop for multiple copies (no variations) ---
                        # Define constants for copy actions
                        COPY_PROMPT = 'copy_prompt'
                        COPY_OUTPUT = 'copy_output'

                        while True:
                            self.console.print("\n[bold yellow]Copy output? (or go back)[/bold yellow]")
                            no_variation_choices = [
                                Choice('Copy Original Prompt', value=COPY_PROMPT),
                                Choice('Copy Full Output', value=COPY_OUTPUT),
                                Choice("Back to Main Menu", value=copy_back_value)
                            ]
                            copy_choice = questionary.select(
                                "Select an action:",
                                choices=no_variation_choices,
                                style=self.custom_style
                            ).ask()

                            if copy_choice is None or copy_choice == copy_back_value:
                                break  # Exit copy loop
                            elif copy_choice == COPY_PROMPT:
                                copy_to_clipboard(self.console, question, show_success=False)
                                # Clear the console to reduce clutter
                                self.console.clear()
                                # Re-display the panel with the output
                                self.console.print(display_output.strip())
                            elif copy_choice == COPY_OUTPUT:
                                # Use the cleaned display_output
                                copy_to_clipboard(self.console, display_output.strip(), show_success=False)
                                # Clear the console to reduce clutter
                                self.console.clear()
                                # Re-display the panel with the output
                                self.console.print(display_output.strip())

                # Add a newline for spacing before looping back to main menu
                self.console.print()

            elif selected_action == ACTION_GEN_MIDJOURNEY:
                # Process Midjourney image generation
                prompt_type = 'midjourney'
                prompt_noun = 'image'

                # Display a retro-styled prompt for user input
                self.console.print("\n╔" + "═" * 60 + "╗", style="retro_border")
                self.console.print(f"║ [bold cyan]ENTER YOUR DESCRIPTION FOR {prompt_noun.upper()} GENERATION:[/bold cyan]" + " " * (60 - 38 - len(prompt_noun)) + "║", style="retro_border")
                self.console.print("╚" + "═" * 60 + "╝", style="retro_border")
                question = questionary.text(
                    f"Describe the {prompt_noun} (or type 'q' to cancel):", # Clarify 'q' action
                    style=self.custom_style
                ).ask()

                if question is None: # Handle Ctrl+C during text input
                    self.console.print('\n[warning]Input cancelled.[/warning]')
                    continue # Go back to main menu

                # Handle empty input after clarifying 'q'
                if not question:
                    self.console.print('[error]Please provide a description or type \'q\' to cancel.[/error]')
                    continue

                # Check for 'q' specifically
                if question.strip().lower() == 'q':
                    self.console.print('[warning]Generation cancelled.[/warning]')
                    continue # Go back to main menu

                # --- Generation logic with retro styling ---
                with self.console.status("[bold green]⚡ Generating... ⚡[/bold green]"):
                    # Run the async function
                    output = asyncio.run(self.generate_completion(prompt_type, question))

                if output:
                    # Display and save output with retro styling
                    self.console.print("\n╔" + "═" * 60 + "╗", style="retro_border")
                    self.console.print("║ [bold cyan]GENERATED OUTPUT[/bold cyan]" + " " * 43 + "║", style="retro_border")
                    self.console.print("╠" + "═" * 60 + "╣", style="retro_border")

                    # Clean up the output for display
                    display_output = re.sub(r'\*\*(.*?)\*\*', r'\1', output)
                    display_output = display_output.replace('*', '')

                    # Split the output into lines for proper border display
                    output_lines = display_output.strip().split('\n')
                    for line in output_lines:
                        # Wrap long lines
                        if len(line) > 58:
                            wrapped_lines = [line[i:i+58] for i in range(0, len(line), 58)]
                            for wrapped in wrapped_lines:
                                padding = 58 - len(wrapped)
                                self.console.print(f"║ {wrapped}" + " " * padding + " ║", style="retro_border")
                        else:
                            padding = 58 - len(line)
                            self.console.print(f"║ {line}" + " " * padding + " ║", style="retro_border")

                    self.console.print("╚" + "═" * 60 + "╝", style="retro_border")

                    # Save output but don't display the path
                    self.save_output(prompt_type, question, output)

                    # --- Interactive Copy Logic ---
                    variations = re.findall(r'^\s*(\d+)\.\s*(.*?)(?=\n\s*\d+\.|\n*$)', output, re.DOTALL | re.MULTILINE)

                    copy_back_value = '__back__' # Define constant for back value

                    if variations:
                        # --- Loop for multiple copies ---
                        # Track the current selection index to maintain position
                        current_index = 0
                        while True:
                            self.console.print("\n╔" + "═" * 60 + "╗", style="retro_border")
                            self.console.print("║ [bold yellow]COPY A VARIATION? (OR GO BACK)[/bold yellow]" + " " * 25 + "║", style="retro_border")
                            self.console.print("╚" + "═" * 60 + "╝", style="retro_border")
                            variation_choices = [
                                Choice(f"{num}: {text.strip()[:60]}{'...' if len(text.strip()) > 60 else ''}", value=(i, text.strip()))
                                for i, (num, text) in enumerate(variations)
                            ]
                            variation_choices.append(questionary.Separator())
                            variation_choices.append(Choice("Back to Main Menu", value=copy_back_value))

                            # Create a new questionary instance each time with the current index
                            question = questionary.select(
                                "Select variation to copy:",
                                choices=variation_choices,
                                style=self.custom_style,
                                default=variation_choices[current_index].value if current_index < len(variations) else None
                            )
                            selected_variation = question.ask()

                            if selected_variation is None or selected_variation == copy_back_value:
                                break # Exit copy loop
                            else:
                                # selected_variation is now a tuple of (index, text)
                                index, text = selected_variation
                                copy_to_clipboard(self.console, text, show_success=False)
                                # Update the current index to maintain position
                                current_index = index
                                # Clear the console to reduce clutter
                                self.console.clear()
                                # Re-display the panel with the output
                                self.console.print(display_output.strip())
                        # --- End Loop ---

                    else:
                        # --- Loop for multiple copies (no variations) ---
                        # Define constants for copy actions
                        COPY_PROMPT = 'copy_prompt'
                        COPY_OUTPUT = 'copy_output'

                        while True:
                            self.console.print("\n╔" + "═" * 60 + "╗", style="retro_border")
                            self.console.print("║ [bold yellow]COPY OUTPUT? (OR GO BACK)[/bold yellow]" + " " * 29 + "║", style="retro_border")
                            self.console.print("╚" + "═" * 60 + "╝", style="retro_border")
                            no_variation_choices = [
                                Choice('Copy Original Prompt', value=COPY_PROMPT),
                                Choice('Copy Full Output', value=COPY_OUTPUT),
                                Choice("Back to Main Menu", value=copy_back_value)
                            ]
                            copy_choice = questionary.select(
                                "Select an action:",
                                choices=no_variation_choices,
                                style=self.custom_style
                            ).ask()

                            if copy_choice is None or copy_choice == copy_back_value:
                                break # Exit copy loop
                            elif copy_choice == COPY_PROMPT:
                                copy_to_clipboard(self.console, question, show_success=False)
                                # Clear the console to reduce clutter
                                self.console.clear()
                                # Re-display the panel with the output
                                self.console.print(display_output.strip())
                            elif copy_choice == COPY_OUTPUT:
                                # Use the cleaned display_output
                                copy_to_clipboard(self.console, display_output.strip(), show_success=False)
                                # Clear the console to reduce clutter
                                self.console.clear()
                                # Re-display the panel with the output
                                self.console.print(display_output.strip())
                        # --- End Loop ---
                    # --- END ADDED ---

                # Add a newline for spacing before looping back to main menu
                self.console.print()
            else:
                # Handle cases where selected_action is not matched (should not happen with Choice)
                self.console.print(f"[error]Unknown action: {selected_action}[/error]")
                continue
