import os.path

try:
    from urllib.parse import quote_plus, parse_qs
except ImportError:
    from urllib import quote_plus
    from urlparse import parse_qs

import betamax
import pytest

from betamax.cassette.util import deserialize_prepared_request

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


def get_placeholders():
    username = os.environ.get("SYMANTEC_USER", "X" * 30)
    password = os.environ.get("SYMANTEC_PASSWORD", "X" * 30)
    partner_code = os.environ.get("SYMANTEC_PARTNER_CODE", "X" * 30)

    return [
        {"placeholder": "<<SYMANTEC_USER>>", "replace": username},
        {"placeholder": "<<SYMANTEC_PASSWORD>>", "replace": password},
        {
            "placeholder": "<<SYMANTEC_PASSWORD_QUOTED>>",
            "replace": quote_plus(password),
        },
        {"placeholder": "<<SYMANTEC_PARTNER>>", "replace": partner_code},
    ]


class FormEncodeMatcher(betamax.BaseMatcher):

    name = "form-body"
    content_type = "application/x-www-form-urlencoded"

    def match(self, request, recorded_request):
        recorded = deserialize_prepared_request(recorded_request)

        if (request.headers.get("Content-Type") != self.content_type
                or recorded.headers.get("Content-Type") != self.content_type):
            return False

        body = parse_qs(request.body) if request.body else None
        recorded_body = parse_qs(recorded.body) if recorded.body else None

        return body == recorded_body

betamax.Betamax.register_request_matcher(FormEncodeMatcher)


@pytest.fixture(scope="session")
def _betamax_configure():
    username = os.environ.get("SYMANTEC_USER")
    password = os.environ.get("SYMANTEC_PASSWORD")
    partner_code = os.environ.get("SYMANTEC_PARTNER_CODE")

    config = betamax.Betamax.configure()
    config.cassette_library_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "cassettes",
    )
    config.default_cassette_options["record_mode"] = (
        "none" if not (username and password and partner_code) else "all"
    )
    config.default_cassette_options["match_requests_on"] = [
        "form-body",
        "method",
        "uri",
    ]

    for placeholder in get_placeholders():
        config.define_cassette_placeholder(
            placeholder["placeholder"],
            placeholder["replace"],
        )


class VCR(object):

    def __init__(self, cassette_name, default_placeholders=None):
        self.betamax = None
        self.__cassette = cassette_name
        self.__placeholders = (
            default_placeholders if default_placeholders is not None else []
        )

    def __getattr__(self, name):
        return getattr(self.betamax, name)

    def use_cassette(self, **kwargs):
        placeholders = kwargs.pop("placeholders", [])
        placeholders = self.__placeholders + placeholders
        kwargs["placeholders"] = placeholders
        return self.betamax.use_cassette(self.__cassette, **kwargs)


class NoVCR(object):

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def use_cassette(self, **kwargs):
        return self


@pytest.fixture
def vcr(request, _betamax_configure):
    if "SYMANTEC_NO_BETAMAX" in os.environ:
        return NoVCR()
    else:
        return VCR(
            request.node.name,
            default_placeholders=get_placeholders(),
        )


@pytest.fixture
def symantec(request, vcr):
    username = os.environ.get("SYMANTEC_USER")
    password = os.environ.get("SYMANTEC_PASSWORD")
    partner_code = os.environ.get("SYMANTEC_PARTNER_CODE")

    api_url = os.environ.get(
        "SYMANTEC_API_URL",
        "https://test-api.geotrust.com/webtrust/partner",
    )

    if not (username and password and partner_code):
        username, password, partner_code = ["X" * 30] * 3

    api = Symantec(username, password, url=api_url)
    api.partner_code = partner_code

    vcr.betamax = betamax.Betamax(api.session)

    return api
