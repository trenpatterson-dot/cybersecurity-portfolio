"""Tests for the mock product source and helpers."""

from __future__ import annotations

from decimal import Decimal

from app.config import load_settings
from app.product_source import (
    CreatorsApiProductSourceProvider,
    MockProductSourceProvider,
    filter_products_by_price,
    get_all_products,
    get_products_by_category,
    resolve_provider,
)


def test_mock_provider_loads_products():
    """Proves the default mock provider returns local development products."""

    products = get_all_products()

    assert len(products) >= 4
    assert products[0].product_id.startswith("mock-")


def test_get_products_by_category_filters_case_insensitively():
    """Proves category filtering works even if input casing differs."""

    products = get_products_by_category("ELECTRONICS", provider=MockProductSourceProvider())

    assert products
    assert all(product.category == "electronics" for product in products)


def test_filter_products_by_price_returns_matching_range():
    """Proves price filtering keeps only products inside the requested range."""

    products = get_all_products(provider=MockProductSourceProvider())

    filtered = filter_products_by_price(products, min_price=40, max_price=90)

    assert filtered
    assert all(Decimal("40") <= product.source_price <= Decimal("90") for product in filtered)


def test_resolve_provider_uses_mock_by_default(monkeypatch):
    """Proves the workflow defaults to the local mock provider safely."""

    monkeypatch.setenv("AMAZON_ASSOCIATE_TAG", "yourtag-20")
    settings = load_settings()

    selection = resolve_provider(settings)

    assert selection.provider_name == "mock"
    assert selection.fallback_reason is None
    assert isinstance(selection.provider, MockProductSourceProvider)


def test_resolve_provider_falls_back_to_mock_when_creators_api_is_incomplete(monkeypatch):
    """Proves incomplete real-provider config falls back without breaking the app."""

    monkeypatch.setenv("AMAZON_ASSOCIATE_TAG", "yourtag-20")
    monkeypatch.setenv("PRODUCT_SOURCE_PROVIDER", "creators_api")
    settings = load_settings()

    selection = resolve_provider(settings)

    assert selection.provider_name == "mock"
    assert "Creators API provider is selected but missing configuration" in (selection.fallback_reason or "")
    assert isinstance(selection.provider, MockProductSourceProvider)


def test_creators_api_provider_accepts_complete_configuration(monkeypatch):
    """Proves the real-provider scaffold can be constructed from complete settings."""

    monkeypatch.setenv("AMAZON_ASSOCIATE_TAG", "yourtag-20")
    monkeypatch.setenv("PRODUCT_SOURCE_PROVIDER", "creators_api")
    monkeypatch.setenv("CREATORS_API_PUBLIC_KEY", "public-key")
    monkeypatch.setenv("CREATORS_API_PRIVATE_KEY", "private-key")
    monkeypatch.setenv("CREATORS_API_HOST", "api.example.test")
    monkeypatch.setenv("CREATORS_API_REGION", "us-east-1")
    monkeypatch.setenv("CREATORS_API_MARKETPLACE", "amazon.com")
    monkeypatch.setenv("CREATORS_API_ITEM_IDS", "B012345678,B012345679")
    settings = load_settings()

    selection = resolve_provider(settings)

    assert selection.provider_name == "creators_api"
    assert selection.fallback_reason is None
    assert isinstance(selection.provider, CreatorsApiProductSourceProvider)


def test_creators_api_provider_fetches_products_with_signed_client(monkeypatch):
    """Proves the provider hands configured item ids to the signed client."""

    monkeypatch.setenv("AMAZON_ASSOCIATE_TAG", "yourtag-20")
    monkeypatch.setenv("PRODUCT_SOURCE_PROVIDER", "creators_api")
    monkeypatch.setenv("CREATORS_API_PUBLIC_KEY", "public-key")
    monkeypatch.setenv("CREATORS_API_PRIVATE_KEY", "private-key")
    monkeypatch.setenv("CREATORS_API_HOST", "api.example.test")
    monkeypatch.setenv("CREATORS_API_REGION", "us-east-1")
    monkeypatch.setenv("CREATORS_API_MARKETPLACE", "amazon.com")
    monkeypatch.setenv("CREATORS_API_ITEM_IDS", "B012345678")
    settings = load_settings()
    selection = resolve_provider(settings)

    captured_item_ids: list[str] = []

    def fake_get_items(self, item_ids):
        captured_item_ids.extend(item_ids)
        return [MockProductSourceProvider().get_all_products()[0]]

    monkeypatch.setattr("app.product_source.CreatorsApiClient.get_items", fake_get_items)

    products = selection.provider.get_all_products()

    assert captured_item_ids == ["B012345678"]
    assert len(products) == 1
