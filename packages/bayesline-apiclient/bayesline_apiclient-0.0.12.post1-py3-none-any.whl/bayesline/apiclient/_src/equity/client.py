import asyncio
import datetime as dt
import importlib.util
import io
from typing import Any, Literal

import polars as pl
from bayesline.api import (
    AsyncSettingsRegistry,
    SettingsRegistry,
)
from bayesline.api.equity import (
    AssetExposureApi,
    AssetUniverseApi,
    AsyncAssetExposureApi,
    AsyncAssetUniverseApi,
    AsyncBayeslineEquityApi,
    AsyncBayeslineEquityExposureApi,
    AsyncBayeslineEquityIdApi,
    AsyncBayeslineEquityPortfolioApi,
    AsyncBayeslineEquityUniverseApi,
    AsyncBayeslineFactorRiskModelsApi,
    AsyncBayeslineModelConstructionApi,
    AsyncBayeslinePortfolioHierarchyApi,
    AsyncBayeslinePortfolioReportApi,
    AsyncFactorRiskEngineApi,
    AsyncFactorRiskModelApi,
    AsyncModelConstructionEngineApi,
    AsyncPortfolioHierarchyApi,
    BayeslineEquityApi,
    BayeslineEquityExposureApi,
    BayeslineEquityIdApi,
    BayeslineEquityPortfolioApi,
    BayeslineEquityUniverseApi,
    BayeslineFactorRiskModelsApi,
    BayeslineModelConstructionApi,
    BayeslinePortfolioHierarchyApi,
    BayeslinePortfolioReportApi,
    ExposureSettings,
    ExposureSettingsMenu,
    FactorRiskEngineApi,
    FactorRiskModelApi,
    FactorRiskModelSettings,
    FactorRiskModelSettingsMenu,
    FactorType,
    ModelConstructionEngineApi,
    ModelConstructionSettings,
    ModelConstructionSettingsMenu,
    PortfolioHierarchyApi,
    PortfolioHierarchySettings,
    PortfolioHierarchySettingsMenu,
    UniverseSettings,
    UniverseSettingsMenu,
)
from bayesline.api.types import (
    DateLike,
    IdType,
    to_date,
    to_date_string,
)

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient
from bayesline.apiclient._src.equity.portfolio import (
    AsyncBayeslineEquityPortfolioApiClient,
    BayeslineEquityPortfolioApiClient,
)
from bayesline.apiclient._src.equity.portfolioreport import (
    AsyncBayeslinePortfolioReportApiClient,
    BayeslinePortfolioReportApiClient,
)
from bayesline.apiclient._src.settings import (
    AsyncHttpSettingsRegistryClient,
    HttpSettingsRegistryClient,
)

tqdm = lambda x: x  # noqa: E731
if importlib.util.find_spec("tqdm"):
    from tqdm import tqdm  # type: ignore


class BayeslineEquityIdApiClient(BayeslineEquityIdApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("ids")

    def lookup_ids(self, ids: list[str], top_n: int = 0) -> pl.DataFrame:
        response = self._client.get("lookup", params={"ids": ids, "top_n": top_n})
        try:
            response.raise_for_status()
        except Exception as e:
            raise ValueError(response.json()["detail"]) from e
        return pl.read_parquet(io.BytesIO(response.content))


class AsyncBayeslineEquityIdApiClient(AsyncBayeslineEquityIdApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("ids")

    async def lookup_ids(self, ids: list[str], top_n: int = 0) -> pl.DataFrame:
        response = await self._client.get("lookup", params={"ids": ids, "top_n": top_n})
        try:
            response.raise_for_status()
        except Exception as e:
            raise ValueError(response.json()["detail"]) from e
        return pl.read_parquet(io.BytesIO(response.content))


class BayeslineAssetUniverseApiClient(AssetUniverseApi):

    def __init__(
        self,
        client: ApiClient,
        universe_settings: UniverseSettings,
        id_types: list[IdType],
    ):
        self._client = client
        self._universe_settings = universe_settings
        self._id_types = id_types

    @property
    def settings(self) -> UniverseSettings:
        return self._universe_settings

    @property
    def id_types(self) -> list[IdType]:
        return list(self._id_types)

    def coverage(self, id_type: IdType | None = None) -> list[str]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = self._client.post(
            "coverage",
            params=params,
            body=self._universe_settings.model_dump(),
        )

        return response.json()

    def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        response = self._client.post(
            "dates",
            params={"range_only": range_only, "trade_only": trade_only},
            body=self._universe_settings.model_dump(),
        )
        return [to_date(d) for d in response.json()]

    def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pl.DataFrame:
        params: dict[str, Any] = {
            "mode": mode,
            "filter_mode": filter_mode,
        }
        _check_and_add_id_type(self._id_types, id_type, params)
        response = self._client.post(
            "input-id-mapping",
            params=params,
            body=self._universe_settings.model_dump(),
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def counts(
        self,
        dates: bool = True,
        industry_level: int = 0,
        region_level: int = 0,
        universe_type: Literal["estimation", "coverage", "both"] = "both",
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["dates"] = dates
        params["industry_level"] = industry_level
        params["region_level"] = region_level
        params["universe_type"] = universe_type

        response = self._client.post(
            "counts",
            params=params,
            body=self._universe_settings.model_dump(),
        )

        return pl.read_parquet(io.BytesIO(response.content))

    def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        params["filter_tradedays"] = filter_tradedays

        response = self._client.post(
            "",
            params=params,
            body=self._universe_settings.model_dump(),
        )

        return pl.read_parquet(io.BytesIO(response.content))


class AsyncBayeslineAssetUniverseApiClient(AsyncAssetUniverseApi):

    def __init__(
        self,
        client: AsyncApiClient,
        universe_settings: UniverseSettings,
        id_types: list[IdType],
    ):
        self._client = client
        self._universe_settings = universe_settings
        self._id_types = id_types

    @property
    def settings(self) -> UniverseSettings:
        return self._universe_settings

    @property
    def id_types(self) -> list[IdType]:
        return list(self._id_types)

    async def coverage(self, id_type: IdType | None = None) -> list[str]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = await self._client.post(
            "coverage",
            params=params,
            body=self._universe_settings.model_dump(),
        )

        return response.json()

    async def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        response = await self._client.post(
            "dates",
            params={"range_only": range_only, "trade_only": trade_only},
            body=self._universe_settings.model_dump(),
        )
        return [to_date(d) for d in response.json()]

    async def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pl.DataFrame:
        params: dict[str, Any] = {
            "mode": mode,
            "filter_mode": filter_mode,
        }
        _check_and_add_id_type(self._id_types, id_type, params)
        response = await self._client.post(
            "input-id-mapping",
            params=params,
            body=self._universe_settings.model_dump(),
        )
        return pl.read_parquet(io.BytesIO(response.content))

    async def counts(
        self,
        dates: bool = True,
        industry_level: int = 0,
        region_level: int = 0,
        universe_type: Literal["estimation", "coverage", "both"] = "both",
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["dates"] = dates
        params["industry_level"] = industry_level
        params["region_level"] = region_level
        params["universe_type"] = universe_type

        response = await self._client.post(
            "counts",
            params=params,
            body=self._universe_settings.model_dump(),
        )

        return pl.read_parquet(io.BytesIO(response.content))

    async def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        filter_tradedays: bool = False,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        params["filter_tradedays"] = filter_tradedays

        response = await self._client.post(
            "",
            params=params,
            body=self._universe_settings.model_dump(),
        )

        return pl.read_parquet(io.BytesIO(response.content))


class BayeslineEquityUniverseApiClient(BayeslineEquityUniverseApi):
    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("universe")
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/universe"),
            UniverseSettings,
            UniverseSettingsMenu,
        )

    @property
    def settings(self) -> SettingsRegistry[UniverseSettings, UniverseSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | UniverseSettings) -> AssetUniverseApi:
        id_types = self._settings.available_settings().id_types

        if isinstance(ref_or_settings, UniverseSettings):
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return BayeslineAssetUniverseApiClient(
                self._client, ref_or_settings, id_types
            )
        else:
            universe_settings = self.settings.get(ref_or_settings)
            return BayeslineAssetUniverseApiClient(
                self._client,
                universe_settings,
                id_types,
            )


class AsyncBayeslineEquityUniverseApiClient(AsyncBayeslineEquityUniverseApi):
    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("universe")
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/universe"),
            UniverseSettings,
            UniverseSettingsMenu,
        )

    @property
    def settings(self) -> AsyncSettingsRegistry[UniverseSettings, UniverseSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | UniverseSettings
    ) -> AsyncAssetUniverseApi:
        settings_menu = await self._settings.available_settings()
        id_types = settings_menu.id_types

        if isinstance(ref_or_settings, UniverseSettings):
            settings_menu.validate_settings(ref_or_settings)
            return AsyncBayeslineAssetUniverseApiClient(
                self._client, ref_or_settings, id_types
            )
        else:
            universe_settings = await self.settings.get(ref_or_settings)
            return AsyncBayeslineAssetUniverseApiClient(
                self._client,
                universe_settings,
                id_types,
            )


class BayeslineAssetExposureApiClient(AssetExposureApi):

    def __init__(
        self,
        client: ApiClient,
        exposure_settings: ExposureSettings,
        id_types: list[IdType],
        universe_api: BayeslineEquityUniverseApi,
    ):
        self._client = client
        self._exposure_settings = exposure_settings
        self._id_types = id_types
        self._universe_api = universe_api

    @property
    def settings(self) -> ExposureSettings:
        return self._exposure_settings

    def dates(
        self,
        universe: str | int | UniverseSettings | AssetUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = self._client.post(
            "dates",
            params={"range_only": range_only},
            body={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        return [to_date(d) for d in response.json()]

    def coverage_stats(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["by"] = by

        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncAssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = self._client.post(
            "/coverage-stats",
            params=params,
            body={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        response.raise_for_status()
        return pl.read_parquet(io.BytesIO(response.content))

    def get(
        self,
        universe: str | int | UniverseSettings | AssetUniverseApi,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)

        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        body = {
            "universe_settings": universe_settings.model_dump(),
            "exposure_settings": self._exposure_settings.model_dump(),
        }

        response = self._client.post(
            "",
            params=params,
            body=body,
        )

        def _read_df(r: Any) -> pl.DataFrame:
            return pl.read_parquet(io.BytesIO(r.content))

        if response.headers["content-type"] == "application/json":
            df = pl.concat(
                _read_df(self._client.post(page, body=body, absolute_url=True))
                for page in tqdm(response.json()["urls"])
            )
        else:
            df = _read_df(response)

        return df


class AsyncBayeslineAssetExposureApiClient(AsyncAssetExposureApi):

    def __init__(
        self,
        client: AsyncApiClient,
        exposure_settings: ExposureSettings,
        id_types: list[IdType],
        universe_api: AsyncBayeslineEquityUniverseApi,
    ):
        self._client = client
        self._exposure_settings = exposure_settings
        self._id_types = id_types
        self._universe_api = universe_api

    @property
    def settings(self) -> ExposureSettings:
        return self._exposure_settings

    async def dates(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncAssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = await self._client.post(
            "dates",
            params={"range_only": range_only},
            body={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        return [to_date(d) for d in response.json()]

    async def coverage_stats(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["by"] = by

        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncAssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = await self._client.post(
            "/coverage-stats",
            params=params,
            body={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        response.raise_for_status()
        return pl.read_parquet(io.BytesIO(response.content))

    async def get(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)

        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        body = {
            "universe_settings": universe_settings.model_dump(),
            "exposure_settings": self._exposure_settings.model_dump(),
        }

        response = await self._client.post(
            "",
            params=params,
            body=body,
        )

        def _read_df(r: Any) -> pl.DataFrame:
            return pl.read_parquet(io.BytesIO(r.content))

        if response.headers["content-type"] == "application/json":
            tasks = []
            pages = response.json()["urls"]
            results = []
            tasks = [
                self._client.post(page, body=body, absolute_url=True) for page in pages
            ]
            results.extend(await asyncio.gather(*tasks))

            df = pl.concat(_read_df(r) for r in results)
        else:
            df = _read_df(response)

        return df


class BayeslineEquityExposureApiClient(BayeslineEquityExposureApi):

    def __init__(self, client: ApiClient, universe_api: BayeslineEquityUniverseApi):
        self._client = client.append_base_path("exposures")
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/exposure"),
            ExposureSettings,
            ExposureSettingsMenu,
        )
        self._universe_api = universe_api

    @property
    def settings(self) -> SettingsRegistry[ExposureSettings, ExposureSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | ExposureSettings) -> AssetExposureApi:
        id_types = self._universe_api.settings.available_settings().id_types

        if isinstance(ref_or_settings, ExposureSettings):
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return BayeslineAssetExposureApiClient(
                self._client,
                ref_or_settings,
                id_types,
                self._universe_api,
            )
        else:
            exposure_settings = self.settings.get(ref_or_settings)
            return BayeslineAssetExposureApiClient(
                self._client,
                exposure_settings,
                id_types,
                self._universe_api,
            )


class AsyncBayeslineEquityExposureApiClient(AsyncBayeslineEquityExposureApi):

    def __init__(
        self,
        client: AsyncApiClient,
        universe_api: AsyncBayeslineEquityUniverseApi,
    ):
        self._client = client.append_base_path("exposures")
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/exposure"),
            ExposureSettings,
            ExposureSettingsMenu,
        )
        self._universe_api = universe_api

    @property
    def settings(self) -> AsyncSettingsRegistry[ExposureSettings, ExposureSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ExposureSettings
    ) -> AsyncAssetExposureApi:
        id_types = (await self._universe_api.settings.available_settings()).id_types

        if isinstance(ref_or_settings, ExposureSettings):
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return AsyncBayeslineAssetExposureApiClient(
                self._client, ref_or_settings, id_types, self._universe_api
            )
        else:
            exposure_settings = await self.settings.get(ref_or_settings)
            return AsyncBayeslineAssetExposureApiClient(
                self._client,
                exposure_settings,
                id_types,
                self._universe_api,
            )


class FactorRiskModelApiClient(FactorRiskModelApi):

    def __init__(
        self,
        client: ApiClient,
        model_id: int,
        settings: FactorRiskModelSettings,
        asset_exposures: AssetExposureApi,
        asset_universe: AssetUniverseApi,
    ):
        self._client = client
        self._model_id = model_id
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._asset_universe = asset_universe

    def _resolve_id_type(self, id_type: IdType | None) -> IdType:
        if id_type is None:
            universe_settings = self._settings.universe
            if isinstance(universe_settings, (str, int)):
                universe_settings = self._asset_universe.settings
            return universe_settings.id_type
        else:
            return id_type

    def dates(self) -> list[dt.date]:
        response = self._client.get(f"model/{self._model_id}/dates")
        return [to_date(d) for d in response.json()]

    def factors(self, *which: FactorType) -> list[str]:
        response = self._client.get(
            f"model/{self._model_id}/factors",
            params={"which": list(which)},
        )
        return response.json()

    def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        return self._asset_exposures.get(
            self._settings.universe, start=start, end=end, id_type=id_type
        )

    def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        return self._asset_universe.get(start=start, end=end, id_type=id_type)

    def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = self._client.get(
            f"model/{self._model_id}/estimation-universe",
            params={"start": start, "end": end, "id_type": id_type},
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = self._client.get(
            f"model/{self._model_id}/market-caps",
            params={"start": start, "end": end, "id_type": id_type},
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = self._client.get(
            f"model/{self._model_id}/future-asset-returns",
            params={"start": start, "end": end, "id_type": id_type},
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pl.DataFrame:
        response = self._client.get(
            f"model/{self._model_id}/market-stats",
            params={
                "estimation_universe": estimation_universe,
                "industries": industries,
                "regions": regions,
            },
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def t_stats(self) -> pl.DataFrame:
        response = self._client.get(f"model/{self._model_id}/t-stats")
        return pl.read_parquet(io.BytesIO(response.content))

    def p_values(self) -> pl.DataFrame:
        response = self._client.get(f"model/{self._model_id}/p-values")
        return pl.read_parquet(io.BytesIO(response.content))

    def r2(self) -> pl.DataFrame:
        response = self._client.get(f"model/{self._model_id}/r2")
        return pl.read_parquet(io.BytesIO(response.content))

    def sigma2(self) -> pl.DataFrame:
        response = self._client.get(f"model/{self._model_id}/sigma2")
        return pl.read_parquet(io.BytesIO(response.content))

    def style_correlation(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        response = self._client.get(
            f"model/{self._model_id}/style-correlation",
            params=params,
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def industry_exposures(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        response = self._client.get(
            f"model/{self._model_id}/industry-exposures",
            params=params,
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def fcov(
        self,
        start: DateLike | int | None = -1,
        end: DateLike | int | None = None,
        dates: list[DateLike] | None = None,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            if not isinstance(start, int):
                params["start"] = to_date_string(start)
            else:
                params["start"] = start  # type: ignore

        if end is not None:
            if not isinstance(end, int):
                params["end"] = to_date_string(end)
            else:
                params["end"] = end  # type: ignore

        body = {"dates": None}
        if dates is not None:
            body["dates"] = [to_date_string(d) for d in dates]  # type: ignore

        response = self._client.post(
            f"model/{self._model_id}/fcov", params=params, body=body
        )
        return pl.read_parquet(io.BytesIO(response.content))

    def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        if freq is not None:
            params["freq"] = freq
        if cumulative:
            params["cumulative"] = cumulative
        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        response = self._client.get(
            f"model/{self._model_id}/fret",
            params=params,
        )
        return pl.read_parquet(io.BytesIO(response.content))


class AsyncFactorRiskModelApiClient(AsyncFactorRiskModelApi):

    def __init__(
        self,
        client: AsyncApiClient,
        model_id: int,
        settings: FactorRiskModelSettings,
        asset_exposures: AsyncAssetExposureApi,
        asset_universe: AsyncAssetUniverseApi,
    ):
        self._client = client
        self._model_id = model_id
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._asset_universe = asset_universe

    def _resolve_id_type(self, id_type: IdType | None) -> IdType:
        if id_type is None:
            universe_settings = self._settings.universe
            if isinstance(universe_settings, (str, int)):
                universe_settings = self._asset_universe.settings
            return universe_settings.id_type
        else:
            return id_type

    async def dates(self) -> list[dt.date]:
        response = await self._client.get(f"model/{self._model_id}/dates")
        return [to_date(d) for d in response.json()]

    async def factors(self, *which: FactorType) -> list[str]:
        response = await self._client.get(
            f"model/{self._model_id}/factors",
            params={"which": list(which)},
        )
        return response.json()

    async def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        return await self._asset_exposures.get(
            self._settings.universe, start=start, end=end, id_type=id_type
        )

    async def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        return await self._asset_universe.get(start=start, end=end, id_type=id_type)

    async def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = await self._client.get(
            f"model/{self._model_id}/estimation-universe",
            params={"start": start, "end": end, "id_type": id_type},
        )
        return pl.read_parquet(io.BytesIO(response.content))

    async def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = await self._client.get(
            f"model/{self._model_id}/market-caps",
            params={"start": start, "end": end, "id_type": id_type},
        )
        return pl.read_parquet(io.BytesIO(response.content))

    async def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = await self._client.get(
            f"model/{self._model_id}/future-asset-returns",
            params={"start": start, "end": end, "id_type": id_type},
        )
        return pl.read_parquet(io.BytesIO(response.content))

    async def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pl.DataFrame:
        response = await self._client.get(
            f"model/{self._model_id}/market-stats",
            params={
                "estimation_universe": estimation_universe,
                "industries": industries,
                "regions": regions,
            },
        )
        return pl.read_parquet(io.BytesIO(response.content))

    async def t_stats(self) -> pl.DataFrame:
        response = await self._client.get(f"model/{self._model_id}/t-stats")
        return pl.read_parquet(io.BytesIO(response.content))

    async def p_values(self) -> pl.DataFrame:
        response = await self._client.get(f"model/{self._model_id}/p-values")
        return pl.read_parquet(io.BytesIO(response.content))

    async def r2(self) -> pl.DataFrame:
        response = await self._client.get(f"model/{self._model_id}/r2")
        return pl.read_parquet(io.BytesIO(response.content))

    async def sigma2(self) -> pl.DataFrame:
        response = await self._client.get(f"model/{self._model_id}/sigma2")
        return pl.read_parquet(io.BytesIO(response.content))

    async def style_correlation(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        response = await self._client.get(
            f"model/{self._model_id}/style-correlation",
            params=params,
        )
        return pl.read_parquet(io.BytesIO(response.content))

    async def industry_exposures(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        response = await self._client.get(
            f"model/{self._model_id}/industry-exposures",
            params=params,
        )
        return pl.read_parquet(io.BytesIO(response.content))

    async def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pl.DataFrame:
        params: dict[str, Any] = {}
        if freq is not None:
            params["freq"] = freq
        if cumulative:
            params["cumulative"] = cumulative
        if start is not None:
            params["start"] = to_date_string(start)
        if end is not None:
            params["end"] = to_date_string(end)
        response = await self._client.get(
            f"model/{self._model_id}/fret",
            params=params,
        )
        return pl.read_parquet(io.BytesIO(response.content))


class ModelConstructionEngineApiClient(ModelConstructionEngineApi):

    def __init__(
        self,
        client: ApiClient,
        settings: ModelConstructionSettings,
    ):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> ModelConstructionSettings:
        return self._settings


class AsyncModelConstructionEngineApiClient(AsyncModelConstructionEngineApi):

    def __init__(
        self,
        client: AsyncApiClient,
        settings: ModelConstructionSettings,
    ):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> ModelConstructionSettings:
        return self._settings


class FactorRiskEngineApiClient(FactorRiskEngineApi):

    def __init__(
        self,
        client: ApiClient,
        settings: FactorRiskModelSettings,
        asset_exposures: AssetExposureApi,
        asset_universe: AssetUniverseApi,
        model_id: int | None = None,
    ):
        self._client = client
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._asset_universe = asset_universe
        self._model_id = model_id

    @property
    def settings(self) -> FactorRiskModelSettings:
        return self._settings

    def get(self) -> FactorRiskModelApi:
        if self._model_id is None:
            self._model_id = self._client.post(
                "model", body=self._settings.model_dump()
            ).json()

        return FactorRiskModelApiClient(
            self._client,
            self._model_id,
            self._settings,
            self._asset_exposures,
            self._asset_universe,
        )


class AsyncFactorRiskEngineApiClient(AsyncFactorRiskEngineApi):

    def __init__(
        self,
        client: AsyncApiClient,
        settings: FactorRiskModelSettings,
        asset_exposures: AsyncAssetExposureApi,
        asset_universe: AsyncAssetUniverseApi,
        model_id: int | None = None,
    ):
        self._client = client
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._asset_universe = asset_universe
        self._model_id = model_id

    @property
    def settings(self) -> FactorRiskModelSettings:
        return self._settings

    async def get(self) -> AsyncFactorRiskModelApi:
        if self._model_id is None:
            self._model_id = (
                await self._client.post("model", body=self._settings.model_dump())
            ).json()

        return AsyncFactorRiskModelApiClient(
            self._client,
            self._model_id,
            self._settings,
            self._asset_exposures,
            self._asset_universe,
        )


class BayeslineModelConstructionApiClient(BayeslineModelConstructionApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("modelconstruction")
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/model-construction"),
            ModelConstructionSettings,
            ModelConstructionSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> SettingsRegistry[ModelConstructionSettings, ModelConstructionSettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | ModelConstructionSettings
    ) -> ModelConstructionEngineApi:
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(settings)
            return ModelConstructionEngineApiClient(self._client, settings)
        else:
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            return ModelConstructionEngineApiClient(self._client, settings_obj)


class AsyncBayeslineModelConstructionApiClient(AsyncBayeslineModelConstructionApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("modelconstruction")
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/model-construction"),
            ModelConstructionSettings,
            ModelConstructionSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[
        ModelConstructionSettings, ModelConstructionSettingsMenu
    ]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ModelConstructionSettings
    ) -> AsyncModelConstructionEngineApi:
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(settings)
            return AsyncModelConstructionEngineApiClient(self._client, settings)
        else:
            ref = ref_or_settings
            settings_obj = await self.settings.get(ref)
            return AsyncModelConstructionEngineApiClient(self._client, settings_obj)


class BayeslineFactorRiskModelsApiClient(BayeslineFactorRiskModelsApi):

    def __init__(
        self,
        client: ApiClient,
        exposure_api: BayeslineEquityExposureApi,
        universe_api: BayeslineEquityUniverseApi,
    ):
        self._client = client.append_base_path("riskmodels")
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/factor-risk-model"),
            FactorRiskModelSettings,
            FactorRiskModelSettingsMenu,
        )
        self._exposure_api = exposure_api
        self._universe_api = universe_api

    @property
    def settings(
        self,
    ) -> SettingsRegistry[FactorRiskModelSettings, FactorRiskModelSettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | FactorRiskModelSettings
    ) -> FactorRiskEngineApi:
        if isinstance(ref_or_settings, FactorRiskModelSettings):
            settings = ref_or_settings
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(settings)
            asset_exposures = self._exposure_api.load(settings.exposures)
            asset_universe = self._universe_api.load(settings.universe)
            return FactorRiskEngineApiClient(
                self._client, settings, asset_exposures, asset_universe
            )
        else:
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            if isinstance(ref, str):
                model_id = self.settings.names()[ref]
            else:
                model_id = ref
            asset_exposures = self._exposure_api.load(settings_obj.exposures)
            asset_universe = self._universe_api.load(settings_obj.universe)
            return FactorRiskEngineApiClient(
                self._client, settings_obj, asset_exposures, asset_universe, model_id
            )


class AsyncBayeslineFactorRiskModelsApiClient(AsyncBayeslineFactorRiskModelsApi):

    def __init__(
        self,
        client: AsyncApiClient,
        exposure_api: AsyncBayeslineEquityExposureApi,
        universe_api: AsyncBayeslineEquityUniverseApi,
    ):
        self._client = client.append_base_path("riskmodels")
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/factor-risk-model"),
            FactorRiskModelSettings,
            FactorRiskModelSettingsMenu,
        )
        self._exposure_api = exposure_api
        self._universe_api = universe_api

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[FactorRiskModelSettings, FactorRiskModelSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | FactorRiskModelSettings
    ) -> AsyncFactorRiskEngineApi:
        if isinstance(ref_or_settings, FactorRiskModelSettings):
            settings = ref_or_settings
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(settings)
            asset_exposures = await self._exposure_api.load(settings.exposures)
            asset_universe = await self._universe_api.load(settings.universe)
            return AsyncFactorRiskEngineApiClient(
                self._client, settings, asset_exposures, asset_universe
            )
        else:
            ref = ref_or_settings
            settings_obj = await self.settings.get(ref)
            if isinstance(ref, str):
                names = await self.settings.names()
                model_id = names[ref]
            else:
                model_id = ref
            asset_exposures = await self._exposure_api.load(settings_obj.exposures)
            asset_universe = await self._universe_api.load(settings_obj.universe)
            return AsyncFactorRiskEngineApiClient(
                self._client, settings_obj, asset_exposures, asset_universe, model_id
            )


class PortfolioHierarchyApiClient(PortfolioHierarchyApi):

    def __init__(self, client: ApiClient, settings: PortfolioHierarchySettings):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> PortfolioHierarchySettings:
        return self._settings

    def get_id_types(self) -> dict[str, list[IdType]]:
        return self._client.post("id-types", body=self._settings.model_dump()).json()

    def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        response = self._client.post(
            "dates", body=self._settings.model_dump(), params={"collapse": collapse}
        )
        response_data = response.json()
        return {p: [to_date(d) for d in response_data[p]] for p in response_data.keys()}

    def get(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        params = {}
        if start_date is not None:
            params["start_date"] = to_date_string(start_date)
        if end_date is not None:
            params["end_date"] = to_date_string(end_date)
        if id_type is not None:
            params["id_type"] = id_type
        response = self._client.post(
            "/",
            params=params,
            body=self._settings.model_dump(),
        )

        return pl.read_parquet(io.BytesIO(response.content))


class AsyncPortfolioHierarchyApiClient(AsyncPortfolioHierarchyApi):

    def __init__(self, client: AsyncApiClient, settings: PortfolioHierarchySettings):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> PortfolioHierarchySettings:
        return self._settings

    async def get_id_types(self) -> dict[str, list[IdType]]:
        return (
            await self._client.post("id-types", body=self._settings.model_dump())
        ).json()

    async def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        response = await self._client.post(
            "dates", body=self._settings.model_dump(), params={"collapse": collapse}
        )
        response_data = response.json()
        return {p: [to_date(d) for d in response_data[p]] for p in response_data.keys()}

    async def get(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        params = {}
        if start_date is not None:
            params["start_date"] = to_date_string(start_date)
        if end_date is not None:
            params["end_date"] = to_date_string(end_date)
        if id_type is not None:
            params["id_type"] = id_type
        response = await self._client.post(
            "/",
            params=params,
            body=self._settings.model_dump(),
        )

        return pl.read_parquet(io.BytesIO(response.content))


class BayeslinePortfolioHierarchyApiClient(BayeslinePortfolioHierarchyApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("portfoliohierarchy")
        self._settings = HttpSettingsRegistryClient(
            client.append_base_path("settings/portfolio-hierarchy"),
            PortfolioHierarchySettings,
            PortfolioHierarchySettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> SettingsRegistry[PortfolioHierarchySettings, PortfolioHierarchySettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | PortfolioHierarchySettings
    ) -> PortfolioHierarchyApi:
        if isinstance(ref_or_settings, PortfolioHierarchySettings):
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return PortfolioHierarchyApiClient(self._client, ref_or_settings)
        else:
            portfoliohierarchy_settings = self.settings.get(ref_or_settings)
            return PortfolioHierarchyApiClient(
                self._client,
                portfoliohierarchy_settings,
            )


class AsyncBayeslinePortfolioHierarchyApiClient(AsyncBayeslinePortfolioHierarchyApi):
    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("portfoliohierarchy")
        self._settings = AsyncHttpSettingsRegistryClient(
            client.append_base_path("settings/portfolio-hierarchy"),
            PortfolioHierarchySettings,
            PortfolioHierarchySettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[
        PortfolioHierarchySettings, PortfolioHierarchySettingsMenu
    ]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | PortfolioHierarchySettings
    ) -> AsyncPortfolioHierarchyApi:
        if isinstance(ref_or_settings, PortfolioHierarchySettings):
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return AsyncPortfolioHierarchyApiClient(self._client, ref_or_settings)
        else:
            portfoliohierarchy_settings = await self.settings.get(ref_or_settings)
            return AsyncPortfolioHierarchyApiClient(
                self._client,
                portfoliohierarchy_settings,
            )


class BayeslineEquityApiClient(BayeslineEquityApi):
    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("equity")
        self._id_client = BayeslineEquityIdApiClient(self._client)
        self._universe_client = BayeslineEquityUniverseApiClient(self._client)
        self._exposure_client = BayeslineEquityExposureApiClient(
            self._client,
            self._universe_client,
        )
        self._modelconstruction_client = BayeslineModelConstructionApiClient(
            self._client
        )
        self._factorrisk_client = BayeslineFactorRiskModelsApiClient(
            self._client, self._exposure_client, self._universe_client
        )
        self._portfoliohierarchy_client = BayeslinePortfolioHierarchyApiClient(
            self._client
        )
        self._portfolioreport_client = BayeslinePortfolioReportApiClient(
            self._client,
            self._portfoliohierarchy_client,
        )
        self._portfolio_client = BayeslineEquityPortfolioApiClient(self._client)

    @property
    def ids(self) -> BayeslineEquityIdApi:
        return self._id_client

    @property
    def universes(self) -> BayeslineEquityUniverseApi:
        return self._universe_client

    @property
    def exposures(self) -> BayeslineEquityExposureApi:
        return self._exposure_client

    @property
    def modelconstruction(self) -> BayeslineModelConstructionApi:
        return self._modelconstruction_client

    @property
    def riskmodels(self) -> BayeslineFactorRiskModelsApi:
        return self._factorrisk_client

    @property
    def portfolioreport(self) -> BayeslinePortfolioReportApi:
        return self._portfolioreport_client

    @property
    def portfolios(self) -> BayeslineEquityPortfolioApi:
        return self._portfolio_client

    @property
    def portfoliohierarchy(self) -> BayeslinePortfolioHierarchyApi:
        return self._portfoliohierarchy_client


class AsyncBayeslineEquityApiClient(AsyncBayeslineEquityApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("equity")
        self._id_client = AsyncBayeslineEquityIdApiClient(self._client)
        self._universe_client = AsyncBayeslineEquityUniverseApiClient(self._client)

        self._exposure_client = AsyncBayeslineEquityExposureApiClient(
            self._client, self._universe_client
        )
        self._modelconstruction_client = AsyncBayeslineModelConstructionApiClient(
            self._client
        )
        self._factorrisk_client = AsyncBayeslineFactorRiskModelsApiClient(
            self._client, self._exposure_client, self._universe_client
        )
        self._portfoliohierarchy_client = AsyncBayeslinePortfolioHierarchyApiClient(
            self._client
        )
        self._portfolioreport_client = AsyncBayeslinePortfolioReportApiClient(
            self._client,
            self._portfoliohierarchy_client,
        )
        self._portfolio_client = AsyncBayeslineEquityPortfolioApiClient(self._client)

    @property
    def ids(self) -> AsyncBayeslineEquityIdApi:
        return self._id_client

    @property
    def universes(self) -> AsyncBayeslineEquityUniverseApi:
        return self._universe_client

    @property
    def exposures(self) -> AsyncBayeslineEquityExposureApi:
        return self._exposure_client

    @property
    def modelconstruction(self) -> AsyncBayeslineModelConstructionApi:
        return self._modelconstruction_client

    @property
    def riskmodels(self) -> AsyncBayeslineFactorRiskModelsApi:
        return self._factorrisk_client

    @property
    def portfolioreport(self) -> AsyncBayeslinePortfolioReportApi:
        return self._portfolioreport_client

    @property
    def portfolios(self) -> AsyncBayeslineEquityPortfolioApi:
        return self._portfolio_client

    @property
    def portfoliohierarchy(self) -> AsyncBayeslinePortfolioHierarchyApi:
        return self._portfoliohierarchy_client


def _check_and_add_id_type(
    id_types: list[IdType],
    id_type: IdType | None,
    params: dict[str, Any],
) -> None:
    if id_type is not None:
        if id_type not in id_types:
            raise ValueError(f"given id type {id_type} is not supported")
        params["id_type"] = id_type
