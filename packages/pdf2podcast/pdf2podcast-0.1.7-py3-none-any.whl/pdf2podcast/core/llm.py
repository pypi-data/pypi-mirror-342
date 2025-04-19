"""
Large Language Model (LLM) implementations for pdf2podcast.
"""

import os
import re
import time
import logging
from typing import Dict, Any, Optional, Callable
from functools import wraps
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core import retry
from google.api_core.exceptions import GoogleAPIError
from .base import BaseLLM
from .prompts import PodcastPromptBuilder

# Setup logging
logger = logging.getLogger(__name__)


def retry_on_exception(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (GoogleAPIError,),
) -> Callable:
    """
    Retry decorator with exponential backoff.

    Args:
        retries (int): Maximum number of retries
        delay (float): Initial delay between retries in seconds
        backoff (float): Backoff multiplier
        exceptions (tuple): Exceptions to catch
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_delay = delay
            last_exception = None

            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if i < retries - 1:
                        logger.warning(
                            f"Attempt {i + 1}/{retries} failed: {str(e)}. "
                            f"Retrying in {retry_delay:.1f}s..."
                        )
                        time.sleep(retry_delay)
                        retry_delay *= backoff
                    else:
                        logger.error(f"All {retries} attempts failed.")

            raise last_exception

        return wrapper

    return decorator


class GeminiLLM(BaseLLM):
    """
    Google's Gemini-based LLM implementation with optimized content generation.
    """

    def __init__(
        self,
        api_key: str = None,
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0.2,
        top_p: float = 0.9,
        max_output_tokens: int = 4096,
        streaming: bool = False,
        prompt_builder: PodcastPromptBuilder = None,
    ):
        """
        Initialize Gemini LLM system.

        Args:
            api_key (str, optional): Google API key. If not provided, will look for GENAI_API_KEY env var
            model_name (str): Name of the Gemini model to use (default: "gemini-1.5-flash")
            temperature (float): Sampling temperature (default: 0.2)
            top_p (float): Nucleus sampling parameter (default: 0.9)
            max_output_tokens (int): Maximum output length (default: 4096)
            streaming (bool): Whether to use streaming mode (default: False)
            prompt_builder (Optional[PodcastPromptBuilder]): Custom prompt builder
        """
        super().__init__(prompt_builder or PodcastPromptBuilder())

        if api_key is None:
            load_dotenv()
            api_key = os.getenv("GENAI_API_KEY")
            if not api_key:
                raise ValueError("No API key provided and GENAI_API_KEY not found")

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_output_tokens,
            streaming=streaming,
            google_api_key=api_key,
        )

    def _clean_text(self, text: str) -> str:
        """
        Clean text using regex patterns to remove visual references and formatting.

        Args:
            text (str): Input text to clean

        Returns:
            str: Cleaned text with visual references removed
        """
        patterns = [
            r"(Figure|Fig\.|Table|Image)\s+\d+[a-z]?",
            r"(shown|illustrated|depicted|as seen) (in|on|above|below)",
            r"(refer to|see|view) (figure|table|image)",
            r"\(fig\.\s*\d+\)",
            r"as (shown|depicted) (here|below|above)",
        ]

        processed = text
        for pattern in patterns:
            processed = re.sub(pattern, "", processed, flags=re.IGNORECASE)

        processed = re.sub(r"\s+", " ", processed)
        return processed.strip()

    def _expand_content(
        self, text: str, script: str, max_attempts: int = 3, **kwargs: Dict[str, Any]
    ) -> str:
        """
        Expand the content of the script to meet minimum length requirements.

        Args:
            text (str): Original text to be expanded
            script (str): Current script
            max_attempts (int): Maximum number of attempts for expansion
            **kwargs: Additional parameters for customization, including:
                - min_length (int): Minimum length of the generated script

        Returns:
            str: Expanded script
        """
        attempts = 0
        min_length = kwargs.get("min_length", 10000)
        while len(script) < min_length and attempts < max_attempts:
            logger.info(
                f"Attempting to expand script ({len(script)} characters) to at least {min_length} characters."
            )
            expand_prompt = self.prompt_builder.build_expand_prompt(
                text=text,
                script=script,
                **kwargs,
            )
            response = self.llm.invoke(expand_prompt)
            script = response.content.strip()
            attempts += 1

        if len(script) < min_length:
            logger.info(f"Failed to expand script to required length ({min_length})")

        return script

    @retry_on_exception()
    def generate_podcast_script(
        self,
        text: str,
        **kwargs: Dict[str, Any],
    ) -> str:
        """
        Generate a coherent podcast script adapted to target audience and complexity.

        Args:
            text (str): Input text to convert into a podcast script
            **kwargs: Additional parameters for customization, including:
                - complexity (str): Desired complexity level ("simple", "intermediate", "advanced")
                - target_audience (str): Target audience category ("general", "technical", "expert")
                - min_length (int): Minimum length of the generated script
                - max_attempts (int): Maximum attempts for expansion

        Returns:
            str: Generated podcast script
        """
        try:
            # Clean and validate input text
            if not text or not text.strip():
                raise ValueError("Input text cannot be empty")

            processed_text = self._clean_text(text)
            if not processed_text:
                raise ValueError("Text cleaning resulted in empty content")

            min_length = kwargs.get("min_length", 10000)

            # Generate initial script
            try:
                prompt = self.prompt_builder.build_prompt(
                    text=processed_text,
                    **kwargs,
                )

                response = self.llm.invoke(prompt)
                script = response.content.strip()

                # Expand if needed
                if len(script) < min_length:
                    logger.info(
                        f"Initial script length ({len(script)}) below target ({min_length}). "
                        "Expanding content..."
                    )
                    script = self._expand_content(
                        text=text, script=script, min_length=min_length
                    )
                else:
                    logger.info(
                        f"Script generated successfully with length: {len(script)}"
                    )

                logger.info(f"Successfully generated script of length {len(script)}")
                return script

            except GoogleAPIError as e:
                logger.error(f"Google API error: {str(e)}")
                raise  # Will be caught by retry decorator
            except Exception as e:
                logger.error(f"Unexpected error in script generation: {str(e)}")
                raise Exception(f"Failed to generate podcast script: {str(e)}")

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Script generation failed: {str(e)}")
            raise
