import pytest
from playwright.sync_api import Playwright

# Local Backend API Base URL
BASE_URL = "http://127.0.0.1:8000"


def test_get_status_api(playwright: Playwright):
    """Test 1: Validate GET /api/status endpoint"""
    request_context = playwright.request.new_context(base_url=BASE_URL)
    response = request_context.get("/api/status")

    # Assertions
    assert response.status == 200
    json_data = response.json()
    assert json_data["status"] == "Healthy"
    assert json_data["lab_name"] == "RKLab Enterprise Lab"


def test_get_items_api(playwright: Playwright):
    """Test 2: Validate GET /api/items endpoint"""
    request_context = playwright.request.new_context(base_url=BASE_URL)
    response = request_context.get("/api/items")

    assert response.status == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 2  # At least 2 initial items exist


def test_create_item_api_positive(playwright: Playwright):
    """Test 3: Validate POST /api/items with valid payload (201)"""
    request_context = playwright.request.new_context(base_url=BASE_URL)

    payload = {
        "name": "Playwright API Automation",
        "status": "In Progress",
    }

    response = request_context.post("/api/items", data=payload)

    assert response.status == 201
    json_data = response.json()
    assert json_data["message"] == "Item created successfully!"
    assert json_data["data"]["name"] == "Playwright API Automation"


def test_create_item_api_negative_validation(playwright: Playwright):
    """Test 4: Validate POST /api/items with empty payload (422)"""
    request_context = playwright.request.new_context(base_url=BASE_URL)

    response = request_context.post("/api/items", data={})

    assert response.status == 422