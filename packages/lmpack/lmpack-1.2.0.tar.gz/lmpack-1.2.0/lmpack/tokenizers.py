# lmpack/tokenizers.py (New File)
import logging
from typing import Protocol, Optional

log = logging.getLogger(__name__)


class TokenizerBackend(Protocol):
    """Protocol for tokenizer backends."""

    encoding_name: str

    def count_tokens(self, text: str) -> int:
        """Counts the tokens in the given text."""
        ...


class TikTokenBackend:
    """Tokenizer backend using tiktoken."""

    def __init__(self, encoding_name: str = "cl100k_base"):
        try:
            import tiktoken
        except ImportError:
            log.error(
                "tiktoken is not installed. Please install it to use token counting: "
                "pip install lmpack[tiktoken]"
            )
            raise
        self.encoding_name = encoding_name
        try:
            self._encoding = tiktoken.get_encoding(encoding_name)
            log.debug(f"Initialized tiktoken with encoding: {encoding_name}")
        except Exception as e:
            log.error(f"Failed to initialize tiktoken encoding '{encoding_name}': {e}")
            raise

    def count_tokens(self, text: str) -> int:
        """Counts the tokens using the initialized tiktoken encoding."""
        try:
            return len(self._encoding.encode(text))
        except Exception as e:
            # Log error but return 0 to avoid crashing the whole process
            log.warning(f"tiktoken failed to encode text fragment: {e}")
            return 0


class VertexAiLocalTokenizerBackend:
    """Tokenizer backend using Vertex AI (Local)."""

    def __init__(self, encoding_name: str = "gemini-1.5-pro-002"):
        try:
            from vertexai.preview import tokenization
        except ImportError:
            log.error(
                "vertexai tokenization is not installed. Please install it to use token counting: "
                "pip install lmpack[tokenization]"
            )
            raise

        # Coerce name to valid one
        if encoding_name == "gemini":
            encoding_name = "gemini-1.5-pro-002"
        if encoding_name == "gemini-1.5-pro":
            encoding_name = "gemini-1.5-pro-002"
        if encoding_name == "gemini-1.5":
            encoding_name = "gemini-1.5-flash-002"

        self.encoding_name = encoding_name
        try:
            self._encoding = tokenization.get_tokenizer_for_model(encoding_name)
            log.debug(f"Initialized Vertex AI with encoding: {encoding_name}")
        except Exception as e:
            log.error(f"Failed to initialize Vertex AI encoding '{encoding_name}': {e}")
            raise

    def count_tokens(self, text: str) -> int:
        """Counts the tokens using the initialized Vertex AI encoding."""
        try:
            result = self._encoding.count_tokens(text)
            return result.total_tokens
        except Exception as e:
            # Log error but return 0 to avoid crashing the whole process
            log.warning(f"Vertex AI failed to encode text fragment: {e}")
            return 0


class NullTokenizerBackend:
    """A tokenizer that does no counting."""

    encoding_name = "none"

    def count_tokens(self, text: str) -> int:
        return 0


# --- Factory ---
_tokenizer_instance: Optional[TokenizerBackend] = None


def get_tokenizer(
    encoding_name: str = "cl100k_base", enable_counting: bool = True
) -> TokenizerBackend:
    """Gets a tokenizer instance, creating it if necessary."""
    global _tokenizer_instance
    if not enable_counting:
        return NullTokenizerBackend()

    # Cache
    if _tokenizer_instance is not None and _tokenizer_instance.encoding_name == encoding_name:
        return _tokenizer_instance

    if encoding_name.startswith("gemini"):
        try:
            _tokenizer_instance = VertexAiLocalTokenizerBackend(encoding_name)
        except ImportError:
            # Vertex AI logs the error, provide a fallback
            print(
                f"Falling back: Token counting disabled as vertexai is unavailable for encoding '{encoding_name}'."
            )
            return NullTokenizerBackend()
    else:
        try:
            _tokenizer_instance = TikTokenBackend(encoding_name)
        except ImportError:
            # TikTokenBackend logs the error, provide a fallback
            print(
                f"Falling back: Token counting disabled as tiktoken is unavailable for encoding '{encoding_name}'."
            )
            return NullTokenizerBackend()

    return _tokenizer_instance
