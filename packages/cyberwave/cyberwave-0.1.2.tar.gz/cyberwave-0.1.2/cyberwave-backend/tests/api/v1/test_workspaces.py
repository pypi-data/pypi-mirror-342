import pytest
from httpx import AsyncClient

# Base URL of the running server
# Ensure your server is running at http://localhost:8000
BASE_URL = "http://localhost:8000/api/v1"

@pytest.mark.asyncio
async def test_read_workspaces_e2e():
    """
    Test retrieving workspaces from the running server.
    Assumes the database is already migrated and seeded.
    """
    async with AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        try:
            response = await client.get("/workspaces")
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        except Exception as e:
            pytest.fail(f"Request to {BASE_URL}/workspaces failed: {e}")

        # Check status code (already checked by raise_for_status, but good practice)
        assert response.status_code == 200

        # Check response body structure and content
        try:
            response_data = response.json()
        except Exception as e:
            pytest.fail(f"Failed to parse JSON response: {e}\nResponse text: {response.text}")

        assert isinstance(response_data, list), "Response should be a list"
        assert len(response_data) >= 1, "Should be at least one workspace (the seeded one)"

        # Find the seeded workspace and verify its details
        seeded_workspace = next((ws for ws in response_data if ws.get("name") == "Default Workspace"), None)
        assert seeded_workspace is not None, "Seeded 'Default Workspace' not found in response"
        assert seeded_workspace.get("id") == 1, "Seeded workspace should have id 1"
        assert "created_at" in seeded_workspace, "Response item should have 'created_at' field"

# You can add more E2E tests here for:
# - GET /workspaces/{id}
# - POST /workspaces
# - PUT /workspaces/{id}
# - DELETE /workspaces/{id}
# - Testing pagination (skip/limit)
# - Testing error conditions (e.g., workspace not found) 