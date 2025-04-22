import pytest
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from formatter.formatter_md import FormatterMD
from models import PDFResult, FormattedResult


@pytest.fixture
def mock_pdf_result():
    return PDFResult(
        metadata={
            "format": "PDF 1.7",
            "title": "Sample",
            "author": "Author",
            "subject": "",
            "keywords": "",
            "creator": "Creator",
            "producer": "Producer",
            "creationDate": "2023-01-01",
            "modDate": "2023-01-01",
            "trapped": "",
            "encryption": None,
            "file_path": "/path/to/sample.pdf",
            "page_count": 1,
            "page": 1
        },
        toc_items=[],
        tables=[],
        images=[],
        graphics=[],
        text="# Sample Document\n\nThis is a sample text with a [link](https://example.com).\n\n- Item 1\n- Item 2\n\n1. Numbered item 1\n2. Numbered item 2",
        words=[]
    )


@pytest.fixture
def mock_pdf_result_empty_text():
     return PDFResult(
        metadata={
            "format": "PDF 1.7",
            "title": "Empty",
            "author": "",
            "subject": "",
            "keywords": "",
            "creator": "",
            "producer": "",
            "creationDate": "",
            "modDate": "",
            "trapped": "",
            "encryption": None,
            "file_path": "/path/to/empty.pdf",
            "page_count": 1,
            "page": 1
        },
        toc_items=[],
        tables=[],
        images=[],
        graphics=[],
        text="",
        words=[]
    )


def test_init_formatter(mock_pdf_result):
    formatter = FormatterMD([mock_pdf_result])
    assert formatter.content == [mock_pdf_result]
    assert hasattr(formatter, 'encoding')


def test_check_content_valid(mock_pdf_result):
    formatter = FormatterMD([mock_pdf_result])
    formatter._check_content()


def test_check_content_not_list():
    formatter = FormatterMD("not a list")
    
    with pytest.raises(ValueError) as excinfo:
        formatter._check_content()
    
    assert "Content must be a List of PDFResult" in str(excinfo.value)


def test_check_content_empty_list():
    formatter = FormatterMD([])
    
    with pytest.raises(ValueError) as excinfo:
        formatter._check_content()
    
    assert "Content is empty" in str(excinfo.value)


def test_check_content_invalid_item():
    formatter = FormatterMD(["not a PDFResult"])
    
    with pytest.raises(ValueError) as excinfo:
        formatter._check_content()
    
    assert "Content must be a List of PDFResult" in str(excinfo.value)


def test_check_content_empty_text(mock_pdf_result_empty_text):
    formatter = FormatterMD([mock_pdf_result_empty_text])
    
    with pytest.raises(ValueError) as excinfo:
        formatter._check_content()
    
    assert "Content text is empty" in str(excinfo.value)


def test_count_markdown_elements():
    formatter = FormatterMD([])
    
    markdown_text = """# Title
## Subtitle

- Item 1
- Item 2

1. First
2. Second

[Link 1](https://example.com)
<https://example.org>
"""
    
    elements = formatter._count_markdown_elements(markdown_text)
    
    assert len(elements['titles']) == 2
    assert len(elements['lists']) == 4
    assert len(elements['links']) == 2
    assert elements['links'][0].text == "Link 1"
    assert elements['links'][0].url == "https://example.com"
    assert elements['links'][1].text == "https://example.org"
    assert elements['links'][1].url == "https://example.org"


def test_count_markdown_elements_empty():
    formatter = FormatterMD([])
    
    elements = formatter._count_markdown_elements("")
    
    assert len(elements['titles']) == 0
    assert len(elements['lists']) == 0
    assert len(elements['links']) == 0


def test_count_markdown_elements_error():
    formatter = FormatterMD([])
    
    def mock_findall_error(*args, **kwargs):
        raise Exception("Test exception")
    
    original_findall = re.findall
    re.findall = mock_findall_error
    
    try:
        with pytest.raises(ValueError) as excinfo:
            formatter._count_markdown_elements("Test text")
        
        assert "Error counting markdown elements" in str(excinfo.value)
    finally:
        re.findall = original_findall


def test_format_success(mock_pdf_result, monkeypatch):
    formatter = FormatterMD([mock_pdf_result])
    
    def mock_detect(text):
        return "en"
    
    monkeypatch.setattr("langdetect.detect", mock_detect)
    
    result = formatter.format()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FormattedResult)
    assert result[0].metadata.file_path == "/path/to/sample.pdf"
    assert result[0].metadata.page == 1
    assert len(result[0].elements.titles) == 1
    assert len(result[0].elements.lists) == 4
    assert len(result[0].elements.links) == 1
    assert result[0].language == "en"
    assert result[0].tokens > 0


def test_format_error():
    formatter = FormatterMD(["not a PDFResult"])
    
    with pytest.raises(ValueError) as excinfo:
        formatter.format()
    
    assert "Error formatting content" in str(excinfo.value)


def test_format_with_missing_attributes(mock_pdf_result, monkeypatch):
    delattr(mock_pdf_result, 'tables')
    
    formatter = FormatterMD([mock_pdf_result])
    
    def mock_detect(text):
        return "en"
    
    monkeypatch.setattr("langdetect.detect", mock_detect)
    
    result = formatter.format()
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FormattedResult)
    assert isinstance(result[0].elements.tables, list)
    assert len(result[0].elements.tables) == 0 