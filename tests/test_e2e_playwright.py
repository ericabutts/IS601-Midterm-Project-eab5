import pytest

from playwright.sync_api import sync_playwright

@pytest.mark.e2e
def test_calculator_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5500")

        page.fill("#a","5")
        page.fill("#b","7")
        page.click("#add")

        page.wait_for_selector("#result")

        result = page.inner_text("#result")
        assert result == "12"
        browser.close()

        