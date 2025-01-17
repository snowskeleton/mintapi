from typing import Dict, List, Optional, Union

from mintapi.browser import SeleniumBrowser
from mintapi.rest import RESTClient


class Mint(object):
    """
    Composed API client to route through the browser or REST calls
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        cookies: Optional[Union[str, List[Dict]]] = None,
        **browser_params
    ):
        """
        Passes forward parameters to the browser and rest client

        Pass a driver or email + password to authenticate with the browser
        OR pass in an api_key or cookie to auth directly with the rest client

        Browser is mainly used to generate auth (only necessary if not otherwise passed)
        """
        self.rest_client = RESTClient(api_key=api_key, cookies=cookies)

        # only use browser if not sufficiently authorized already
        if not api_key or not cookies:
            self.browser = SeleniumBrowser(**browser_params)

            if self.browser.driver is not None:
                self.transfer_auth()
            self.browser.close()

    def transfer_auth(self):
        api_key = self.browser._get_api_key_header()["authorization"]
        cookies = self.browser._get_cookies()
        self.rest_client.authorize(cookies=cookies, api_key=api_key)

    def __getattr__(self, attr):
        """
        Automatically handle routing to prefer the rest client but fallback to the browser for uinimplemented
        methods
        """
        if hasattr(self.rest_client, attr):
            return getattr(self.rest_client, attr)
        elif hasattr(self.browser, attr):
            return getattr(self.browser, attr)
        else:
            raise NotImplementedError


def get_accounts(email, password):
    mint = Mint(email, password)
    return mint.get_account_data()


def get_net_worth(email, password):
    mint = Mint(email, password)
    return mint.get_net_worth_data()


def get_budgets(email, password):
    mint = Mint(email, password)
    return mint.get_budget_data()


def get_credit_score(email, password):
    mint = Mint(email, password)
    return mint.get_credit_score()


def get_credit_report(email, password):
    mint = Mint(email, password)
    return mint.get_credit_report()


def initiate_account_refresh(email, password):
    mint = Mint(email, password)
    return mint.initiate_account_refresh()
