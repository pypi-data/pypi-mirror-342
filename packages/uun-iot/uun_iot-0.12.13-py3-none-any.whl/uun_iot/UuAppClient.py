"""Communication with the .Main uuSubApp."""

import datetime
import json
import logging
import time
import typing as t
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests_toolbelt.utils import user_agent as ua

import uun_iot

from .exceptions import TokenCommandError, TokenError, UuAppClientException

logger = logging.getLogger(__name__)


class UuAppClient:
    """Library functions for communication and authentication with uuApp.

    The class gets a dictionary ``config`` containing the configuration of the application.
    The (root) keys and subkeys of interest to this class are

        - ``uuApp``: information about server uuApp

            - ``gateway``: domain gateway of the corresponding uuApp
            - ``uuAppName``: full name of the uuApp
            - ``awid``
            - ``uuCmdList``: containing uuCmd endpoint. The keys are not used
              by :class:`UuAppClient` class - they are used by the application
              user modules (most commonly specified in Python package path
              ``<package_name>/modules/__init__.py``.

        - ``uuThing``: authentication information about the IoT gateway

            - ``uuIdentity``
            - ``accessCode1``
            - ``accessCode2``

        - ``oidcGrantToken``: information about the authentication token
          service used in server communication

            - ``gateway``: (usually ``uuidentity.plus4u.net``) domain gateway of the `OIDC` service
            - ``uuAppName``: (usually ``uu-oidc-maing02``) full name of the `OIDC` uuApp
            - ``awid``
            - ``clientId``
            - ``clientSecret``
            - ``uuCmd``: (usually ``oidc/grantToken``) uuCmd enpoint for token granting
            - ``tokenPath``: (usually ``./oidc-token``) filesystem location (on
              the IoT gateway) where the token will be saved

    Args:
        config: dictionary with configuration, see above
        fn_post_request: optional function to get a token response from server,
            defaults to :meth:`requests.post`
        refresh_token_on_init: call :meth:`.refresh_token` on initialization of this class
        token_leeway: leeway (drift) between Client and Server Clock [s], defaults to 60 s
            fresh token is requested when token is to be expired in less than token_leeway [s]
            the lower the leeway, the more often is token going to be requested
            the token validity time is controlled by the server, this option accounts only for drift
    """

    _config: dict
    _token: Optional[str]
    _user_agent: str
    _token_expires_at: Optional[float]
    _auth_active: bool
    _token_leeway: float

    def __init__(
        self,
        config: dict,
        fn_token_request: Callable[..., requests.Response] = requests.post,
        refresh_token_on_init: bool = True,
        token_leeway: float = 60,
    ):
        self._config = config
        self._token = None
        self._token_expires_at = None
        self._user_agent = ua.UserAgentBuilder("uun-iot", uun_iot.__version__).build()
        self._token_leeway = token_leeway
        self._auth_active = (
            "uuApp" in self._config
            and "uuThing" in self._config
            and "oidcGrantToken" in self._config
        )
        self._fn_token_request = fn_token_request

        if refresh_token_on_init and self._auth_active:
            self.refresh_token()
        else:
            if refresh_token_on_init:
                logger.info(
                    "UuApp connection & gateway authentication is not "
                    "defined in the configuration file. Are you sure, you do not "
                    "want to use the connection? It will not be possible to "
                    "issue requests to uu servers."
                )
            logger.debug("Not granting any auth token.")

    def _store_token(self, token_json: dict) -> None:
        """Save serialized token to file."""
        with open(self._config["oidcGrantToken"]["tokenPath"], "w") as file:
            file.write(json.dumps(token_json))

    def is_token_expired(self) -> bool:
        """
        # view with respect to server-centered time
        #       <-> leeway
        # ++++++==|-----
        #         |
        #    server_token_expire
        #
        # +: when (local) now is there, token is valid
        # =: when (local) now is there, token is valid but apply for a new token
        #      because of the possible leeway between client and server clocks
        # -: when (local) now is there, token is invalid
        """
        return (
            self._token_expires_at is None
            or self._token_expires_at - self._token_leeway < time.time()
        )

    def refresh_token(self) -> bool:
        """Refresh token if expired. If authentication is disabled, noops and returns False.

        Returns False if token refresh was not needed - that is, if token is
        already loaded and valid. Refresh token and return True otherwise.

        Raises:
            TokenError: when a valid token could not be obtained due to network or server error
            TokenCommandError (subclass of TokenError): server-side uuApp returned error
        """
        if not self._auth_active:
            return False

        if self._token is None:
            # load from file
            token_path = self._config["oidcGrantToken"]["tokenPath"]
            try:
                with open(token_path) as json_file:
                    token = json.load(json_file)
                    self._token = token["id_token"]
                    self._token_expires_at = float(token["expires_at"])

                logger.debug(
                    "loaded token from %s, expires at [%s]",
                    token_path,
                    datetime.datetime.fromtimestamp(self._token_expires_at),
                )
            except IOError:
                logger.debug("loading token from %s failed, file not found", token_path)
            except json.JSONDecodeError:
                logger.debug("Invalid JSON token file.")
            except KeyError:
                logger.debug("Invalid structure of token file.")

        if self.is_token_expired():
            self._token_expires_at = self._grant_token(self._fn_token_request)
            logger.debug(
                "granted new token, expires at [%s]",
                datetime.datetime.fromtimestamp(self._token_expires_at),
            )
            return True

        return False

    def _grant_token(self, fn_post_request: Callable[..., requests.Response]) -> float:
        """Grant token.

        Refresh and save the new token.

        Args:
            fn_post_request: function to get a token response from server

        Returns:
             expiry date as unix timestamp

        Raises:
            TokenError: when a valid token could not be obtained due to network or server error
            TokenCommandError: server-side uuApp returned error
        """
        scope_host = self._config["uuApp"]["gateway"]
        scope_context = self._config["uuApp"]["uuAppName"]
        scope_awid = self._config["uuApp"]["awid"]
        post_data = {
            "grant_type": "password",
            "username": None,
            "password": None,
            "accessCode1": self._config["uuThing"]["accessCode1"],
            "accessCode2": self._config["uuThing"]["accessCode2"],
            "scope": f"openid https://{scope_host}/{scope_context}/{scope_awid}",
        }

        try:
            post_data.update(
                {
                    "client_id": self._config["oidcGrantToken"]["clientId"],
                    "client_secret": self._config["oidcGrantToken"]["clientSecret"],
                }
            )
        except KeyError:
            # does not matter if these are not present - not required - depends on server settings
            pass

        headers = {"Content-Type": "application/json", "User-Agent": self._user_agent}
        uucmd = self._config["oidcGrantToken"]["uuCmd"]

        host = self._config["oidcGrantToken"]["gateway"]
        uu_app_name = self._config["oidcGrantToken"]["uuAppName"]
        awid = self._config["oidcGrantToken"]["awid"]
        url = f"https://{host}/{uu_app_name}/{awid}/{uucmd}"
        response = None
        try:
            response = fn_post_request(url, headers=headers, json=post_data, timeout=20)
            response.raise_for_status()
        except requests.HTTPError as e:
            assert response is not None
            logger.log(
                logging.DEBUG,
                "`%s` POST response (%s): %s",
                uucmd,
                response.status_code,
                response.text,
            )
            status = response.status_code
            try:
                error_json = response.json()
            except json.JSONDecodeError as exc:
                raise TokenError(
                    "A server error occured while getting a token and could not decode"
                    " JSON error object."
                ) from exc
            if "uuAppErrorMap" in error_json:
                raise TokenCommandError(error_json["uuAppErrorMap"], status) from e
            raise TokenError(
                "Server error occured but could not get more information."
            ) from e
        except requests.RequestException as e:
            logger.log(
                logging.WARNING,
                "`%s` POST RequestException when getting a new token: %s",
                uucmd,
                str(e),
            )
            raise TokenError(
                "A network error occured when requesting new token."
            ) from e

        try:
            token_json = response.json()
            self._token = token_json["id_token"]
            token_json["expires_at"] = time.time() + float(token_json["expires_in"])
        except json.JSONDecodeError as e:
            raise TokenError(
                "While getting a token, could not decode received JSON server response."
            ) from e
        except KeyError as e:
            raise TokenError("Token did not have required fields.") from e
        except ValueError as e:
            raise TokenError("Token has invalid value types.") from e

        self._store_token(token_json)
        return token_json["expires_at"]

    def get_uucmd_url(self, uucmd: str) -> str:
        """Return fully quallified URL from relative uucmd string.

        Args:
            uucmd: uucmd in relative path, eg. ``gateway/getWeather``
        """
        host = self._config["uuApp"]["gateway"]
        uu_app_name = self._config["uuApp"]["uuAppName"]
        awid = self._config["uuApp"]["awid"]
        return f"https://{host}/{uu_app_name}/{awid}/{uucmd}"

    def get_auth_headers(self, content_type: str = "application/json"):
        """Get request headers with Bearer authentication.
        The token is refreshed automatically, if expired.

        Headers also includes specified ``Content-type`` and uun-iot's ``User-Agent``.
        """
        if self.is_token_expired():
            self.refresh_token()
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-type": content_type,
            "User-Agent": self._user_agent,
        }

    def custom_request(
        self,
        custom_send_f: Callable[[object], requests.Response],
        dto_in: Optional[object] = None,
        label: Optional[str] = None,
        log_level: int = logging.WARNING,
    ) -> Tuple[
        Optional[requests.Response],
        Optional[Union[TokenError, requests.RequestException]],
    ]:
        """
        Custom request wrapper for catching :mod:`requests`-related and token-acquiring-related
        Exceptions. Token errors, request exceptions, including HTTP non-success status codes,
        are suppressed, logged with specified level and returned.

        Supply your own :attr:`custom_send_f` function (taking :attr:`dto_in` as
        only argument) and outputting a :attr:`requests.Response`. To make an
        authenticated request, you should use authentication headers available
        through :meth:`.get_auth_headers`. Note that you can specify the headers
        either directly during *definition*, or during *evaluation* of
        :attr:`custom_send_f`. The latter is preferred due to handling TokenErrors
        in a unified way with other exceptions. Note that token acquisition is not in
        scope of :meth:`.custom_request` and has to be supplied by caller.

        See also :meth:`.get_uucmd_url` and :meth:`.get_auth_headers` for
        constructing own function.

        .. note::
            Example for ``custom_send_f`` follows.

            .. code-block:: python

                uucmd = "gateway/heartbeat"
                full_url = uuappclient.get_uucmd_url(uucmd)
                def handler(dto_in):
                    return requests.get(full_url, headers=self.get_auth_headers(), json=dto_in_, timeout=20)
                uuappclient.custom_request(handler, {"key": "value"}, uucmd)


        This function will
            - call :attr:`custom_send_f` with :attr:`dto_in` positional
              argument,
            - raise for non-success HTTP status codes
            - catch :attr:`requests.HTTPError` and
              :attr:`requests.RequestException`,
            - log the exceptions and
            - returns response along with the exception

        Args:
            custom_send_f: custom send function which is used instead of
                :meth:`requests.get` label: label used in log messages to identify the request
            dto_in: dictionary data to send. If ``None``, pass ``{}`` to :attr:`custom_send_f`.
            log_level: optional logging level for possible exceptions, defaults to ``logging.WARNING``

        Returns: Tuple ``(response, exc)``,
                - :class:`requests.Response` response, ``None`` if non-HTTP (not
                  200 HTTP status code) exception was raised
                - ``exc``: :class:`requests.RequestException` or :class:`TokenError` if the same
                  exception was raised during request. ``None`` if no exception during request was raised

        Raises: None
        """

        if dto_in is None:
            dto_in = {}

        response = None
        exc = None
        try:
            response = custom_send_f(dto_in)
            response.raise_for_status()
        except requests.HTTPError as e:
            assert response is not None
            logger.log(
                log_level,
                "`%s` response (%s): %s",
                label,
                response.status_code,
                response.text,
            )
            exc = e
        except requests.RequestException as e:
            logger.log(log_level, "`%s` RequestException: %s", label, str(e))
            exc = e
        except TokenError as e:
            logger.log(log_level, "`%s` TokenError: %s", label, str(e))
            exc = e

        return response, exc

    def get(
        self,
        uucmd: str,
        dto_in: Optional[dict] = None,
        log_level: int = logging.WARNING,
    ) -> Tuple[
        Optional[requests.Response],
        Optional[Union[TokenError, requests.RequestException]],
    ]:
        """
        Get request using an authenticated Bearer token.
        Token errors, request exceptions, including HTTP non-success status codes, are suppressed,
        logged with specified level and returned.
        See :meth:`.custom_request` for more informaton.

        Args:
            uucmd: UuCmd in relative path format, eg. ``gateway/heartbeat``
            dto_in: data to send
            log_level: optional logging level for possible exceptions,
                defaults to ``logging.WARNING``

        Returns:
            Tuple ``(response, exc)``,
                - :class:`requests.Response` response, ``None`` if non-HTTP (not 200 HTTP status code)
                  exception was raised
                - :class:`requests.RequestException` exc is None if no exception
                  during request was raised
        """

        full_url = self.get_uucmd_url(uucmd)

        def get_f(dto_in_):
            # ask for headers in the handler function, custom_request first refreshes token
            logger.debug("`%s` GET request, payload: %s", uucmd, dto_in)
            return requests.get(
                full_url, headers=self.get_auth_headers(), json=dto_in_, timeout=20
            )

        return self.custom_request(get_f, dto_in, uucmd, log_level)

    def get_ignore_http_err(
        self,
        uucmd: str,
        dto_in: Optional[dict] = None,
        log_level: int = logging.WARNING,
    ) -> requests.Response:
        """
        GET request with authentication. Ignore HTTP errors, raise errors for other network errors.
        Logs all errors (including HTTP non-200) with :attr:`log_level` severity.
        See :meth:`.custom_request` for more informaton.

        Args:
            uucmd: uuCmd path of the target uuApp
            dto_in: data to be passed as JSON input to the uuApp
            log_level: logging library level of network error, default logging.WARNING

        Raises: :class:`requests.RequestException` or :class:`TokenError`
        """

        r, exc = self.get(uucmd, dto_in, log_level)
        if exc is not None:
            try:
                raise exc
            except requests.HTTPError:
                pass
        assert r is not None
        return r

    def post(
        self,
        uucmd: str,
        dto_in: Optional[Union[dict, MultipartEncoder]] = None,
        log_level: int = logging.WARNING,
    ) -> Tuple[
        Optional[requests.Response],
        Optional[Union[TokenError, requests.RequestException]],
    ]:
        """
        POST request using an authenticated Bearer token.
        Request exceptions, including HTTP non-success status codes, are suppressed, logged with specified level and returned.
        See :meth:`.custom_request` for more informaton.

        Args:
            uucmd: UuCmd in relative path format, eg. ``gateway/heartbeat``
            dto_in: data to send, dictionary or MultipartEncoder data
            log_level: optional logging level for possible exceptions,
                defaults to ``logging.WARNING``

        Returns:
            Tuple ``(response, exc)``,
                - :class:`requests.Response` response, ``None`` if non-HTTP (not 200 HTTP status code)
                  exception was raised
                - :class:`requests.RequestException` exc is None if no exception
                  during request was raised

        Raises: ValueError if ``dto_in`` type is not ``dict`` or ``MultipartEncoder``
        """

        if dto_in is None:
            dto_in = {}

        full_url = self.get_uucmd_url(uucmd)
        if isinstance(dto_in, dict):
            headers = self.get_auth_headers

            def post_f(dto_in_):
                logger.debug("`%s` POST request, payload: %s", uucmd, dto_in)
                return requests.post(
                    full_url, headers=headers(), json=dto_in_, timeout=20
                )

        elif isinstance(dto_in, MultipartEncoder):
            headers = partial(self.get_auth_headers, dto_in.content_type)

            def post_f(dto_in_):
                logger.debug("`%s` MULTIPART request, payload: %s", uucmd, dto_in)
                return requests.post(
                    full_url, headers=headers(), data=dto_in_, timeout=20
                )

        else:
            raise ValueError(f"Invalid dto_in type: {type(dto_in)}")

        return self.custom_request(post_f, dto_in, uucmd, log_level)

    def post_ignore_http_err(
        self,
        uucmd: str,
        dto_in: Optional[Union[dict, MultipartEncoder]] = None,
        log_level: int = logging.WARNING,
    ) -> requests.Response:
        """
        POST request with authentication. Ignore HTTP errors, raise errors for other network errors.
        Logs all errors (including HTTP non-200) with :attr:`log_level` severity.

        Args:
            uucmd: uuCmd path of the target uuApp
            dto_in: data to be passed as JSON input to the uuApp
            log_level: logging library level of network error, default logging.WARNING

        Raises: :class:`requests.RequestException` or :class:`TokenError`
        """
        r, exc = self.post(uucmd, dto_in, log_level)
        if exc is not None:
            try:
                raise exc
            except requests.HTTPError:
                pass
        assert r is not None
        return r

    def multipart(
        self,
        uucmd: str,
        dto_in: Optional[dict] = None,
        log_level: int = logging.WARNING,
    ) -> Tuple[
        Optional[requests.Response],
        Optional[Union[TokenError, requests.RequestException]],
    ]:
        """POST request with authentication and MULTIPART encoded data
        with oidc2 authentication. Useful for sending binary data (images, ...). See
        https://toolbelt.readthedocs.io/en/latest/user.html#multipart-form-data-encoder
        for information about multipart encoder.

        Pass data to dto_in, they will be transformed using MultipartEncoder and passed to
        :meth:`UuAppClient.post` (see for more information and usage).
        """

        if dto_in is None:
            return self.post(uucmd, None, log_level)
        multipart_encoded = MultipartEncoder(fields=dto_in)
        return self.post(uucmd, multipart_encoded, log_level)


class UuCmdSession:
    """
    Send all data with UuCmd in one session to avoid creating multiple connections.

    Args:
        uuclient: initialized authentication client
        uucmd: UuCmd in relative path format, eg. ``gateway/getWeather``
        log_level: ``logging`` library log level to use for network and HTTP errors,
            defaults to :attr:`logging.WARNING`
    """

    def __init__(
        self, uuclient: UuAppClient, uucmd: str, log_level: int = logging.WARNING
    ):
        self._uucmd = uucmd
        self._loglevel = log_level
        self._url = uuclient.get_uucmd_url(uucmd)
        self._session = requests.Session()
        self._uuclient = uuclient

    def update_headers(self):
        """Update session auth headers ensured to containing a valid Bearer token."""
        self._session.headers.update(self._uuclient.get_auth_headers())

    def get(
        self, data: Optional[dict] = None, log_level: int = logging.WARNING
    ) -> Tuple[
        Optional[requests.Response],
        Optional[Union[TokenError, requests.RequestException]],
    ]:
        """Authenticated GET request with session.
        See :meth:`UuAppClient.get` for more information."""

        full_url = self._uuclient.get_uucmd_url(self._uucmd)

        def get_f(dto_in_):
            self.update_headers()
            logger.debug("`%s` GET request, payload: %s", self._uucmd, data)
            return self._session.get(full_url, json=dto_in_, timeout=20)

        return self._uuclient.custom_request(get_f, data, self._uucmd, log_level)

    def post(
        self,
        data: Optional[t.Union[dict, list]] = None,
        log_level: int = logging.WARNING,
    ) -> Tuple[
        Optional[requests.Response],
        Optional[Union[TokenError, requests.RequestException]],
    ]:
        """Authenticated POST request with session.
        See :meth:`UuAppClient.post` for more information."""

        full_url = self._uuclient.get_uucmd_url(self._uucmd)

        def post_f(dto_in_):
            self.update_headers()
            logger.debug("`%s` POST request, payload: %s", self._uucmd, data)
            return self._session.post(full_url, json=dto_in_, timeout=20)

        return self._uuclient.custom_request(post_f, data, self._uucmd, log_level)
