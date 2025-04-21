"""Test CLI functionality."""

from unittest.mock import patch

from fmla.cli import get_pip_guide, get_pip_info, main


def test_get_pip_info() -> None:
    """Test that PIP info is returned."""
    info = get_pip_info()
    assert isinstance(info, str)
    assert "PIP: Performance Improvement Plan" in info
    assert len(info) > 0


def test_get_pip_guide() -> None:
    """Test that PIP guide is returned with FMLA information."""
    guide = get_pip_guide()
    assert isinstance(guide, str)
    assert "Guide to Surviving a PIP and Using FMLA" in guide
    assert "MENTAL STRATEGIES:" in guide
    assert "FMLA INFORMATION:" in guide
    assert "FMLA: Family and Medical Leave Act" in guide
    assert len(guide) > 0


def test_main_info_command() -> None:
    """Test that info command works."""
    with patch("builtins.print") as mock_print:
        result = main(["info"])
        assert result == 0
        mock_print.assert_called_once()
        args, _ = mock_print.call_args
        assert "PIP: Performance Improvement Plan" in args[0]


def test_main_guide_command() -> None:
    """Test that guide command works with FMLA information."""
    with patch("builtins.print") as mock_print:
        result = main(["guide"])
        assert result == 0
        mock_print.assert_called_once()
        args, _ = mock_print.call_args
        assert "Guide to Surviving a PIP and Using FMLA" in args[0]
        assert "MENTAL STRATEGIES:" in args[0]
        assert "FMLA INFORMATION:" in args[0]


def test_main_no_args() -> None:
    """Test that help is shown when no command is provided."""
    with patch("argparse.ArgumentParser.print_help") as mock_print_help:
        result = main([])
        assert result == 1
        mock_print_help.assert_called_once()
