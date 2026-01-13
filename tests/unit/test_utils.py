"""Unit tests suite for utils.py"""
import pytest
from pydantic import ValidationError

from src import utils  # pylint: disable=E0401


class TestWritePrettyJSONToFileSuite:
    """Test suite for the write_pretty_json_to_file function."""
    def test_write_pretty_json_to_file_raises_validation_error_without_arguments(self) -> None:  # noqa: E501 pylint: disable=C0301
        """Test if running without arguments raises validation error."""
        with pytest.raises(ValidationError):
            utils.write_pretty_json_to_file()
