import pytest
from httpx import AsyncClient

# Base URL of the running server
# Ensure your server is running at http://localhost:8000
BASE_URL = "http://localhost:8000/api/v1"

@pytest.mark.asyncio
async def test_read_robots_e2e():
    """
    Test retrieving robots from the running server.
    Assumes the database is already migrated and seeded.
    """
    async with AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        try:
            # This endpoint should now exist
            response = await client.get("/robots")
            response.raise_for_status() # Raise an exception for bad status codes
        except Exception as e:
            pytest.fail(f"Request to {BASE_URL}/robots failed: {e}")

        assert response.status_code == 200

        try:
            response_data = response.json()
        except Exception as e:
            pytest.fail(f"Failed to parse JSON response: {e}\nResponse text: {response.text}")

        assert isinstance(response_data, list), "Response should be a list"
        assert len(response_data) >= 2, "Should be at least the 2 seeded robots"

        agv_alpha = next((r for r in response_data if r.get("name") == "AGV-Alpha"), None)
        agv_beta = next((r for r in response_data if r.get("name") == "AGV-Beta"), None)

        assert agv_alpha is not None, "Seeded 'AGV-Alpha' not found"
        assert agv_beta is not None, "Seeded 'AGV-Beta' not found"
        assert agv_alpha.get("id") == 601
        assert agv_beta.get("id") == 602
        assert "registration_date" in agv_alpha
        assert agv_alpha.get("robot_type") == "agv/model-x"

@pytest.mark.asyncio
async def test_create_robot_frictionless_flow_e2e():
    """
    Test the frictionless onboarding flow:
    1. Create robot without token -> get token
    2. Create another robot with token
    3. Verify access with/without token
    4. Cleanup
    """
    share_token = None
    robot_ids_to_delete = []

    async with AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        try:
            # === Step 1: Create first robot (no token) ===
            print("\nTesting Step 1: Create first robot without token...")
            robot_1_data = {"name": "TempBot-1", "robot_type": "tester_v1"} # No level_id
            response1 = await client.post("/robots", json=robot_1_data)

            assert response1.status_code == 201, f"Expected 201, got {response1.status_code}. Response: {response1.text}"
            response1_data = response1.json()
            
            assert "id" in response1_data
            robot_ids_to_delete.append(response1_data["id"])
            
            assert "share_token" in response1_data
            share_token = response1_data["share_token"]
            assert share_token is not None, "share_token should be returned for new session"
            
            assert "share_url" in response1_data
            assert response1_data["share_url"] is not None
            
            # Check header as well
            assert "X-Share-Token" in response1.headers
            assert response1.headers["X-Share-Token"] == share_token
            print(f"Step 1 Success: Created Robot ID {response1_data['id']}, got share_token {share_token}")

            # === Step 2: Create second robot (with token) ===
            print("\nTesting Step 2: Create second robot with token...")
            robot_2_data = {"name": "TempBot-2", "robot_type": "tester_v2"}
            headers = {"X-Share-Token": share_token}
            response2 = await client.post("/robots", json=robot_2_data, headers=headers)
            
            assert response2.status_code == 201, f"Expected 201, got {response2.status_code}. Response: {response2.text}"
            response2_data = response2.json()

            assert "id" in response2_data
            robot_ids_to_delete.append(response2_data["id"])
            
            # Should NOT return a new token when using an existing one
            assert response2_data.get("share_token") is None
            assert response2_data.get("share_url") is None
            print(f"Step 2 Success: Created Robot ID {response2_data['id']} using existing token")

            # === Step 3: Verify access (with token) ===
            print("\nTesting Step 3: Verify access with token...")
            robot1_id = response1_data["id"]
            robot2_id = response2_data["id"]
            
            # Get Robot 1
            get_r1_resp = await client.get(f"/robots/{robot1_id}", headers=headers)
            assert get_r1_resp.status_code == 200, f"Failed to get Robot 1 with token. Status: {get_r1_resp.status_code}"
            assert get_r1_resp.json()["id"] == robot1_id

            # Get Robot 2
            get_r2_resp = await client.get(f"/robots/{robot2_id}", headers=headers)
            assert get_r2_resp.status_code == 200, f"Failed to get Robot 2 with token. Status: {get_r2_resp.status_code}"
            assert get_r2_resp.json()["id"] == robot2_id
            print("Step 3 Success: Verified access to both robots with token")

            # === Step 4: Verify NO access (without token) ===
            print("\nTesting Step 4: Verify NO access without token...")
            get_r1_no_token_resp = await client.get(f"/robots/{robot1_id}") # No headers
            assert get_r1_no_token_resp.status_code == 403, f"Expected 403 Forbidden without token, got {get_r1_no_token_resp.status_code}"
            print("Step 4 Success: Verified 403 Forbidden when accessing without token")

        finally:
            # === Step 5: Cleanup (with token) ===
            print("\nTesting Step 5: Cleanup created robots...")
            if share_token and robot_ids_to_delete:
                headers = {"X-Share-Token": share_token}
                for robot_id in robot_ids_to_delete:
                    print(f"Deleting robot {robot_id}...")
                    delete_resp = await client.delete(f"/robots/{robot_id}", headers=headers)
                    assert delete_resp.status_code == 200, f"Failed to delete robot {robot_id}. Status: {delete_resp.status_code}"
                print("Cleanup Success: Robots deleted")
            else:
                print("Skipping cleanup as not all necessary info was available (token/IDs)")

# Add more tests later for claiming, expiration, etc.

# Add more tests later for POST, PUT, DELETE, GET by ID etc. 