"""Tests for the signed Creators API client helpers."""

from __future__ import annotations

from datetime import UTC, datetime

from app.creators_api import build_signed_request_components


def test_build_signed_request_components_returns_sigv4_headers():
    """Proves the signing helper returns a stable SigV4-shaped authorization header."""

    signed = build_signed_request_components(
        access_key="PUBLICKEY123",
        secret_key="PRIVATEKEY456",
        region="us-east-1",
        service="execute-api",
        host="example.execute-api.us-east-1.amazonaws.com",
        method="POST",
        path="/creators-api/products",
        payload={"ItemIds": ["B012345678"]},
        now_utc=datetime(2026, 4, 9, 22, 0, 0, tzinfo=UTC),
    )

    assert signed.amz_date == "20260409T220000Z"
    assert signed.date_stamp == "20260409"
    assert signed.signed_headers == "content-type;host;x-amz-content-sha256;x-amz-date"
    assert "Credential=PUBLICKEY123/20260409/us-east-1/execute-api/aws4_request" in signed.authorization_header
    assert "SignedHeaders=content-type;host;x-amz-content-sha256;x-amz-date" in signed.authorization_header
    assert "Signature=" in signed.authorization_header
