from src.app import activities


def test_signup_accepts_empty_email_under_current_contract(client):
    # Arrange
    activity_name = "Chess Club"
    empty_email = ""

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": empty_email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {empty_email} for {activity_name}"
    assert empty_email in activities[activity_name]["participants"]


def test_signup_is_case_sensitive_for_activity_name(client):
    # Arrange
    activity_name_with_wrong_case = "chess club"
    email = "case.check@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name_with_wrong_case}/signup",
        params={"email": email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"
