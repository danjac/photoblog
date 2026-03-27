"""Top-level E2E tests."""

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


def _open_user_dropdown(auth_page: Page, e2e_user) -> None:
    auth_page.get_by_role("button", name=e2e_user.username).click()
    expect(auth_page.get_by_role("menu")).to_be_visible()


def test_user_dropdown_opens_and_shows_menu_items(
    auth_page: Page, e2e_user, live_server
):
    """User dropdown opens and shows Account settings and Sign out."""
    auth_page.goto(f"{live_server.url}{reverse('index')}")

    auth_page.get_by_role("button", name=e2e_user.username).click()

    menu = auth_page.get_by_role("menu")
    expect(menu).to_be_visible()
    expect(menu.get_by_role("link", name="Account settings")).to_be_visible()
    expect(menu.locator('[data-testid="logout-button"]')).to_be_visible()


def test_user_dropdown_closes_on_outside_click(auth_page: Page, e2e_user, live_server):
    """Clicking outside the dropdown closes it."""
    auth_page.goto(f"{live_server.url}{reverse('index')}")
    _open_user_dropdown(auth_page, e2e_user)

    # Click somewhere outside the dropdown
    auth_page.locator("main").click()

    expect(auth_page.get_by_role("menu")).not_to_be_visible()


def test_user_dropdown_closes_on_escape(auth_page: Page, e2e_user, live_server):
    """Pressing Escape closes the dropdown."""
    auth_page.goto(f"{live_server.url}{reverse('index')}")
    _open_user_dropdown(auth_page, e2e_user)

    auth_page.keyboard.press("Escape")

    expect(auth_page.get_by_role("menu")).not_to_be_visible()


def test_language_switcher_changes_language(page: Page, live_server):
    """Switching to French via the language dropdown activates the French locale."""
    page.goto(f"{live_server.url}{reverse('index')}")

    # Open the language dropdown
    page.get_by_role("button", name="Select language").click()

    # Click Français in the menu
    page.get_by_role("button", name="Français").click()

    # After the POST + redirect, the navbar should show "FR" as the active language code
    expect(page.locator("header")).to_contain_text("FR")
