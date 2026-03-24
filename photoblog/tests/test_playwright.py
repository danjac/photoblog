"""Top-level E2E tests."""

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


def test_language_switcher_changes_language(page: Page, live_server):
    """Switching to French via the language dropdown activates the French locale."""
    page.goto(f"{live_server.url}{reverse('index')}")

    # Open the language dropdown
    page.get_by_role("button", name="Select language").click()

    # Click Français in the menu
    page.get_by_role("button", name="Français").click()

    # After the POST + redirect, the navbar should show "FR" as the active language code
    expect(page.locator("header")).to_contain_text("FR")
