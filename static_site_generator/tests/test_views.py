"""Test views."""

import pytest

from static_site_generator.core.views import extract_title


@pytest.mark.parametrize(
    "text, expected",
    [
        ("#   Hello world   ", "Hello world"),
        ("#  Hello  world", "Hello  world"),
    ],
)
def test_extract_title(text, expected):
    """Test that `extract_title` works correctly."""
    assert extract_title(text) == expected
