from flows.account_flow import AccountFlow
from utils.data_factory import UserData


def test_verify_login_with_valid_credentials(
    api_client,
    page,
    user_data: UserData,
) -> None:
    flow = AccountFlow(page, api_client)

    # Arrange
    flow.create_user_via_ui(user_data)

    # Act
    response = api_client.verify_login(
        email=user_data.email,
        password=user_data.password,
    )

    # Assert
    assert response["status_code"] == 200
    assert str(response["body"].get("responseCode")) == "200"

    # Cleanup
    flow.delete_user_via_api(user_data)


def test_get_user_detail_by_email(
    api_client,
    page,
    user_data: UserData,
) -> None:
    flow = AccountFlow(page, api_client)

    # Arrange
    flow.create_user_via_ui(user_data)

    # Act
    response = api_client.get_user_detail_by_email(user_data.email)

    # Assert
    assert response["status_code"] == 200
    assert str(response["body"].get("responseCode")) == "200"

    if "user" in response["body"]:
        returned_user = response["body"]["user"]
        assert returned_user["email"] == user_data.email
        assert returned_user["first_name"] == user_data.first_name
        assert returned_user["last_name"] == user_data.last_name

    # Cleanup
    flow.delete_user_via_api(user_data)


def test_verify_login_with_invalid_password(
    api_client,
    page,
    user_data: UserData,
) -> None:
    flow = AccountFlow(page, api_client)

    # Arrange
    flow.create_user_via_ui(user_data)

    # Act
    response = api_client.verify_login(
        email=user_data.email,
        password="WrongPassword123",
    )

    # Assert
    assert response["status_code"] == 200
    assert str(response["body"].get("responseCode")) != "200"

    # Cleanup
    flow.delete_user_via_api(user_data)