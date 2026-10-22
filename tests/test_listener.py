"""Offline callback contracts; no provider credentials or customer data."""
from collections import OrderedDict
from types import SimpleNamespace
import socket

import pytest
import requests

from paypal_IPN.listener import PayPalIPNListener, VerificationError


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def denied(*args, **kwargs):
        raise AssertionError("Tests must not contact PayPal")
    monkeypatch.setattr(socket.socket, "connect", denied)
    monkeypatch.setattr(socket.socket, "connect_ex", denied)


@pytest.mark.parametrize("mapping", [dict, OrderedDict])
@pytest.mark.parametrize("sandbox", [False, True])
def test_verified_callback_preserves_mapping_and_utf8_payload(monkeypatch, mapping, sandbox):
    original = mapping([("txn_id", "fixture-txn"), ("item_name", "Caf\u00e9"),
        ("mc_gross", "19.99"), ("mc_currency", "USD"), ("raw", b"unchanged")])
    calls = []
    def post(url, data):
        calls.append((url, data))
        return SimpleNamespace(content=b"VERIFIED")
    monkeypatch.setattr("paypal_IPN.listener.requests.post", post)
    listener = PayPalIPNListener(sandbox=sandbox)
    result = listener.process_request(original)
    assert result == original
    assert len(calls) == 1
    assert calls[0][0] == (listener.SANDBOX_URL if sandbox else listener.PAYPAL_URL)
    payload = calls[0][1]
    assert list(payload)[0] == "cmd"
    assert payload["cmd"] == "_notify-validate"
    assert payload["item_name"] == "Caf\u00e9".encode("utf-8")
    assert payload["raw"] == b"unchanged"
    assert "cmd" not in original


@pytest.mark.parametrize("reply", [b"INVALID", b"VERIFIED\n", b"", b"unexpected"])
def test_unverified_callback_is_rejected(monkeypatch, reply):
    monkeypatch.setattr("paypal_IPN.listener.requests.post", lambda *a, **k: SimpleNamespace(content=reply))
    with pytest.raises(VerificationError):
        PayPalIPNListener().process_request(OrderedDict(txn_id="fixture-txn"))


def test_decode_flattens_only_single_item_lists_without_mutating_input():
    original = OrderedDict(single=["one"], multiple=["one", "two"], empty=[], scalar="value")
    result = PayPalIPNListener().decode_request(original)
    assert result == OrderedDict(single="one", multiple=["one", "two"], empty=[], scalar="value")
    assert original["single"] == ["one"]


def test_transport_failure_propagates_without_acknowledging_callback(monkeypatch):
    def failed(*args, **kwargs):
        raise requests.ConnectionError("Synthetic verification connection failure")
    monkeypatch.setattr("paypal_IPN.listener.requests.post", failed)
    with pytest.raises(requests.ConnectionError):
        PayPalIPNListener().process_request(OrderedDict(txn_id="fixture-txn"))
