import json
import pytest
from fetch_meditation.spad_entry import SpadEntry


@pytest.fixture
def sample_entry():
    return SpadEntry(
        "2023-10-26",
        "Sample Title",
        "Sample Page",
        "Sample Quote",
        "Sample Source",
        ["Content Line 1", "Content Line 2"],
        "Sample Thought",
        "Sample Copyright",
    )


def test_spad_entry_properties(sample_entry):
    entry = sample_entry

    assert isinstance(entry.date, str)
    assert isinstance(entry.title, str)
    assert isinstance(entry.page, str)
    assert isinstance(entry.quote, str)
    assert isinstance(entry.source, str)
    assert isinstance(entry.content, list)
    assert isinstance(entry.thought, str)
    assert isinstance(entry.copyright, str)


def test_spad_entry_without_tags(sample_entry):
    entry = sample_entry
    entry.title = "Sample <br>Title"

    result = entry.without_tags()
    assert result["title"] == "Sample Title"


def test_spad_entry_to_json(sample_entry):
    entry = sample_entry
    response_data = entry.to_json()
    decoded_response = json.loads(response_data)

    assert decoded_response is not None
    assert "date" in decoded_response
    assert "title" in decoded_response
    assert "page" in decoded_response
    assert "quote" in decoded_response
    assert "source" in decoded_response
    assert "content" in decoded_response
    assert "thought" in decoded_response
    assert "copyright" in decoded_response
