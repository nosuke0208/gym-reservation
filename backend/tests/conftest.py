# backend/tests/conftest.py
import os
import sys

os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault(
    "SUPABASE_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJyb2xlIjoic2VydmljZV9yb2xlIn0"
    ".test-signature-placeholder",
)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def api_client():
    """supabaseをモックしたFastAPI TestClientを返すfixture"""
    mock_sb = MagicMock()
    with patch("main.supabase", mock_sb):
        import main
        yield TestClient(main.app), mock_sb
