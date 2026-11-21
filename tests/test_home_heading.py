from playwright.sync_api import Page, expect


def test_home_heading(page: Page):
    page.goto("https://rklab2026-org.github.io/rklab/")

    heading = page.get_by_role("heading", level=1)

    expect(heading).to_have_text("Welcome to RKLab!")