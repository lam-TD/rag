import pytest
import schemathesis


@pytest.fixture
def api_schema():
    return schemathesis.openapi.from_url("http://localhost:8000/openapi.json")


@schemathesis.hook.apply_to(path="/api/v1/collections", method="POST")
def before_call(_, case: schemathesis.Case, **__):
    if isinstance(case.body, dict):
        case.body["name"] = "fake_model"

    return None


# Create lazy schema from fixture
schema = schemathesis.pytest.from_fixture("api_schema")


# Use with parametrize to generate tests
@schema.parametrize()
def test_api(case):

    case.call_and_validate()
