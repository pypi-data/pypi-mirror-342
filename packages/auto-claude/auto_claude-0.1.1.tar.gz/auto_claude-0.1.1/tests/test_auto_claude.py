import pytest

from src.auto_claude.auto_claude import main


def test_auto_claude_runs():
    try:
        main()
    except Exception as e:
        pytest.fail(f"auto_claude.main() raised an exception: {e}")
