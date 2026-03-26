import pytest
from utils.data_factory import UserData


def test_verify_login_with_valid_credentials(
    api_client,
    page,
    user_data: UserData,
) -> None:
    # Arrange - create user through UI first because API createAccount
    # does not reliably create a real UI-loginable user in this site.
    page.goto("https://automationexercise.com/login")

    page.locator("[data-qa='signup-name']").fill(user_data.name)
    page.locator("[data-qa='signup-email']").fill(user_data.email)
    page.locator("[data-qa='signup-button']").click()

    page.locator("#id_gender1").check()
    page.locator("[data-qa='password']").fill(user_data.password)
    page.locator("[data-qa='days']").select_option("1")
    page.locator("[data-qa='months']").select_option("1")
    page.locator("[data-qa='years']").select_option("2000")
    page.locator("[data-qa='first_name']").fill(user_data.first_name)
    page.locator("[data-qa='last_name']").fill(user_data.last_name)
    page.locator("[data-qa='company']").fill(user_data.company)
    page.locator("[data-qa='address']").fill(user_data.address1)
    page.locator("[data-qa='address2']").fill(user_data.address2)
    page.locator("[data-qa='country']").select_option(user_data.country)
    page.locator("[data-qa='state']").fill(user_data.state)
    page.locator("[data-qa='city']").fill(user_data.city)
    page.locator("[data-qa='zipcode']").fill(user_data.zipcode)
    page.locator("[data-qa='mobile_number']").fill(user_data.mobile_number)
    page.locator("[data-qa='create-account']").click()

    # Act
    response = api_client.verify_login(
        email=user_data.email,
        password=user_data.password,
    )

    # Assert
    assert response["status_code"] == 200
    assert str(response["body"].get("responseCode")) == "200"

    # Cleanup
    delete_response = api_client.delete_account(
        email=user_data.email,
        password=user_data.password,
    )
    assert delete_response["status_code"] == 200


def test_get_user_detail_by_email(
    api_client,
    page,
    user_data: UserData,
) -> None:
    # Arrange - create via UI
    page.goto("https://automationexercise.com/login")

    page.locator("[data-qa='signup-name']").fill(user_data.name)
    page.locator("[data-qa='signup-email']").fill(user_data.email)
    page.locator("[data-qa='signup-button']").click()

    page.locator("#id_gender1").check()
    page.locator("[data-qa='password']").fill(user_data.password)
    page.locator("[data-qa='days']").select_option("1")
    page.locator("[data-qa='months']").select_option("1")
    page.locator("[data-qa='years']").select_option("2000")
    page.locator("[data-qa='first_name']").fill(user_data.first_name)
    page.locator("[data-qa='last_name']").fill(user_data.last_name)
    page.locator("[data-qa='company']").fill(user_data.company)
    page.locator("[data-qa='address']").fill(user_data.address1)
    page.locator("[data-qa='address2']").fill(user_data.address2)
    page.locator("[data-qa='country']").select_option(user_data.country)
    page.locator("[data-qa='state']").fill(user_data.state)
    page.locator("[data-qa='city']").fill(user_data.city)
    page.locator("[data-qa='zipcode']").fill(user_data.zipcode)
    page.locator("[data-qa='mobile_number']").fill(user_data.mobile_number)
    page.locator("[data-qa='create-account']").click()

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
    delete_response = api_client.delete_account(
        email=user_data.email,
        password=user_data.password,
    )
    assert delete_response["status_code"] == 200


def test_verify_login_with_invalid_password(
    api_client,
    page,
    user_data: UserData,
) -> None:
    # Arrange - create via UI
    page.goto("https://automationexercise.com/login")

    page.locator("[data-qa='signup-name']").fill(user_data.name)
    page.locator("[data-qa='signup-email']").fill(user_data.email)
    page.locator("[data-qa='signup-button']").click()

    page.locator("#id_gender1").check()
    page.locator("[data-qa='password']").fill(user_data.password)
    page.locator("[data-qa='days']").select_option("1")
    page.locator("[data-qa='months']").select_option("1")
    page.locator("[data-qa='years']").select_option("2000")
    page.locator("[data-qa='first_name']").fill(user_data.first_name)
    page.locator("[data-qa='last_name']").fill(user_data.last_name)
    page.locator("[data-qa='company']").fill(user_data.company)
    page.locator("[data-qa='address']").fill(user_data.address1)
    page.locator("[data-qa='address2']").fill(user_data.address2)
    page.locator("[data-qa='country']").select_option(user_data.country)
    page.locator("[data-qa='state']").fill(user_data.state)
    page.locator("[data-qa='city']").fill(user_data.city)
    page.locator("[data-qa='zipcode']").fill(user_data.zipcode)
    page.locator("[data-qa='mobile_number']").fill(user_data.mobile_number)
    page.locator("[data-qa='create-account']").click()

    # Act
    response = api_client.verify_login(
        email=user_data.email,
        password="WrongPassword123",
    )

    # Assert
    assert response["status_code"] == 200
    assert str(response["body"].get("responseCode")) != "200"

    # Cleanup
    delete_response = api_client.delete_account(
        email=user_data.email,
        password=user_data.password,
    )
    assert delete_response["status_code"] == 200