import pytest


@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def order(first_entry):
    return []


@pytest.fixture(autouse=True)
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(order, first_entry):
    assert order == [first_entry]


def test_string_and_int(order, first_entry):
    order.append(2)
    assert order == [first_entry, 2]


@pytest.mark.parametrize(
    "method,url,payload,expected_status",
    [
        ("POST", "/users", {"name": "A"}, 201),
        ("POST", "/users", {"name": ""}, 422),
        ("POST", "/users", {}, 422),
    ],
    ids=["ok", "name_empty", "missing_body"],
)
def test_create_user_cases(client, method, url, payload, expected_status):
    resp = client.request(method, url, json=payload)
    assert resp.status_code == expected_status
