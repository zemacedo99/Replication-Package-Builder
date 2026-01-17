"""Unit tests suite for the data module"""
import pytest
from pydantic import ValidationError

from src.data import process  # pylint: disable=E0401


@pytest.mark.skip("Work in progress")
class TestFilterAfterAgileManifestoDateSuite:
    """Test suite for the filter_after_agile_manifesto_date function."""
    def test_filter_after_agile_manifesto_date_raises_validation_error_without_arguments(self) -> None:  # noqa: E501 pylint: disable=C0301
        """Test if running without arguments raises validation error."""
        with pytest.raises(ValidationError):
            process.filter_after_agile_manifesto_date()


class TestProcessAndSaveResultSuite:
    """Test suite for the process_and_save_result function."""
    def test_process_and_save_result_raises_validation_error_without_arguments(self) -> None:  # noqa: E501 pylint: disable=C0301
        """Test if running without arguments raises validation error."""
        with pytest.raises(ValidationError):
            process.process_and_save_result()


class TestProcessAndSaveResultsSuite:
    """Test suite for the process_and_save_results function."""
    def test_process_and_save_results_raises_validation_error_without_arguments(self) -> None:  # noqa: E501 pylint: disable=C0301
        """Test if running without arguments raises validation error."""
        with pytest.raises(ValidationError):
            process.process_and_save_results()
