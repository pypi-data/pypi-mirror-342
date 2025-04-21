"""Test welcome message functionality."""

from unittest.mock import patch

from fmla import get_welcome_messages, welcome


def test_welcome_message() -> None:
    """Test that a welcome message is printed."""
    with patch("builtins.print") as mock_print:
        welcome()
        mock_print.assert_called_once()
        args, _ = mock_print.call_args
        assert args[0] in get_welcome_messages()


def test_welcome_function_exists() -> None:
    """Test that welcome function exists."""
    assert callable(welcome)


def test_get_welcome_messages() -> None:
    """Test that welcome messages list is not empty."""
    messages = get_welcome_messages()
    assert len(messages) > 0
    assert isinstance(messages[0], str)
