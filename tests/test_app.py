from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert all("participants" in details for details in data.values())


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Basketball Team"
    email = f"student-{uuid4().hex}@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    email = f"student-{uuid4().hex}@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400():
    # Arrange
    activity_name = "Swimming Club"
    email = f"duplicate-{uuid4().hex}@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert response.status_code == 200

    # Act
    duplicate_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student is already signed up for this activity"


def test_root_redirects_to_static_index():
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
