import httpx
from bayesline.api import (
    AsyncBayeslineApi,
    AsyncUserPermissionsApi,
    BayeslineApi,
    UserPermissionsApi,
)
from bayesline.api.equity import AsyncBayeslineEquityApi, BayeslineEquityApi

from bayesline.apiclient._src.apiclient import ApiClient, AsyncApiClient
from bayesline.apiclient._src.equity.client import (
    AsyncBayeslineEquityApiClient,
    BayeslineEquityApiClient,
)
from bayesline.apiclient._src.permissions import (
    AsyncUserPermissionsApiClient,
    UserPermissionsApiClient,
)


class AsyncBayeslineApiClient(AsyncBayeslineApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("v1")
        self._equity_client = AsyncBayeslineEquityApiClient(self._client)
        self._permissions_client = AsyncUserPermissionsApiClient(self._client)

    @classmethod
    def new_client(
        cls: type["AsyncBayeslineApiClient"],
        *,
        endpoint: str = "https://api.bayesline.com",
        api_key: str,
        client: httpx.AsyncClient | None = None,
        verify: bool = True,
    ) -> AsyncBayeslineApi:
        return cls(
            AsyncApiClient(
                endpoint,
                auth_str=api_key,
                auth_type="API_KEY",
                client=client,
                verify=verify,
            )
        )

    @property
    def equity(self) -> AsyncBayeslineEquityApi:
        return self._equity_client

    @property
    def permissions(self) -> AsyncUserPermissionsApi:
        return self._permissions_client


class BayeslineApiClient(BayeslineApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("v1")
        self._equity_client = BayeslineEquityApiClient(self._client)
        self._permissions_client = UserPermissionsApiClient(self._client)

    @classmethod
    def new_client(
        cls: type["BayeslineApiClient"],
        *,
        endpoint: str = "https://api.bayesline.com",
        api_key: str,
        client: httpx.Client | None = None,
        verify: bool = True,
    ) -> BayeslineApi:
        return cls(
            ApiClient(
                endpoint,
                auth_str=api_key,
                auth_type="API_KEY",
                client=client,
                verify=verify,
            )
        )

    @classmethod
    def new_async_client(
        cls: type["BayeslineApiClient"],
        *,
        endpoint: str = "https://api.bayesline.com",
        api_key: str,
        client: httpx.AsyncClient | None = None,
        verify: bool = True,
    ) -> AsyncBayeslineApi:
        return AsyncBayeslineApiClient.new_client(
            endpoint=endpoint,
            api_key=api_key,
            client=client,
            verify=verify,
        )

    @property
    def equity(self) -> BayeslineEquityApi:
        return self._equity_client

    @property
    def permissions(self) -> UserPermissionsApi:
        return self._permissions_client
