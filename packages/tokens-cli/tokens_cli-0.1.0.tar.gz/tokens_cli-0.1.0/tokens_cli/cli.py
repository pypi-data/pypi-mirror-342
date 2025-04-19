"""Command-line interface for tokens."""

import sys
import argparse
from .tokenizer import count_tokens, get_available_encodings, ENCODINGS


def main():
    """Process input from stdin and count tokens."""
    parser = argparse.ArgumentParser(description="Count tokens in text using tiktoken encoders")

    # Model and encoding options
    model_group = parser.add_mutually_exclusive_group()
    model_group.add_argument(
        "-m", "--model",
        choices=list(ENCODINGS.keys()),
        help="Specify the model to use for tokenization"
    )
    model_group.add_argument(
        "-e", "--encoding",
        choices=get_available_encodings(),
        help="Specify the encoding to use directly"
    )

    # Output options
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show more detailed output"
    )
    parser.add_argument(
        "-l", "--list-models",
        action="store_true",
        help="List available models and encodings"
    )

    args = parser.parse_args()

    # Handle listing models
    if args.list_models:
        print("Available models and their encodings:")
        for model, encoding in sorted(ENCODINGS.items()):
            print(f"  {model:20} {encoding}")
        return 0

    # Read from stdin if available, otherwise prompt
    if not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Enter text to tokenize (press Ctrl+D when finished):")
        text = sys.stdin.read()

    # Count tokens
    token_count = count_tokens(
        text,
        encoding_name=args.encoding,
        model_name=args.model
    )

    # Output
    if args.verbose:
        model_name = args.model or "default"
        encoding_name = args.encoding or ENCODINGS.get(args.model, "cl100k_base")
        print(f"Model: {model_name}")
        print(f"Encoding: {encoding_name}")
        print(f"Token count: {token_count}")
    else:
        print(token_count)

    return 0


if __name__ == "__main__":
    sys.exit(main())
