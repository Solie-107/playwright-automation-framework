from flows.account_flow import AccountFlow
from utils.data_factory import UserData


def test_full_account_flow(page, api_client, user_data: UserData):
    flow = AccountFlow(page, api_client)

    flow.create_user_via_ui(user_data)

    flow.logout()
    flow.login_via_ui(user_data)

    flow.verify_user_via_api(user_data)
    flow.get_user_details_via_api(user_data)

    flow.delete_user_via_api(user_data)