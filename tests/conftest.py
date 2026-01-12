import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_s3():
    return MagicMock()

@pytest.fixture
def mock_repo():
    return MagicMock()
