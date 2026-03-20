"""E2E tests for photos."""

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect

from photoblog.photos.tests.factories import PhotoFactory

pytestmark = [pytest.mark.e2e, pytest.mark.django_db(transaction=True)]


def _dismiss_cookie_banner(page: Page) -> None:
    banner = page.get_by_role("region", name="Cookie consent")
    if banner.is_visible():
        page.get_by_role("button", name="Accept cookies and close banner").click()
        expect(banner).to_be_hidden()


def test_comment_form_hidden_by_default(auth_page: Page, e2e_user, live_server):
    photo = PhotoFactory(user=e2e_user)
    auth_page.goto(
        f"{live_server.url}{reverse('photos:photo_detail', args=[photo.pk])}"
    )
    _dismiss_cookie_banner(auth_page)
    expect(auth_page.get_by_role("button", name="Add comment")).to_be_visible()
    expect(auth_page.get_by_role("button", name="Submit")).to_be_hidden()
    expect(auth_page.get_by_role("button", name="Cancel")).to_be_hidden()


def test_comment_form_shows_on_add_comment_click(
    auth_page: Page, e2e_user, live_server
):
    photo = PhotoFactory(user=e2e_user)
    auth_page.goto(
        f"{live_server.url}{reverse('photos:photo_detail', args=[photo.pk])}"
    )
    _dismiss_cookie_banner(auth_page)
    auth_page.get_by_role("button", name="Add comment").click()
    expect(auth_page.get_by_role("button", name="Add comment")).to_be_hidden()
    expect(auth_page.locator('[name="comment"]')).to_be_visible()
    expect(auth_page.get_by_role("button", name="Submit")).to_be_visible()
    expect(auth_page.get_by_role("button", name="Cancel")).to_be_visible()


def test_cancel_hides_form_and_restores_add_button(
    auth_page: Page, e2e_user, live_server
):
    photo = PhotoFactory(user=e2e_user)
    auth_page.goto(
        f"{live_server.url}{reverse('photos:photo_detail', args=[photo.pk])}"
    )
    _dismiss_cookie_banner(auth_page)
    auth_page.get_by_role("button", name="Add comment").click()
    auth_page.get_by_role("button", name="Cancel").click()
    expect(auth_page.get_by_role("button", name="Add comment")).to_be_visible()
    expect(auth_page.get_by_role("button", name="Submit")).to_be_hidden()
    expect(auth_page.get_by_role("button", name="Cancel")).to_be_hidden()
