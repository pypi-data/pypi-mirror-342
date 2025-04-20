"""
Tracing configuration for OpenAI Agents SDK.
This module provides functions to configure tracing for the OpenAI Agents SDK.
"""

import os
import logging
import importlib.metadata

logger = logging.getLogger(__name__)

def configure_tracing():
    """
    Configure tracing for the OpenAI Agents SDK.
    This function sets up the necessary configuration for tracing to work properly.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY environment variable not set. Tracing will not work.")
        return False

    try:
        # Import the necessary functions from the OpenAI Agents SDK
        from agents import set_tracing_export_api_key, set_default_openai_key, set_tracing_disabled
        from agents.tracing.processors import BackendSpanExporter, BatchTraceProcessor
        from agents.tracing import set_trace_processors, add_trace_processor
        import agents

        # Get the OpenAI Agents SDK version (log at debug level)
        try:
            agents_version = importlib.metadata.version('openai-agents')
            logger.debug(f"OpenAI Agents SDK version: {agents_version}")
        except importlib.metadata.PackageNotFoundError:
            logger.debug(f"OpenAI Agents SDK version: {getattr(agents, '__version__', 'unknown')}")

        # Set the API key for tracing export
        set_tracing_export_api_key(api_key)
        logger.debug("API key set for tracing export")

        # Also set the default OpenAI key to ensure consistency
        set_default_openai_key(api_key)
        logger.debug("Default OpenAI key set")

        # Explicitly enable tracing
        set_tracing_disabled(False)
        logger.debug("Tracing explicitly enabled")

        # Configure logging level for the OpenAI Agents SDK
        # Set to WARNING to reduce console output while keeping tracing functional
        import logging
        logging.getLogger("openai.agents").setLevel(logging.WARNING)
        logging.getLogger("openai.agents.tracing").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)

        # Ensure tracing is enabled via environment variables as well
        os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "0"

        # Include sensitive data for complete tracing
        os.environ["OPENAI_AGENTS_DONT_LOG_MODEL_DATA"] = "0"  # Set to 0 to include model data
        os.environ["OPENAI_AGENTS_DONT_LOG_TOOL_DATA"] = "0"   # Set to 0 to include tool data

        # Create a new backend exporter with explicit configuration
        try:
            # Create a default processor that sends traces to OpenAI
            exporter = BackendSpanExporter()
            # Set the API key on the exporter
            exporter.set_api_key(api_key)
            # Create a batch processor with the exporter
            processor = BatchTraceProcessor(exporter)
            # Set the processor as the only processor
            set_trace_processors([processor])
            logger.debug("Configured trace processor with explicit API key")
        except Exception as e:
            logger.debug(f"Could not configure trace processor: {str(e)}")

        # Only log success at INFO level
        logger.debug("Tracing configured successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to configure tracing: {str(e)}")
        return False
