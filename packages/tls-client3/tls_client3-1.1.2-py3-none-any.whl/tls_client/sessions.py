from .cffi import request, freeMemory, destroySession
from requests.structures import CaseInsensitiveDict
from requests import Request, Response
from collections import OrderedDict
from .adapters import TLSClientAdapter
from .config import TLSClientConfig
from importlib.metadata import version
from typing import Optional, Union
import warnings
from json import dumps, loads
import ctypes
import uuid
import requests

__version__ = version("tls_client3")

class Session(requests.Session):

    def __init__(
        self,
        config: Optional[Union[TLSClientConfig, str]] = None,
        *args,
        **kwargs,  # for legacy support
    ) -> None:
        """
    Initialize the TLS client.

    This constructor supports both the modern way of passing a `TLSClientConfig` object
    and the legacy way using positional or keyword arguments. Legacy usage is deprecated
    and will be removed in a future release.

    :param config: Configuration for the TLS client. Can be either a `TLSClientConfig` instance
                  or a legacy `client_identifier` string.
    :type config: TLSClientConfig or str, optional
    :param args: Positional arguments for legacy configuration.
    :param kwargs: Additional keyword arguments. May include deprecated legacy fields
                   or valid options such as `max_retries`.

    :keyword int max_retries: Number of retries to use for the underlying TLS adapter.

    .. deprecated:: 0.2.0
        Using positional arguments or legacy keyword arguments is deprecated.
        Please pass a `TLSClientConfig` instance instead.

        The following legacy parameters are deprecated:

        :keyword str client_identifier: Identifier of the TLS fingerprint preset (e.g., "chrome_112").
        :keyword str ja3_string: Custom JA3 fingerprint string.
        :keyword dict h2_settings: HTTP/2 SETTINGS frame values.
        :keyword list h2_settings_order: Order of HTTP/2 SETTINGS keys.
        :keyword list supported_signature_algorithms: Supported TLS signature algorithms.
        :keyword list supported_delegated_credentials_algorithms: Delegated credentials algorithms.
        :keyword list supported_versions: TLS versions to advertise.
        :keyword list key_share_curves: Elliptic curves for key exchange.
        :keyword str cert_compression_algo: Certificate compression algorithm.
        :keyword bool additional_decode: Enable additional decoding logic.
        :keyword list pseudo_header_order: Pseudo-header order for HTTP/2.
        :keyword int connection_flow: HTTP/2 connection flow control value.
        :keyword list priority_frames: HTTP/2 priority frame definitions.
        :keyword list header_order: HTTP header order to send.
        :keyword dict header_priority: Priority values for HTTP headers.
        :keyword bool random_tls_extension_order: Randomize TLS extension order.
        :keyword bool force_http1: Force HTTP/1.1 instead of HTTP/2.
        :keyword bool catch_panics: Catch internal panics (used internally).
        :keyword bool debug: Enable debug logging.
        :keyword bool certificate_pinning: Enforce certificate pinning.
        """
        
        legacy_keys = [
            "client_identifier", "ja3_string", "h2_settings", "h2_settings_order",
            "supported_signature_algorithms", "supported_delegated_credentials_algorithms",
            "supported_versions", "key_share_curves", "cert_compression_algo",
            "additional_decode", "pseudo_header_order", "connection_flow",
            "priority_frames", "header_order", "header_priority",
            "random_tls_extension_order", "force_http1", "catch_panics",
            "debug", "certificate_pinning"
        ]
        used_legacy = False

        if isinstance(config, TLSClientConfig):
            pass
        elif config is not None:
            # config - is client_identifier
            args = (config,) + args
            config = None
            used_legacy = True

        if config is None:
            legacy_kwargs = dict(zip(legacy_keys, args))
            legacy_kwargs.update(kwargs)

            if not used_legacy:
                used_legacy = any(key in kwargs for key in legacy_keys)

            if used_legacy:
                warnings.warn(
                    "Using legacy positional arguments or legacy keyword arguments is deprecated. "
                    "Use config=TLSClientConfig(...) instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )

            config = TLSClientConfig(**legacy_kwargs)

        for key in legacy_keys:
            kwargs.pop(key, None)

        self._session_id = str(uuid.uuid4())
        
        super().__init__()

        self.headers = CaseInsensitiveDict(
            {
                "User-Agent": f"tls-client/{__version__}",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "*/*",
                "Connection": "keep-alive",
            }
        )

        self.adapters = OrderedDict()
        adapter = TLSClientAdapter(config, **kwargs)
        self.mount("https://", adapter)
        self.mount("http://", adapter)

    def close(self) -> str:
        destroy_session_payload = {
            "sessionId": self._session_id
        }

        destroy_session_response = destroySession(dumps(destroy_session_payload).encode('utf-8'))
        # we dereference the pointer to a byte array
        destroy_session_response_bytes = ctypes.string_at(destroy_session_response)
        # convert our byte array to a string (tls client returns json)
        destroy_session_response_string = destroy_session_response_bytes.decode('utf-8')
        # convert response string to json
        destroy_session_response_object = loads(destroy_session_response_string)

        freeMemory(destroy_session_response_object['id'].encode('utf-8'))

        return destroy_session_response_string

    def execute_request(
        self,
        **kwargs
    ) -> Response:
        return self.request(**kwargs)

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        verify=None,
        cert=None,
        json=None,
        headers_order=None,
        insecure_skip_verify=None,
        timeout_seconds=None,
        proxy=None
    ):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects``
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param hooks: (optional) Dictionary mapping hook name to one event or
            list of events, event must be callable.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``. When set to
            ``False``, requests will accept any TLS certificate presented by
            the server, and will ignore hostname mismatches and/or expired
            certificates, which will make your application vulnerable to
            man-in-the-middle (MitM) attacks. Setting verify to ``False``
            may be useful during local development or testing.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :param headers_order: list with headers in the same order as they appear in the request
        :rtype: requests.Response
        """
        # For backward compatibility
        verify = insecure_skip_verify if insecure_skip_verify is not None else verify
        timeout = timeout_seconds if timeout_seconds is not None else timeout
        if type(proxy) is dict:
            proxies = proxy
        elif type(proxy) is str:
            proxies = {
                "http": proxy,
                "https": proxy
            }

        # Create the Request.
        req = Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
        )
        req._headers_order = headers_order
        prep = self.prepare_request(req)

        proxies = proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, None, verify, cert
        )

        # Send the request.
        send_kwargs = {
            "timeout": timeout,
            "allow_redirects": allow_redirects,
        }
        send_kwargs.update(settings)
        resp = self.send(prep, **send_kwargs)

        return resp

    def prepare_request(self, request):
        p = super().prepare_request(request)
        p._session_id = self._session_id
        p._headers_order = request._headers_order
        return p