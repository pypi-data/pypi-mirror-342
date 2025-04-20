"""
Tracing utilities for OpenAI Agents SDK.
This module provides functionality to log prompts and other information to OpenAI Agents SDK tracing.
"""

import os
import logging
import uuid
from typing import Optional, Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Import the tracing configuration
from cli.src.tracing_config import configure_tracing

# Load environment variables from user's home directory
home_env_path = os.path.join(os.path.expanduser('~'), '.prompt-surfer', '.env')
if os.path.exists(home_env_path):
    load_dotenv(home_env_path)

# Ensure the OpenAI API key is available for tracing
def ensure_openai_api_key():
    """Ensure that the OpenAI API key is available for tracing."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY environment variable not set. Tracing may not work.")
        return False

    # Configure tracing with the API key
    return configure_tracing()

def setup_prompt_tracing():
    """
    Set up prompt tracing for the OpenAI Agents SDK.
    This should be called during application initialization.
    """
    try:
        # First, ensure the OpenAI API key is available and tracing is configured
        if not ensure_openai_api_key():
            logger.warning("OpenAI API key not available. Tracing may not work properly.")
            return False

        # Import the necessary modules
        try:
            from agents.tracing import TracingProcessor, Trace, Span, add_trace_processor
            from agents.tracing.processors import BackendSpanExporter, BatchTraceProcessor
            from agents.tracing import set_trace_processors
        except ImportError as e:
            logger.error(f"Failed to import tracing modules: {str(e)}")
            logger.error("Make sure you have openai-agents>=0.0.11 installed")
            return False

        # Create a custom processor for adding metadata to traces
        class PromptMetadataProcessor(TracingProcessor):
            """A custom trace processor that adds metadata to traces."""

            def on_trace_start(self, trace: Trace) -> None:
                """Add metadata when a trace starts."""
                if trace.metadata is None:
                    trace.metadata = {}

                # Add application-specific metadata - ensure all values are strings
                trace.metadata["app"] = "prompt-surfer"
                trace.metadata["version"] = "1.0.0"
                trace.metadata["trace_source"] = "prompt_cli_app"
                trace.metadata["timestamp"] = str(uuid.uuid4())  # Add a unique timestamp

                logger.debug(f"Added metadata to trace: {trace.trace_id}")

            def on_trace_end(self, trace: Trace) -> None:
                """Ensure all metadata values are strings when a trace ends."""
                if trace.metadata:
                    for key, value in list(trace.metadata.items()):
                        if not isinstance(value, str):
                            trace.metadata[key] = str(value)

                logger.debug(f"Trace ended with metadata: {trace.trace_id}")

            def on_span_start(self, span: Span) -> None:
                """Called when a span starts."""
                pass

            def on_span_end(self, span: Span) -> None:
                """Add metadata to generation spans."""
                # For generation spans, add additional metadata
                if hasattr(span.span_data, "type") and span.span_data.type == "generation":
                    # Add metadata to the span if it has a metadata attribute
                    if hasattr(span.span_data, "metadata"):
                        if span.span_data.metadata is None:
                            span.span_data.metadata = {}

                        # Add metadata - ensure all values are strings
                        span.span_data.metadata["prompt_source"] = "prompt-surfer"
                        span.span_data.metadata["captured_by"] = "prompt_metadata_processor"
                        span.span_data.metadata["timestamp"] = str(uuid.uuid4())  # Add a unique timestamp

                        # Ensure all metadata values are strings
                        for key, value in list(span.span_data.metadata.items()):
                            if not isinstance(value, str):
                                span.span_data.metadata[key] = str(value)

            def force_flush(self) -> None:
                """Force flush any buffered data."""
                pass

            def shutdown(self) -> None:
                """Shutdown the processor."""
                pass

        # Create our custom processor
        metadata_processor = PromptMetadataProcessor()

        # Get the API key
        api_key = os.environ.get("OPENAI_API_KEY")

        # Create a new backend exporter with explicit configuration
        try:
            # Create a default processor that sends traces to OpenAI
            exporter = BackendSpanExporter()
            # Set the API key on the exporter
            exporter.set_api_key(api_key)
            # Create a batch processor with the exporter
            backend_processor = BatchTraceProcessor(exporter)

            # Set the processors - this replaces any existing processors
            # We include both our metadata processor and the backend processor
            set_trace_processors([metadata_processor, backend_processor])
            logger.debug("Set up trace processors with explicit API key")
        except Exception as e:
            # If setting processors fails, try adding our processor to existing ones
            logger.debug(f"Could not set trace processors: {str(e)}")
            try:
                # Add our processor to the existing processors
                add_trace_processor(metadata_processor)
                logger.debug("Added metadata processor for tracing")
            except Exception as e:
                logger.debug(f"Could not add metadata processor: {str(e)}")

        # Only log success at INFO level for the final message
        logger.debug("Prompt tracing setup completed successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to set up prompt tracing: {str(e)}")
        return False

def create_trace_metadata(agent_name: str, user_input: str, additional_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Create metadata for a trace, ensuring all values are strings.

    Args:
        agent_name: The name of the agent being used
        user_input: The user's input to the agent
        additional_metadata: Any additional metadata to include

    Returns:
        A dictionary of metadata with string values
    """
    metadata = {
        "agent_name": str(agent_name),
        "user_input": str(user_input),
        "timestamp": str(uuid.uuid4()),  # Use a UUID as a unique timestamp
    }

    # Add any additional metadata
    if additional_metadata:
        for key, value in additional_metadata.items():
            metadata[key] = str(value)

    return metadata
