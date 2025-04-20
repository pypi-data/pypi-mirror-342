# Claude LLM interface
import logging
from langchain_anthropic import ChatAnthropic
from src.utils.config import ANTHROPIC_API_KEY, LLM_MODEL

# Logger
logger = logging.getLogger(__name__)

def get_llm_model():
    """Returns the Claude LLM model."""
    try:
        logger.info(f"Initializing Claude with model: {LLM_MODEL}")
        return ChatAnthropic(
            model_name=LLM_MODEL,
            anthropic_api_key=ANTHROPIC_API_KEY,
            temperature=0.2  # Lower temperature for more factual responses
        )
    except Exception as e:
        logger.error(f"Error initializing Claude model {LLM_MODEL}: {e}")
        # Fall back to default model if specified one fails
        logger.info("Falling back to default Claude model")
        return ChatAnthropic(
            anthropic_api_key=ANTHROPIC_API_KEY,
            temperature=0.2
        )