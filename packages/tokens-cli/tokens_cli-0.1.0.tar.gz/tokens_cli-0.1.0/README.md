# Tokens CLI

A simple command-line tool to count tokens in text using OpenAI's tiktoken tokenizers.

## Why?

When working with LLMs and token-based API pricing, it's useful to quickly see how many tokens your text uses. This tool makes it easy to:

- Check token counts for prompt engineering
- Calculate costs for API requests
- Verify tokenization is as expected

## Installation

From PyPI:
```bash
pip install tokens-cli
# or with uv
uv pip install tokens-cli
```

For development:
```bash
# Clone the repository
git clone https://github.com/nikdavis/tokens_cli.git
cd tokens_cli

# Install locally
uv tool install .
```

## Usage

The `tokens` command (or its shorter alias `tks`) supports piping input from other commands:

```bash
# Basic usage
echo "Count how many tokens are in this text" | tokens
# or with the shorter alias
echo "Count how many tokens are in this text" | tks

# Verbose output with token count details
echo "Count tokens with detailed output" | tokens -v

# Specify model for tokenization
echo "Count tokens using gpt-4 tokenizer" | tokens -m gpt-4

# Specify encoding directly
echo "Count tokens using cl100k_base encoding" | tokens -e cl100k_base

# List available models and encodings
tokens -l
```

## Running Tests

Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

Run tests:

```bash
pytest
# or
uv run pytest
```

## Supported Models/Encodings

- `cl100k_base`: Used by ChatGPT, GPT-4, text-embedding-ada-002
- `o200k_base`: Used by GPT-4o models
- `p50k_base`: Used by code models like text-davinci-002/003
- `p50k_edit`: Used by edit models
- `r50k_base`/`gpt2`: Used by GPT-3 and GPT-2 models

## License

MIT
