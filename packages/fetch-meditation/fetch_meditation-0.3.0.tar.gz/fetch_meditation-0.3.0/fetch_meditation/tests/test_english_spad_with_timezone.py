import pytest
import unittest.mock as mock
import urllib.parse
from fetch_meditation.spad_language import SpadLanguage
from fetch_meditation.spad_settings import SpadSettings
from fetch_meditation.english_spad import EnglishSpad


def test_timezone_parameter_used():
    """Test that the time_zone parameter from settings is used when creating the params dictionary."""
    # Create a settings object with a timeZone
    time_zone = "Australia/Sydney"
    settings = SpadSettings(SpadLanguage.English, time_zone=time_zone)
    spad = EnglishSpad(settings)

    # Mock http_get to capture the params argument
    with mock.patch("fetch_meditation.english_spad.HttpUtility.http_get") as mock_http_get:
        # Set up mock to return valid HTML
        mock_http_get.return_value = """
        <table>
            <tr><td>April 23, 2025</td></tr>
            <tr><td>Test Title</td></tr>
            <tr><td>Page 123</td></tr>
            <tr><td>Test Quote</td></tr>
            <tr><td>Test Source</td></tr>
            <tr><td>Test Content<br/>Line 2</td></tr>
            <tr><td>divider</td></tr>
            <tr><td>Test Thought</td></tr>
            <tr><td>Test Copyright</td></tr>
        </table>
        """

        # Call the fetch method
        spad.fetch()

        # Check that http_get was called with the right parameters
        mock_http_get.assert_called_once()

        # Get the params argument
        args, kwargs = mock_http_get.call_args
        assert len(args) >= 2, "http_get should be called with at least 2 arguments"

        # The second argument should be the params dictionary
        params = args[1]
        assert params is not None, "params should not be None"
        assert isinstance(params, dict), "params should be a dictionary"
        assert "timeZone" in params, "timeZone key not found in params"
        assert (
            params["timeZone"] == time_zone
        ), f"Expected timeZone={time_zone}, got {params['timeZone']}"
