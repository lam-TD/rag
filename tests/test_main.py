import pytest
import schemathesis


@pytest.fixture
def api_schema():
    return schemathesis.openapi.from_url("http://localhost:8000/openapi.json")


# Create lazy schema from fixture
schema = schemathesis.pytest.from_fixture("api_schema")


# Use with parametrize to generate tests
@schema.parametrize()
def test_api(case):
    case.call_and_validate()
