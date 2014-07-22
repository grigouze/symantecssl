import os.path

import pytest

from symantecssl import Symantec


def pytest_collection_modifyitems(items):
    for item in items:
        module_path = os.path.relpath(
            item.module.__file__,
            os.path.commonprefix([__file__, item.module.__file__]),
        )

        if module_path.startswith("functional/"):
            item.add_marker(pytest.mark.functional)
        elif module_path.startswith("unit/"):
            item.add_marker(pytest.mark.unit)
        else:
            raise RuntimeError(
                "Unknown test type (filename = {0})".format(module_path)
            )


@pytest.fixture
def symantec():
    username = os.environ.get("SYMANTEC_USER")
    password = os.environ.get("SYMANTEC_PASSWORD")
    partner_code = os.environ.get("SYMANTEC_PARTNER_CODE")

    api_url = os.environ.get(
        "SYMANTEC_API_URL",
        "https://test-api.geotrust.com/webtrust/partner",
    )

    if not (username and password and partner_code):
        pytest.skip(
            "Cannot access Symantec API without username, password, and "
            "partner code"
        )

    api = Symantec(username, password, url=api_url)
    api.partner_code = partner_code

    return api
