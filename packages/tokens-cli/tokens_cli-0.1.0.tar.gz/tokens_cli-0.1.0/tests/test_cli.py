"""Tests for the tokens_cli.cli module."""

import sys
import io
import pytest
from unittest.mock import patch
from tokens_cli.cli import main


@pytest.fixture
def mock_stdin(monkeypatch):
    """Mock stdin with a specific text."""
    mock_input = io.StringIO("Hello world")
    monkeypatch.setattr(sys, 'stdin', mock_input)
    return mock_input


@pytest.fixture
def mock_isatty(monkeypatch):
    """Mock sys.stdin.isatty to return False."""
    def mock_isatty():
        return False

    monkeypatch.setattr(sys.stdin, 'isatty', mock_isatty)


def test_main_basic(mock_stdin, mock_isatty, capsys):
    """Test basic functionality of main CLI."""
    # Setup command line arguments
    with patch('sys.argv', ['tokens']):
        main()

    # Capture the output
    captured = capsys.readouterr()
    assert captured.out.strip() == "2"


def test_main_verbose(mock_stdin, mock_isatty, capsys):
    """Test verbose output of CLI."""
    # Setup command line arguments
    with patch('sys.argv', ['tokens', '-v']):
        main()

    # Capture the output
    captured = capsys.readouterr()
    assert "Token count: 2" in captured.out


def test_main_with_model(mock_stdin, mock_isatty, capsys):
    """Test CLI with specific model specified."""
    # Setup command line arguments
    with patch('sys.argv', ['tokens', '-m', 'gpt-4']):
        main()

    # Capture the output
    captured = capsys.readouterr()
    assert captured.out.strip() == "2"


def test_list_models(capsys):
    """Test the -l/--list-models option."""
    with patch('sys.argv', ['tokens', '-l']):
        main()

    # Capture the output
    captured = capsys.readouterr()
    assert "Available models and their encodings:" in captured.out
    assert "gpt-4" in captured.out
