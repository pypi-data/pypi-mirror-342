import functools
import json
import os
import time
from http import HTTPStatus
from logging import getLogger
from typing import Any, Awaitable, Callable, Literal

import httpx
from pydantic import BaseModel

logger = getLogger(__name__)

_CLIENT_ERROR_CODES = set(range(400, 500))
_SERVER_ERROR_CODES = set(range(500, 600))
_DEFAULT_TIMEOUT = httpx.Timeout(
    None,
    connect=int(os.getenv("BAYESLINE_APICLIENT_CONNECT_TIMEOUT", 300)),
    read=int(os.getenv("BAYESLINE_APICLIENT_READ_TIMEOUT", 300)),
    write=int(os.getenv("BAYESLINE_APICLIENT_WRITE_TIMEOUT", 300)),
)

MOVED_PERMANENTLY = 301
MOVED_TEMPORARILY = 30


# this address the fun quirk with the AWS ingress controller
# which rewrites http:// urls to https:// and sends a 301 permanent redirect
# The k8s pods internally work on http:// as they should, so if that process
# sends a temporary redirect 307 then then this client will follow it.
# but this redirect has http:// in front of it which then hits the ingress
# controller which rewrites it to https:// and sends a 301 permanent redirect.
# now this becomes a problem when the original request was anything other than a
# GET request because the HTTP protocol prescribes that temporary redirects
# retain their method, but permanent redirects are rewritten to GET.
# this changes the original method from POST to GET and the request fails.
# In this custom transport we always treat permanent redirects as temporary
# to alleviate this issue.
class PermanentToTemporaryRedirectTransport(httpx.HTTPTransport):

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        response = super().handle_request(request)
        if response.status_code == MOVED_PERMANENTLY:
            response.status_code = MOVED_TEMPORARILY

        if "Location" in response.headers:
            location = response.headers["Location"]
            if location.startswith("http://") and request.url.scheme == "https":
                response.headers["Location"] = location.replace("http://", "https://")

        return response


class AsyncPermanentToTemporaryRedirectTransport(httpx.AsyncHTTPTransport):

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        response = await super().handle_async_request(request)
        if response.status_code == MOVED_PERMANENTLY:
            response.status_code = MOVED_TEMPORARILY

        if "Location" in response.headers:
            location = response.headers["Location"]
            if location.startswith("http://") and request.url.scheme == "https":
                response.headers["Location"] = location.replace("http://", "https://")

        return response


class ApiClientError(Exception):
    pass


class ApiServerError(Exception):
    pass


class BaseApiClient:

    def __init__(
        self,
        endpoint: str,
        *,
        auth_str: str,
        auth_type: Literal["BEARER", "API_KEY"] = "API_KEY",
        base_path: str | None = None,
        extra_params: dict[str, Any] | None = None,
    ):
        if not (endpoint.strip() == "" or endpoint.strip()[-1] != "/"):
            raise AssertionError("endpoint should not end with a slash")
        if not (not base_path or base_path.strip()[-1] != "/"):
            raise AssertionError("base_path should not end with a slash")
        if not (not base_path or base_path.strip()[0] != "/"):
            raise AssertionError("base_path should not start with a slash")
        self.endpoint = endpoint.strip()
        self.auth_str = auth_str
        self.auth_type = auth_type
        self.base_path = "" if not base_path else base_path.strip()
        self.extra_params = extra_params or {}

    def make_url(self, url: str, endpoint: bool = True) -> str:
        if url.startswith("/"):
            url = url[1:]

        result = []
        if endpoint:
            result.append(self.endpoint)
        if self.base_path:
            result.append(self.base_path)
        if url:
            result.append(url)

        return "/".join(result)

    def _make_params_and_headers(
        self, params: dict[str, Any] | None
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        params = params or {}
        params.update(self.extra_params)
        if self.auth_type == "BEARER":
            return params, {"Authorization": f"Bearer {self.auth_str}"}
        else:
            return {**params, "api_key": self.auth_str}, {}

    def __str__(self) -> str:
        endpoint, base_path = self.endpoint, self.base_path
        return (
            f"{self.__class__.__name__}("
            f"endpoint={endpoint}, "
            f"auth=***, auth_stype={self.auth_type}, base_path={base_path})"
        )

    def __repr__(self) -> str:
        return str(self)


class ApiClient(BaseApiClient):

    def __init__(
        self,
        endpoint: str,
        *,
        auth_str: str,
        auth_type: Literal["BEARER", "API_KEY"] = "API_KEY",
        base_path: str | None = None,
        client: httpx.Client | None = None,
        verify: bool = True,
        extra_params: dict[str, Any] | None = None,
    ):
        super().__init__(
            endpoint,
            auth_str=auth_str,
            auth_type=auth_type,
            base_path=base_path,
            extra_params=extra_params,
        )
        self.request_executor = client or httpx.Client(
            follow_redirects=True,
            timeout=_DEFAULT_TIMEOUT,
            verify=verify,
            transport=PermanentToTemporaryRedirectTransport(verify=verify),
        )
        self.verify = verify

    def __getstate__(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "auth_str": self.auth_str,
            "auth_type": self.auth_type,
            "base_path": self.base_path,
            "verify": self.verify,
            "extra_params": self.extra_params,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__init__(  # type: ignore
            state["endpoint"],
            auth_str=state["auth_str"],
            auth_type=state["auth_type"],
            base_path=state["base_path"],
            verify=state["verify"],
            extra_params=state["extra_params"],
        )

    def with_base_path(self, base_path: str) -> "ApiClient":
        return ApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=base_path,
            client=self.request_executor,
            extra_params=self.extra_params,
        )

    def append_base_path(self, base_path: str) -> "ApiClient":
        return ApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=self.make_url(base_path, endpoint=False),
            client=self.request_executor,
            extra_params=self.extra_params,
        )

    def get(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)
        return self.raise_for_status(self.request_executor.get)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    def options(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)

        return self.raise_for_status(self.request_executor.options)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    def head(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)

        return self.raise_for_status(self.request_executor.head)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    def post(
        self,
        url: str,
        body: dict[str, Any] | BaseModel | bytes | None,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        if body is not None and data is not None:
            raise ValueError("Only one of json or data should be provided")
        elif body is None and data is None:
            raise ValueError("Either json or data should be provided")

        kwargs: dict[str, Any]
        if isinstance(body, BaseModel):
            kwargs = {"data": body.model_dump_json()}
        elif data is not None:
            kwargs = {"data": data}
        elif isinstance(body, dict):
            kwargs = {"json": body}
        elif isinstance(body, bytes):
            kwargs = {"content": body}
        else:
            kwargs = {"json": body}

        return self.raise_for_status(self.request_executor.post)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
            **kwargs,
        )

    def put(
        self,
        url: str,
        body: dict[str, Any] | BaseModel | bytes,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        kwargs: dict[str, Any]
        if isinstance(body, BaseModel):
            kwargs = {"data": body.model_dump_json()}
        elif isinstance(body, dict):
            kwargs = {"json": body}
        elif isinstance(body, bytes):
            kwargs = {"content": body}
        else:
            kwargs = {"json": body}

        return self.raise_for_status(self.request_executor.put)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
            **kwargs,
        )

    def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        return self.raise_for_status(self.request_executor.delete)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    @staticmethod
    def raise_for_status(fn: Callable[..., httpx.Response]) -> Any:
        @functools.wraps(fn)
        def wrapped(*args, **kwargs: Any) -> Any:  # type: ignore
            response: httpx.Response
            retry: int = 3
            while retry > 0:
                try:
                    now = time.time()
                    response = fn(
                        *args,
                        timeout=_DEFAULT_TIMEOUT,
                        **kwargs,
                    )  # typing: ignore
                    break
                except (httpx.ReadError, httpx.RemoteProtocolError) as e:
                    logger.warning(
                        f"Received read error from server. {str(e)}. Retrying {retry}. "
                        f"Args {args} {kwargs.get('params', {})}",
                    )
                    retry -= 1
                    if retry == 0:
                        raise
                    continue
                except Exception as e:
                    elapsed = time.time() - now
                    raise Exception(
                        f"exception during request. took {elapsed} seconds. "
                        f"Args {args} {kwargs.get('params', {})}",
                    ) from e
                finally:
                    handle_response(response, args)

            return response

        return wrapped


class AsyncApiClient(BaseApiClient):

    def __init__(
        self,
        endpoint: str,
        *,
        auth_str: str,
        auth_type: Literal["BEARER", "API_KEY"] = "API_KEY",
        base_path: str | None = None,
        client: httpx.AsyncClient | None = None,
        verify: bool = True,
        extra_params: dict[str, Any] | None = None,
    ):
        super().__init__(
            endpoint,
            auth_str=auth_str,
            auth_type=auth_type,
            base_path=base_path,
            extra_params=extra_params,
        )
        self.request_executor = client or httpx.AsyncClient(
            follow_redirects=True,
            timeout=_DEFAULT_TIMEOUT,
            verify=verify,
            transport=AsyncPermanentToTemporaryRedirectTransport(verify=verify),
        )
        self.verify = verify

    def __getstate__(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "auth_str": self.auth_str,
            "auth_type": self.auth_type,
            "base_path": self.base_path,
            "verify": self.verify,
            "extra_params": self.extra_params,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__init__(  # type: ignore
            state["endpoint"],
            auth_str=state["auth_str"],
            auth_type=state["auth_type"],
            base_path=state["base_path"],
            verify=state["verify"],
            extra_params=state["extra_params"],
        )

    def sync(self) -> ApiClient:
        return ApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=self.base_path,
            extra_params=self.extra_params,
        )

    def with_base_path(self, base_path: str) -> "AsyncApiClient":
        return AsyncApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=base_path,
            client=self.request_executor,
            extra_params=self.extra_params,
        )

    def append_base_path(self, base_path: str) -> "AsyncApiClient":
        return AsyncApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=self.make_url(base_path, endpoint=False),
            client=self.request_executor,
            extra_params=self.extra_params,
        )

    async def get(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)

        return await self.raise_for_status(self.request_executor.get)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    async def options(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)
        return await self.raise_for_status(self.request_executor.options)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    async def head(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:  # noqa: ANN401
        params, headers = self._make_params_and_headers(params)

        return await self.raise_for_status(self.request_executor.head)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    async def post(
        self,
        url: str,
        body: dict[str, Any] | BaseModel | bytes | None,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        if body is not None and data is not None:
            raise ValueError("Only one of json or data should be provided")
        elif body is None and data is None:
            raise ValueError("Either json or data should be provided")

        kwargs: dict[str, Any]
        if isinstance(body, BaseModel):
            kwargs = {"data": body.model_dump_json()}
        elif data is not None:
            kwargs = {"data": data}
        elif isinstance(body, dict):
            kwargs = {"json": body}
        elif isinstance(body, bytes):
            kwargs = {"content": body}
        else:
            kwargs = {"json": body}

        return await self.raise_for_status(self.request_executor.post)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
            **kwargs,
        )

    async def put(
        self,
        url: str,
        body: dict[str, Any] | BaseModel | bytes,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)

        kwargs: dict[str, Any]
        if isinstance(body, BaseModel):
            kwargs = {"data": body.model_dump_json()}
        elif isinstance(body, dict):
            kwargs = {"json": body}
        elif isinstance(body, bytes):
            kwargs = {"content": body}
        else:
            kwargs = {"json": body}

        return await self.raise_for_status(self.request_executor.put)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
            **kwargs,
        )

    async def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(params)
        return await self.raise_for_status(self.request_executor.delete)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    @staticmethod
    def raise_for_status(fn: Callable[..., Awaitable[httpx.Response]]) -> Any:
        @functools.wraps(fn)
        async def wrapped(*args, **kwargs: Any) -> Any:  # type: ignore
            response: httpx.Response
            retry: int = 3
            while retry > 0:
                try:
                    now = time.time()
                    response = await fn(
                        *args,
                        timeout=_DEFAULT_TIMEOUT,
                        **kwargs,
                    )  # typing: ignore
                    break
                except (httpx.ReadError, httpx.RemoteProtocolError) as e:
                    logger.warning(
                        f"Received read error from server. {str(e)}. Retrying {retry}. "
                        f"Args {args} {kwargs.get('params', {})}",
                    )
                    retry -= 1
                    if retry == 0:
                        raise
                    continue
                except Exception as e:
                    elapsed = time.time() - now
                    raise Exception(
                        f"exception during request. took {elapsed} seconds. "
                        f"Args {args} {kwargs.get('params', {})}",
                    ) from e
                finally:
                    handle_response(response, args)

            return response

        return wrapped


def handle_response(response: httpx.Response, args: Any) -> None:
    if response is not None and response.status_code != HTTPStatus.OK:
        if response.headers.get("content-type") == "application/json":
            content_json = json.loads(response.content)
        else:
            content_json = {"detail": response.content}

        if response.status_code in _SERVER_ERROR_CODES:
            msg = (
                "An error occurred on the server side.",
                "",
                f"Status Code: {response.status_code}",
                os.linesep.join([f"{k}: {v}" for k, v in content_json.items()]),
            )  # type: ignore
            raise ApiServerError(os.linesep.join(msg))
        elif response.status_code in _CLIENT_ERROR_CODES:
            msg = (
                "A client-side error occurred. Please review the request and ",
                "try again.",
                f"Request ID: {response.headers.get('X-request-id')}",
                f"Arguments: {', '.join(map(str, args))}",
                f"Status Code: {response.status_code}",
                os.linesep.join([f"{k}: {v}" for k, v in content_json.items()]),
            )  # type: ignore
            raise ApiClientError(os.linesep.join(msg))
        else:
            response.raise_for_status()
