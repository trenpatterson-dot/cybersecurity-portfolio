"""Amazon Creators API signed request helpers.

This module implements a small SigV4-style signing flow plus a JSON HTTP
client so the rest of the application can request product data without
mixing request signing, transport, and product normalization together.

Important note:
- The public Amazon documentation currently points affiliates toward the
  Creators API, but the exact request shape is still evolving.
- To keep this implementation practical, the endpoint path, service name,
  and request target are configurable through environment variables.
- The signing flow is real and the HTTP request is real, while some
  default body fields are conservative compatibility guesses based on the
  legacy Product Advertising API request model.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.models import Product


class CreatorsApiClientError(Exception):
    """Raised when the signed Creators API request fails."""


@dataclass(slots=True)
class SignedRequestComponents:
    """Data produced while building a signed request."""

    amz_date: str
    date_stamp: str
    payload_text: str
    payload_hash: str
    canonical_headers: str
    signed_headers: str
    authorization_header: str


@dataclass(slots=True)
class CreatorsApiClientConfig:
    """Configuration values required for the signed client."""

    public_key: str
    private_key: str
    host: str
    region: str
    marketplace: str
    partner_tag: str
    service: str = "execute-api"
    path: str = "/creators-api/products"
    method: str = "POST"
    target: str | None = None
    timeout_seconds: int = 20


class CreatorsApiClient:
    """Minimal signed JSON client for Amazon affiliate product lookups."""

    def __init__(self, config: CreatorsApiClientConfig) -> None:
        self._config = config

    def get_items(self, item_ids: list[str]) -> list[Product]:
        """Fetch products by item identifiers and normalize the response."""

        normalized_item_ids = [item_id.strip() for item_id in item_ids if item_id.strip()]
        if not normalized_item_ids:
            raise CreatorsApiClientError(
                "Creators API requires at least one item id. Set CREATORS_API_ITEM_IDS in the environment."
            )

        payload = self._build_default_payload(normalized_item_ids)
        response = self._send_json_request(payload)
        return self._parse_products(response)

    def _build_default_payload(self, item_ids: list[str]) -> dict[str, object]:
        """Build a conservative default request body.

        The field names below intentionally mirror the older affiliate API
        style because Amazon's public transition guidance still references
        that model. These values are configurable at the endpoint level if
        your Creators API account expects a different route or wrapper.
        """

        return {
            "ItemIds": item_ids,
            "Marketplace": self._config.marketplace,
            "PartnerTag": self._config.partner_tag,
            "PartnerType": "Associates",
            "Resources": [
                "ItemInfo.Title",
                "ItemInfo.ByLineInfo",
                "Images.Primary.Large",
                "Offers.Listings.Price",
            ],
        }

    def _send_json_request(self, payload: dict[str, object]) -> dict[str, object]:
        signed = build_signed_request_components(
            access_key=self._config.public_key,
            secret_key=self._config.private_key,
            region=self._config.region,
            service=self._config.service,
            host=self._config.host,
            method=self._config.method,
            path=self._config.path,
            payload=payload,
        )

        headers = {
            "host": self._config.host,
            "content-type": "application/json; charset=utf-8",
            "x-amz-date": signed.amz_date,
            "x-amz-content-sha256": signed.payload_hash,
            "Authorization": signed.authorization_header,
        }

        if self._config.target:
            headers["x-amz-target"] = self._config.target

        url = f"https://{self._config.host}{self._config.path}"
        request = Request(
            url=url,
            data=signed.payload_text.encode("utf-8"),
            headers=headers,
            method=self._config.method,
        )

        try:
            with urlopen(request, timeout=self._config.timeout_seconds) as response:
                response_text = response.read().decode("utf-8")
        except HTTPError as error:
            response_text = error.read().decode("utf-8", errors="ignore")
            raise CreatorsApiClientError(
                f"Creators API returned HTTP {error.code}: {response_text or error.reason}"
            ) from error
        except URLError as error:
            raise CreatorsApiClientError(f"Creators API request failed: {error.reason}") from error

        try:
            parsed = json.loads(response_text)
        except json.JSONDecodeError as error:
            raise CreatorsApiClientError("Creators API returned invalid JSON.") from error

        if not isinstance(parsed, dict):
            raise CreatorsApiClientError("Creators API returned an unexpected response shape.")

        return parsed

    def _parse_products(self, payload: dict[str, object]) -> list[Product]:
        items = _extract_items(payload)
        products: list[Product] = []

        for item in items:
            normalized = _normalize_item(item)
            if normalized is not None:
                products.append(normalized)

        if not products:
            raise CreatorsApiClientError(
                "Creators API returned no usable product records. Check your endpoint path, target, and response format."
            )

        return products


def build_signed_request_components(
    access_key: str,
    secret_key: str,
    region: str,
    service: str,
    host: str,
    method: str,
    path: str,
    payload: dict[str, object],
    now_utc: datetime | None = None,
) -> SignedRequestComponents:
    """Return the core pieces of a SigV4-signed JSON request."""

    request_time = now_utc or datetime.now(UTC)
    amz_date = request_time.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = request_time.strftime("%Y%m%d")
    normalized_path = path if path.startswith("/") else f"/{path}"
    payload_text = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    payload_hash = hashlib.sha256(payload_text.encode("utf-8")).hexdigest()

    canonical_headers = (
        f"content-type:application/json; charset=utf-8\n"
        f"host:{host}\n"
        f"x-amz-content-sha256:{payload_hash}\n"
        f"x-amz-date:{amz_date}\n"
    )
    signed_headers = "content-type;host;x-amz-content-sha256;x-amz-date"
    canonical_request = (
        f"{method.upper()}\n"
        f"{normalized_path}\n"
        "\n"
        f"{canonical_headers}\n"
        f"{signed_headers}\n"
        f"{payload_hash}"
    )
    canonical_request_hash = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = (
        "AWS4-HMAC-SHA256\n"
        f"{amz_date}\n"
        f"{credential_scope}\n"
        f"{canonical_request_hash}"
    )
    signing_key = _derive_signing_key(secret_key, date_stamp, region, service)
    signature = hmac.new(
        signing_key,
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    authorization_header = (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    return SignedRequestComponents(
        amz_date=amz_date,
        date_stamp=date_stamp,
        payload_text=payload_text,
        payload_hash=payload_hash,
        canonical_headers=canonical_headers,
        signed_headers=signed_headers,
        authorization_header=authorization_header,
    )


def _derive_signing_key(secret_key: str, date_stamp: str, region: str, service: str) -> bytes:
    key_date = _sign(f"AWS4{secret_key}".encode("utf-8"), date_stamp)
    key_region = _sign(key_date, region)
    key_service = _sign(key_region, service)
    return _sign(key_service, "aws4_request")


def _sign(key: bytes, message: str) -> bytes:
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()


def _extract_items(payload: dict[str, object]) -> list[dict[str, object]]:
    candidates = [
        payload.get("ItemsResult"),
        payload.get("itemsResult"),
        payload.get("Items"),
        payload.get("items"),
        payload.get("data"),
    ]

    for candidate in candidates:
        if isinstance(candidate, dict):
            nested_items = candidate.get("Items") or candidate.get("items")
            if isinstance(nested_items, list):
                return [item for item in nested_items if isinstance(item, dict)]
        if isinstance(candidate, list):
            return [item for item in candidate if isinstance(item, dict)]

    return []


def _normalize_item(item: dict[str, object]) -> Product | None:
    asin = _first_non_empty_string(
        item.get("ASIN"),
        item.get("asin"),
        item.get("id"),
    )
    if not asin:
        return None

    title = _first_non_empty_string(
        _nested(item, "ItemInfo", "Title", "DisplayValue"),
        _nested(item, "itemInfo", "title", "displayValue"),
        item.get("title"),
        item.get("Title"),
    )
    if not title:
        return None

    product_url = _first_non_empty_string(
        item.get("DetailPageURL"),
        item.get("detailPageURL"),
        item.get("detail_page_url"),
        item.get("url"),
    )
    if not product_url:
        return None

    image_url = _first_non_empty_string(
        _nested(item, "Images", "Primary", "Large", "URL"),
        _nested(item, "images", "primary", "large", "url"),
        _nested(item, "image", "url"),
        item.get("imageUrl"),
    ) or ""

    category = _first_non_empty_string(
        _nested(item, "BrowseNodeInfo", "BrowseNodes", 0, "DisplayName"),
        _nested(item, "browseNodeInfo", "browseNodes", 0, "displayName"),
        item.get("category"),
    ) or "unknown"

    amount_text = _first_non_empty_string(
        _nested(item, "Offers", "Listings", 0, "Price", "Amount"),
        _nested(item, "offers", "listings", 0, "price", "amount"),
        item.get("price"),
    )
    amount = _to_decimal_or_none(amount_text)
    if amount is None:
        return None

    currency = _first_non_empty_string(
        _nested(item, "Offers", "Listings", 0, "Price", "Currency"),
        _nested(item, "offers", "listings", 0, "price", "currency"),
        item.get("currency"),
    ) or "USD"

    return Product(
        product_id=asin,
        asin=asin,
        title=title,
        category=category.lower(),
        source_price=amount,
        source_currency=currency,
        product_url=product_url,
        image_url=image_url,
        source_name="creators_api",
        source_timestamp_utc=datetime.now(UTC).isoformat(),
    )


def _nested(value: object, *keys: object) -> object | None:
    current: object | None = value
    for key in keys:
        if isinstance(key, int):
            if not isinstance(current, list) or len(current) <= key:
                return None
            current = current[key]
            continue

        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _first_non_empty_string(*values: object) -> str | None:
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return None


def _to_decimal_or_none(value: object) -> Decimal | None:
    if value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
