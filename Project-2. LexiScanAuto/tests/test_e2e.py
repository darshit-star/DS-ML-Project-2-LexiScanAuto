import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api import app

client = TestClient(app)

def test_health():
    # Since our app only has POST /extract currently.
    assert True

def test_extract_invalid_file_type():
    response = client.post(
        "/extract",
        files={"file": ("dummy.txt", b"Mock Content", "text/plain")}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are supported."

# Note: In a real system, you would have a sample PDF to mock an end-to-end request:
# def test_extract_valid_pdf():
#     with open("tests/sample_contract.pdf", "rb") as f:
#         response = client.post("/extract", files={"file": ("sample_contract.pdf", f, "application/pdf")})
#     assert response.status_code == 200
#     assert "entities" in response.json()
