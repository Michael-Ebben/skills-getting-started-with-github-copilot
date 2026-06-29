from src.app import activities


def test_signup_adds_participant_successfully(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_when_already_registered(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    max_participants = activities[activity_name]["max_participants"]
    current_count = len(activities[activity_name]["participants"])

    for index in range(max_participants - current_count):
        activities[activity_name]["participants"].append(f"filled{index}@mergington.edu")

    overflow_email = "overflow.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": overflow_email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Activity is full"
    assert overflow_email not in activities[activity_name]["participants"]
