import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from ocr_pipeline import OCRPipeline

@pytest.fixture
def ocr():
    return OCRPipeline()

@patch('ocr_pipeline.convert_from_path')
@patch('ocr_pipeline.pytesseract.image_to_string')
def test_process_pdf(mock_image_to_string, mock_convert, ocr):
    # Mocking single page PDF
    mock_convert.return_value = [MagicMock()]
    mock_image_to_string.return_value = "This is some   noisy \n \n text  "
    
    result = ocr.process_pdf("dummy.pdf")
    
    assert "This is some noisy text" in result
    mock_convert.assert_called_once_with("dummy.pdf")
    mock_image_to_string.assert_called_once()

@patch('ocr_pipeline.pytesseract.image_to_string')
def test_process_image(mock_image_to_string, ocr):
    mock_image_to_string.return_value = "This is\n  an image text"
    
    result = ocr.process_image("dummy.jpg")
    
    assert result == "This is\n an image text"
    mock_image_to_string.assert_called_once_with("dummy.jpg")

def test_clean_text(ocr):
    messy_text = "   Hello   World  \n\n  This \t is a test. \n \n \n"
    clean_text = ocr.clean_text(messy_text)
    assert clean_text == "Hello World\n This is a test."
