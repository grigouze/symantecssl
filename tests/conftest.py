import os.path

import pytest


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
