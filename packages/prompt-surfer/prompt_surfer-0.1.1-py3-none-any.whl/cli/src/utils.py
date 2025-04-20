import os
import sys
import subprocess
import uuid
from dotenv import load_dotenv
from openai import AsyncOpenAI
import logging
import tiktoken
from agents import Runner
# Note: setup_prompt_tracing is imported in cli.py and main.py, not here

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Default model
MODEL = "gpt-4o-mini"

async def get_chat_completion(messages, model='gpt-4o-mini', api_key=None):
    # Create a client with the provided API key or get from environment
    client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    logger.info(f"Calling OpenAI API with model: {model}")
    try:
        # Traditional OpenAI API approach
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
        )
        logger.info("OpenAI API call completed successfully")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        raise

async def get_agent_completion(agent, user_input):
    logger.info(f"Running agent: {agent.name}")
    try:
        # Import the necessary modules from the OpenAI Agents SDK
        from agents import trace, run

        # Create a trace name that includes the agent name for better identification
        trace_name = f"{agent.name} Prompt Generation"

        # Get metadata from the agent if available
        agent_metadata = {}
        if hasattr(agent, '_prompt_metadata') and agent._prompt_metadata:
            agent_metadata = agent._prompt_metadata
            logger.debug(f"Agent metadata found: {agent_metadata}")

        # Import our helper function to create properly formatted metadata
        from cli.src.tracing import create_trace_metadata

        # Create trace metadata with all values as strings
        trace_metadata = create_trace_metadata(
            agent_name=agent.name,
            user_input=user_input,
            additional_metadata=agent_metadata
        )
        logger.debug(f"Created trace metadata with keys: {list(trace_metadata.keys())}")

        # Generate a unique trace ID for this run
        trace_id = f"trace_{uuid.uuid4().hex}"
        logger.debug(f"Generated trace ID: {trace_id}")

        # Configure the run with proper tracing settings
        run_config = run.RunConfig(
            workflow_name=trace_name,
            trace_metadata=trace_metadata,
            trace_include_sensitive_data=True,  # Include sensitive data for complete tracing
            tracing_disabled=False,  # Explicitly enable tracing
            trace_id=trace_id  # Use our generated trace ID
        )

        # Use a trace context manager to ensure the prompt is logged
        # The trace context ensures all operations are captured in the trace
        with trace(trace_name, trace_id=trace_id, metadata=trace_metadata) as current_trace:
            # Use the Runner from the Agents SDK to run the agent
            result = await Runner.run(
                agent,
                user_input,
                max_turns=10,
                run_config=run_config
            )

            # Add the result to the trace metadata for completeness
            if current_trace and current_trace.metadata:
                # Add result information to the trace metadata
                current_trace.metadata["result_length"] = str(len(result.final_output) if result.final_output else 0)
                current_trace.metadata["completion_status"] = "success"
                logger.debug("Added result metadata to trace")

        logger.info("Agent run completed successfully")
        return result.final_output
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        # Log the error type for better debugging
        logger.error(f"Error type: {type(e).__name__}")
        # Re-raise the exception to be handled by the caller
        raise

def count_tokens(text, model=None):
    """Count the number of tokens in a text string."""
    try:
        # For simplicity, we use gpt-4 tokenizer for all models
        # This is an approximation but works well enough for our purposes
        # The model parameter is kept for API compatibility but not used
        encoding = tiktoken.encoding_for_model("gpt-4")
        return len(encoding.encode(text))
    except Exception as e:
        logger.error(f"Error counting tokens: {str(e)}")
        return 0

def calculate_prompt_price(input_tokens, output_tokens, model="gpt-4o-mini"):
    """Calculate the price for a prompt based on token count."""
    # Pricing rates for different models
    prices = {
        "gpt-4o-mini": {
            "input": 0.15 / 1_000_000,  # $0.15 per 1M tokens
            "output": 0.60 / 1_000_000,  # $0.60 per 1M tokens
        },
        "gpt-4o": {
            "input": 5.00 / 1_000_000,  # $5.00 per 1M tokens
            "output": 15.00 / 1_000_000,  # $15.00 per 1M tokens
        },
        "gpt-4.5-preview": {
            "input": 75.00 / 1_000_000,  # $75.00 per 1M tokens
            "output": 150.00 / 1_000_000,  # $150.00 per 1M tokens
        },
        "gpt-4.1-2025-04-14": {
            "input": 3.00 / 1_000_000,  # $3.00 per 1M tokens
            "output": 12.00 / 1_000_000,  # $12.00 per 1M tokens
        }
    }

    if model not in prices:
        model = "gpt-4o-mini"  # default to GPT-4o Mini pricing

    input_price = input_tokens * prices[model]["input"]
    output_price = output_tokens * prices[model]["output"]
    total_price = input_price + output_price

    return {
        "input_cost": round(input_price, 6),  # Increased decimal places for smaller numbers
        "output_cost": round(output_price, 6),
        "total_cost": round(total_price, 6),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }

def copy_to_clipboard(console, text, show_success=True):
    """Helper function to copy text to clipboard with error handling."""
    success = False
    try:
        # Try platform-specific methods first
        if sys.platform == 'darwin':  # macOS
            try:
                # Use pbcopy on macOS
                process = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
                copy_process = subprocess.Popen(['pbcopy'], stdin=process.stdout, stderr=subprocess.PIPE)
                process.stdout.close()  # Allow process to receive a SIGPIPE if copy_process exits
                _, stderr = copy_process.communicate()
                success = copy_process.returncode == 0
                if success:
                    logger.debug("Successfully copied using pbcopy")
                else:
                    logger.warning(f"pbcopy failed: {stderr.decode()}")
                    success = False
            except (FileNotFoundError, subprocess.SubprocessError) as e:
                logger.warning(f"Error using pbcopy: {str(e)}")
                success = False

        # If platform-specific method failed or we're on another platform, try pyperclip
        if not success:
            try:
                import pyperclip
                pyperclip.copy(text)
                success = True
                logger.debug("Successfully copied using pyperclip")
            except ImportError:
                console.print("[error]pyperclip module not found. Cannot copy to clipboard.[/error]")
                console.print("[info]Please install it: pip install pyperclip[/info]")
                success = False
            except Exception as e:
                console.print(f"[error]Error using pyperclip: {str(e)}[/error]")
                success = False

        # Show success message if requested
        if success and show_success:
            console.print("[success]Copied to clipboard![/success]")

    except Exception as e:
        # Catch any other unexpected errors
        console.print(f"[error]Unexpected error copying to clipboard: {str(e)}[/error]")
        if sys.platform == 'darwin':
            console.print("[info]If on macOS, try running: chmod +x /usr/bin/pbcopy[/info]")
        console.print("[info]If using X11, try installing xclip or xsel: sudo apt install xclip[/info]")
        console.print("[info]Alternatively, ensure pyperclip is installed: pip install pyperclip[/info]")
        success = False

    return success