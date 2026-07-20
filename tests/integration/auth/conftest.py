import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "auth:marks tests as authentication tests")

def pytest_collection_modifyitems(config,items):
    for item in items:
        if "auth" in str(item.fspath):
            item.add_marker(pytest.mark.auth)

