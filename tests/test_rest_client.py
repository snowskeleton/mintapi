"""
Rest client tests

Focuses on client instantiation and request construction - not endpoint data
"""
import unittest

import pytest
from mintapi.rest import RESTClient


class RestAuthTests(unittest.TestCase):
    def test_header_updates(self):
        rest_client = RESTClient()
        self.assertIsNone(rest_client.session.headers.get("authorization"))
        self.assertIsNone(rest_client.session.headers.get("cookie"))
        api_key = "API KEY"
        cookie = "mint.authid=1234567890"

        rest_client.authorize(api_key=api_key, cookies=cookie)
        self.assertEqual(api_key, rest_client.session.headers.get(("authorization")))
        self.assertEqual(cookie, rest_client.session.headers.get(("cookie")))

    def test_header_updates_with_cookies_list(self):
        rest_client = RESTClient()
        self.assertIsNone(rest_client.session.headers.get("authorization"))
        self.assertIsNone(rest_client.session.headers.get("cookie"))
        api_key = "API KEY"
        cookies = [
            {
                "domain": ".intuit.com",
                "httpOnly": True,
                "name": "mint.authid",
                "path": "/",
                "sameSite": "None",
                "secure": True,
                "value": "1234567890",
            }
        ]
        rest_client.authorize(api_key=api_key, cookies=cookies)
        self.assertEqual(api_key, rest_client.session.headers.get(("authorization")))
        self.assertEqual(None, rest_client.session.headers.get(("cookie")))

    def test_cookie_updates(self):
        original_cookie = {
            "domain": ".intuit.com",
            "httpOnly": True,
            "name": "mint.authid",
            "path": "/",
            "sameSite": "None",
            "secure": True,
            "value": "1234567890",
        }
        rest_client = RESTClient(api_key="API Key", cookies=[original_cookie])

        updated_cookie = {
            "domain": ".intuit.com",
            "httpOnly": True,
            "name": "mint.authid",
            "path": "/",
            "sameSite": "None",
            "secure": True,
            "value": "0987654321",
        }

        rest_client.update_cookies(cookies=[updated_cookie])
        self.assertEqual(
            updated_cookie["value"], rest_client.session.cookies.get("mint.authid")
        )


class RestRequestHandlingTests(unittest.TestCase):
    def test_request_param_passing(self):
        pass

    def test_response_status_checking(self):
        pass

    def test_pagination_call(self):
        pass


class RestEndpointTests(unittest.TestCase):
    """
    E2E rest endpoint test with mock endpoint responses
    (endpoint logic tested separately)
    """


if __name__ == "__main__":
    pytest.main()
