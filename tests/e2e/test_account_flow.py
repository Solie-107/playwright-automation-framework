from flows.account_flow import AccountFlow
from utils.data_factory import UserData


def test_full_account_flow(page, api_client, user_data: UserData):
    
    print("\n=== Starting: Full Account Flow === ")
    flow = AccountFlow(page, api_client)

    print(f"\n=== Starting Create user via UI ===> {user_data.email}")
    flow.create_user_via_ui(user_data)

    print("\n=== Starting: Logout Existing User === ")
    flow.logout()

    print("\n=== Starting: Login with Existing User === ")
    flow.login_via_ui(user_data)

    print(f"\n=== Starting: Verify User via API ===")
    flow.verify_user_via_api(user_data)
    flow.get_user_details_via_api(user_data)

    print("\n=== Starting: Delete User via API === ")
    flow.delete_user_via_api(user_data)