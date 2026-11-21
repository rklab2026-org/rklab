import pytest
from playwright.sync_api import Page, expect

# Live Webpage URL
BASE_URL = "https://rklab2026-org.github.io/rklab/"

def test_homepage_title(page: Page):
    """Test 1: Check if page title is correct"""
    page.goto(BASE_URL)
    expect(page).to_have_title("RKLab - Home")

def test_explore_button_and_alert(page: Page):
    """Test 2: Click Explore button and verify JS Alert popup text"""
    page.goto(BASE_URL)

    # Setup alert dialog handler
    alert_message = []
    
    def handle_dialog(dialog):
        alert_message.append(dialog.message)
        dialog.accept()

    page.on("dialog", handle_dialog)

    # Click the explore button
    explore_btn = page.locator("#explore-btn")
    expect(explore_btn).to_be_visible()
    explore_btn.click()

    # Validate if alert popped up with correct text
    assert len(alert_message) == 1
    assert "Welcome to RKLab!" in alert_message[0]