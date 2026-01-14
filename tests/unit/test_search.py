"""Unit tests suite for the search module"""
import pytest
from pydantic import ValidationError

from src.search import ieee  # pylint: disable=E0401


class TestSearchSuite:
    """Test suite for the search function."""
    def test_search_raises_validation_error_without_arguments(self) -> None:  # noqa: E501 pylint: disable=C0301
        """Test if running without arguments raises validation error."""
        with pytest.raises(ValidationError):
            ieee.search()


class TestExtractResultsInformationSuite:
    """Test suite for the extract_results_information function."""
    def test_extract_results_information_raises_validation_error_without_arguments(self) -> None:  # noqa: E501 pylint: disable=C0301
        """Test if running without arguments raises validation error."""
        with pytest.raises(ValidationError):
            ieee.extract_results_information()
