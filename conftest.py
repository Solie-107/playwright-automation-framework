import os
import pytest
from playwright.sync_api import Playwright

from api.account_api import AccountApi
from utils.data_factory import UserData, build_user


# ---------- DATA ----------
@pytest.fixture
def user_data() -> UserData:
    return build_user()


# ---------- API ----------
@pytest.fixture
def api_client(playwright: Playwright) -> AccountApi:
    request_context = playwright.request.new_context(ignore_https_errors=True)
    client = AccountApi(request_context)
    yield client
    request_context.dispose()


# ---------- CONTEXT (video + trace) ----------
@pytest.fixture
def context(browser, request):
    os.makedirs("artifacts/videos", exist_ok=True)
    os.makedirs("artifacts/traces", exist_ok=True)

    context = browser.new_context(
        ignore_https_errors=True,
        record_video_dir="artifacts/videos/",
        record_video_size={"width": 1280, "height": 720},
    )

    # 👉 start trace
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # 👉 save trace
    test_name = request.node.name.replace("[", "_").replace("]", "_")
    context.tracing.stop(path=f"artifacts/traces/{test_name}.zip")

    context.close()


# ---------- PAGE + SCREENSHOT ON FAIL ----------
@pytest.fixture
def page(context, request):
    os.makedirs("artifacts/screenshots", exist_ok=True)

    page = context.new_page()
    yield page

    # 👉 screenshot only if test failed
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name.replace("[", "_").replace("]", "_")
        page.screenshot(
            path=f"artifacts/screenshots/{test_name}.png",
            full_page=True
        )

    page.close()


# ---------- HOOK (needed for screenshot) ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)