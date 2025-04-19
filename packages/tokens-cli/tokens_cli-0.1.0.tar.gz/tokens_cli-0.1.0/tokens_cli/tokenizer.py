"""Token counting functionality using tiktoken encoders."""

import tiktoken

# Mapping of model names to encodings
ENCODINGS = {
    "gpt-3.5-turbo": "cl100k_base",  # ChatGPT models
    "gpt-4": "cl100k_base",          # GPT-4 models (pre 4o)
    "gpt-4o": "o200k_base",          # GPT-4o models
    "text-embedding-ada-002": "cl100k_base",
    "text-davinci-002": "p50k_base",  # Code models
    "text-davinci-003": "p50k_base",
    "text-davinci-edit-001": "p50k_edit",  # Edit models
    "davinci": "r50k_base",  # GPT-3 models
    "gpt2": "r50k_base",     # GPT-2 models
}

# Default encoding to use
DEFAULT_ENCODING = "cl100k_base"


def count_tokens(text, encoding_name=None, model_name=None):
    """
    Count tokens in the provided text using tiktoken.

    Args:
        text: The text to tokenize
        encoding_name: The name of the encoding to use (e.g., "cl100k_base", "p50k_base")
        model_name: The name of the model to use for tokenization (e.g., "gpt-4", "gpt-3.5-turbo")

    Returns:
        int: The number of tokens
    """
    if model_name:
        encoding_name = ENCODINGS.get(model_name, DEFAULT_ENCODING)
    elif not encoding_name:
        encoding_name = DEFAULT_ENCODING

    # Get the encoding
    encoding = tiktoken.get_encoding(encoding_name)

    # Encode the text and count tokens
    tokens = encoding.encode(text)
    return len(tokens)


def get_available_encodings():
    """Return a list of available tiktoken encodings."""
    return list(set(ENCODINGS.values()))
