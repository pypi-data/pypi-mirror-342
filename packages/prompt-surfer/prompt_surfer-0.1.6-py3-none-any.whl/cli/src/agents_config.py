import os
import logging
from cli.src.utils import count_tokens
from dotenv import load_dotenv
from agents import Agent, ModelSettings

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# API key will be passed as a parameter

def load_prompt(file_path):
    """Load a prompt from a file."""
    pkg_dir = os.path.dirname(__file__)
    full_path = os.path.join(pkg_dir, '..', file_path)
    with open(full_path, 'r') as file:
        return file.read()

# Create agents for different prompt types
def create_midjourney_agent(model, temperature=0.8):
    """Create an agent for Midjourney prompt generation."""
    system_prompt = load_prompt('prompts/midjourney.txt')

    # Count tokens in the system prompt for tracing purposes
    prompt_tokens = count_tokens(system_prompt)
    logger.debug(f"Midjourney system prompt: {prompt_tokens} tokens")

    # Note: Midjourney v7's Draft mode is selected in the UI and not relevant to include in the prompt itself.
    # Store metadata in a variable for tracing later
    prompt_metadata = {
        "prompt_type": "midjourney",
        "system_prompt_tokens": str(prompt_tokens),  # Convert to string for tracing
        "temperature": str(temperature)  # Convert to string for tracing
    }

    agent = Agent(
        name="Midjourney Prompt Generator",
        instructions=system_prompt,
        model=model,
        model_settings=ModelSettings(
            temperature=temperature
        ),
        mcp_config={"convert_schemas_to_strict": True}
    )

    # We'll use this metadata in the trace context when running the agent
    agent._prompt_metadata = prompt_metadata
    return agent

def create_udio_agent(model, temperature=0.8):
    """Create an agent for Udio prompt generation."""
    system_prompt = load_prompt('prompts/udio.txt')

    # Count tokens in the system prompt for tracing purposes
    prompt_tokens = count_tokens(system_prompt)
    logger.debug(f"Udio system prompt: {prompt_tokens} tokens")

    # Store metadata in a variable for tracing later
    prompt_metadata = {
        "prompt_type": "udio",
        "system_prompt_tokens": str(prompt_tokens),  # Convert to string for tracing
        "temperature": str(temperature)  # Convert to string for tracing
    }

    agent = Agent(
        name="Udio Prompt Generator",
        instructions=system_prompt,
        model=model,
        model_settings=ModelSettings(
            temperature=temperature
        ),
        mcp_config={"convert_schemas_to_strict": True}
    )

    # We'll use this metadata in the trace context when running the agent
    agent._prompt_metadata = prompt_metadata
    return agent

def create_suno_agent(model, temperature=0.8):
    """Create an agent for Suno AI prompt generation."""
    system_prompt = load_prompt('prompts/suno.txt')

    # Count tokens in the system prompt for tracing purposes
    prompt_tokens = count_tokens(system_prompt)
    logger.debug(f"Suno system prompt: {prompt_tokens} tokens")

    # Store metadata in a variable for tracing later
    prompt_metadata = {
        "prompt_type": "suno",
        "system_prompt_tokens": str(prompt_tokens),  # Convert to string for tracing
        "temperature": str(temperature)  # Convert to string for tracing
    }

    agent = Agent(
        name="Suno AI Prompt Generator",
        instructions=system_prompt,
        model=model,
        model_settings=ModelSettings(
            temperature=temperature
        ),
        mcp_config={"convert_schemas_to_strict": True}
    )

    # We'll use this metadata in the trace context when running the agent
    agent._prompt_metadata = prompt_metadata
    return agent
