from __future__ import annotations
import logging
from admitted._base import BasePage
from admitted._executables._manager import ChromeManager
from admitted._url import match_url

logger = logging.getLogger(__name__)


class Site(BasePage):
    """Represents a particular web site and one ChromeDriver instance."""

    _chrome_manager_class = ChromeManager

    def __init__(
        self,
        login_url: str,
        credentials: dict[str, str],
        *,
        timeout: int = 30,
        debug: bool = False,
        reuse_service: bool = False,
        **login_options,
    ):
        """Initialize ChromeDriver and Site instance attributes.

        Args:
          login_url: This site's login page. This should be the URL of the page with the first login input,
            indicating it is okay to begin the login process.
          credentials: Dictionary defining credential values required by _do_login.
          timeout: Default timeout in seconds for wait operations.
          debug: If True, will output chromedriver.log on the desktop and suppress retries.
          reuse_service: If True and an instance of chromedriver is running, we will attach to existing process.
          login_options: Additional options for the login method. See login method for details.
        """
        super().__init__(self._chrome_manager_class(timeout=timeout, debug=debug, reuse_service=reuse_service))
        self.login_url = login_url
        self.credentials = credentials
        self._login_opts = login_options
        self._init_login()
        if login_options.get("postpone") is not True:
            self.login()

    def _init_login(self):
        """Define the login page object.

        Example:
          self.username_selector = "#username"
          self.password_selector = "#password"
          self.submit_selector = "#login-button"
        """
        raise NotImplementedError

    def _do_login(self) -> "Site":
        """Authenticate to the site.

        Example:
          self.css(self.username_selector).clear().send_keys(self.credentials['username'])
          self.css(self.password_selector).clear().send_keys(self.credentials['password'])
          self.css(self.submit_selector).click()
          return self
        """
        raise NotImplementedError

    def login(self) -> "Site":
        """Navigate to login page and authenticate to the site, unless already logged in.

        These __init__ keyword arguments impact login behavior:
          postpone: If True, login will not be called on instantiation.
          start_url: Begin login by navigating to this URL, if different from `login_url`.
          abort_url: Return without logging in if landed on this url.
          path_substr: If True, the login_url path being anywhere in the current_url path is considered a match.
          strict_query: If True, the URL query must match. Default is to ignore it.
        """
        # no need to log in when already authenticated
        if self.is_authenticated():
            return self
        # if we are already on the login page, no need to navigate
        match_kwargs = {
            "path_substr": self._login_opts.get("path_substr", False),
            "ignore_query": not self._login_opts.get("strict_query", False),
        }
        abort_url = self._login_opts.get("abort_url")
        if not match_url(self.current_url, self.login_url, **match_kwargs):
            if "start_url" in self._login_opts:
                url = self._login_opts["start_url"]
                enforce_url = self.login_url
            else:
                url = self.login_url
                enforce_url = True
            self._navigate(url=url, enforce_url=enforce_url, abort_url=abort_url, **match_kwargs)
        if abort_url and match_url(self.current_url, abort_url, **match_kwargs):
            return self
        return self._do_login()

    def is_authenticated(self) -> bool:
        """Check if authentication is current.

        Example:
          return self.window["localStorage.accessToken"] is not None
        """
        raise NotImplementedError
