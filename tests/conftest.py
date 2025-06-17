"""
Pytest configuration and fixtures
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def mock_gemini_client():
    """Mock Gemini client for testing"""
    client = Mock()
    client.analyze_requirement = AsyncMock(return_value={
        "category": "functional",
        "complexity": "medium",
        "dependencies": [],
        "risk_areas": [],
        "testing_types": ["unit"]
    })
    client.analyze_feature_dependency = AsyncMock(return_value={
        "impact_areas": ["testing"],
        "risk_score": 5,
        "mitigation_strategies": ["thorough_testing"]
    })
    return client


@pytest.fixture
def mock_graph_repository():
    """Mock graph repository for testing"""
    repo = Mock()
    repo.store_requirement = AsyncMock(return_value="mock_req_id")
    repo.store_dependency = AsyncMock(return_value="mock_dep_id")
    return repo


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
