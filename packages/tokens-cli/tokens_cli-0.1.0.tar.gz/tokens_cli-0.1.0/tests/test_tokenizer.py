"""Tests for the tokens_cli.tokenizer module."""

import pytest
from tokens_cli.tokenizer import count_tokens, get_available_encodings, ENCODINGS


def test_count_tokens_basic():
    """Test basic token counting functionality."""
    text = "Hello world"
    count = count_tokens(text)
    assert count == 2, f"Expected 2 tokens for 'Hello world', got {count}"


def test_count_tokens_with_encoding():
    """Test token counting with different encodings."""
    text = "Hello world"

    # Test with cl100k_base encoding (ChatGPT/GPT-4)
    cl100k_count = count_tokens(text, encoding_name="cl100k_base")
    assert cl100k_count == 2

    # Test with gpt2/r50k_base encoding (might tokenize differently)
    r50k_count = count_tokens(text, encoding_name="r50k_base")
    # We don't assert the exact count as different encoders may tokenize differently


def test_count_tokens_with_model():
    """Test token counting with different model names."""
    text = "Hello world"

    # Test with ChatGPT model
    gpt35_count = count_tokens(text, model_name="gpt-3.5-turbo")
    assert gpt35_count == 2

    # Test with a GPT-3 model
    davinci_count = count_tokens(text, model_name="davinci")
    # Different models might tokenize differently


def test_special_tokens():
    """Test tokenization of special characters."""
    text = "Hello, world! How are you doing today? 123.45"
    count = count_tokens(text)
    # Just verify we get a positive count - exact count will vary by encoder
    assert count > 0


def test_get_available_encodings():
    """Test the get_available_encodings function."""
    encodings = get_available_encodings()
    assert len(encodings) > 0
    assert "cl100k_base" in encodings


def test_encodings_mapping():
    """Test that the ENCODINGS mapping contains expected models."""
    assert "gpt-3.5-turbo" in ENCODINGS
    assert "gpt-4" in ENCODINGS
    assert "gpt-4o" in ENCODINGS
    assert ENCODINGS["gpt-4o"] == "o200k_base"
