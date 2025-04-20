import abc
import datetime as dt
from typing import Literal

import polars as pl

from bayesline.api._src.equity.riskmodels_settings import (
    FactorRiskModelSettings,
    FactorRiskModelSettingsMenu,
)
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi
from bayesline.api._src.types import DateLike, IdType

FactorType = Literal["Market", "Style", "Industry", "Region"]


class FactorRiskModelApi(abc.ABC):

    @abc.abstractmethod
    def dates(self) -> list[dt.date]:
        """
        Returns
        -------
        All dates covered by this risk model.
        """
        pass

    @abc.abstractmethod
    def factors(self, *which: FactorType) -> list[str]:
        """
        Parameters
        ----------
        which: FactorType
            The factor types to return, e.g. `Market`, `Style`, `Industry`, `Region`.
            By default returns all factors.

        Returns
        -------
        list of all factors for the given factor types.
        """
        ...

    @abc.abstractmethod
    def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the risk model exposures for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range with the first two column as the date and
            asset id. The remaining columns are the individual styles.
        """
        ...

    @abc.abstractmethod
    def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the risk model universe for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the first column is the date and the
            remaining columns are the asset ids. The values are the universe inclusion.
        """
        ...

    @abc.abstractmethod
    def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the risk model estimation universe for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the first column is the date and the
            remaining columns are the asset ids. The values are the estimation universe
            inclusion.
        """
        ...

    @abc.abstractmethod
    def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the market caps for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset market caps.
        """
        ...

    @abc.abstractmethod
    def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the asset returns for this risk model on the next day.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset returns.
        """
        ...

    @abc.abstractmethod
    def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pl.DataFrame:
        """
        Parameters
        ----------
        estimation_universe: bool, optional
            If True, returns the market stats for the estimation universe.
        industries: bool, optional
            If True, groups the market by industries.
        regions: bool, optional
            If True, groups the market by regions.

        Returns
        -------
        pl.DataFrame
            Descriptive daily stats for this risk model.
        """
        ...

    @abc.abstractmethod
    def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pl.DataFrame:
        """
        Parameters
        ----------
        freq: str, optional
            The frequency of the return aggregation, e.g. `D` for daily.
            Defaults to daily (i.e. unaggregated)
        cumulative: bool, optional
            If True, returns the cumulative returns.
        start: DateLike, optional
        end: DateLike, optional

        Returns
        -------
        pl.DataFrame
            The factor returns for the given date range.
        """
        ...

    @abc.abstractmethod
    def t_stats(self) -> pl.DataFrame: ...

    @abc.abstractmethod
    def p_values(self) -> pl.DataFrame: ...

    @abc.abstractmethod
    def r2(self) -> pl.DataFrame: ...

    @abc.abstractmethod
    def sigma2(self) -> pl.DataFrame: ...

    @abc.abstractmethod
    def style_correlation(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pl.DataFrame:
        """
        Parameters
        ----------
        start: DateLike, optional
        end: DateLike, optional

        Returns
        -------
        pl.DataFrame
            The style correlation matrix for the given date range.
        """
        ...

    @abc.abstractmethod
    def industry_exposures(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pl.DataFrame:
        """
        Parameters
        ----------
        start: DateLike, optional
        end: DateLike, optional

        Returns
        -------
        pl.DataFrame
            The average style exposures grouped by industry.
        """
        ...


class AsyncFactorRiskModelApi(abc.ABC):

    @abc.abstractmethod
    async def dates(self) -> list[dt.date]:
        """
        Returns
        -------
        All dates covered by this risk model.
        """
        pass

    @abc.abstractmethod
    async def factors(self, *which: FactorType) -> list[str]:
        """
        Parameters
        ----------
        which: FactorType
            The factor types to return, e.g. `Market`, `Style`, `Industry`, `Region`.
            By default returns all factors.

        Returns
        -------
        list of all factors for the given factor types.
        """
        ...

    @abc.abstractmethod
    async def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the risk model exposures for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the universe to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range with the first two column as the date and
            asset id. The remaining columns are the individual styles.
        """
        ...

    @abc.abstractmethod
    async def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the risk model universe for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the first column is the date and the
            remaining columns are the asset ids. The values are the universe inclusion.
        """
        ...

    @abc.abstractmethod
    async def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the risk model estimation universe for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the first column is the date and the
            remaining columns are the asset ids. The values are the estimation universe
            inclusion.
        """
        ...

    @abc.abstractmethod
    async def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the market caps for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset market caps.
        """
        ...

    @abc.abstractmethod
    async def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pl.DataFrame:
        """
        Obtains the asset returns for this risk model on the next day.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pl.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset returns.
        """
        ...

    @abc.abstractmethod
    async def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pl.DataFrame:
        """
        Parameters
        ----------
        estimation_universe: bool, optional
            If True, returns the market stats for the estimation universe.
        industries: bool, optional
            If True, groups the market by industries.
        regions: bool, optional
            If True, groups the market by regions.

        Returns
        -------
        pl.DataFrame
            Descriptive daily stats for this risk model.
        """
        ...

    @abc.abstractmethod
    async def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pl.DataFrame:
        """
        Parameters
        ----------
        freq: str, optional
            The frequency of the return aggregation, e.g. `D` for daily.
            Defaults to daily (i.e. unaggregated)
        cumulative: bool, optional
            If True, returns the cumulative returns.
        start: DateLike, optional
        end: DateLike, optional

        Returns
        -------
        pl.DataFrame
            The factor returns for the given date range.
        """
        ...

    @abc.abstractmethod
    async def t_stats(self) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def p_values(self) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def r2(self) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def sigma2(self) -> pl.DataFrame: ...


class FactorRiskEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> FactorRiskModelSettings:
        """
        Returns
        -------
        The settings used to create these risk model.
        """
        ...

    @abc.abstractmethod
    def get(self) -> FactorRiskModelApi:
        """

        Returns
        -------
        A built `FactorRiskModelApi` instance for given settings.
        """


class AsyncFactorRiskEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> FactorRiskModelSettings:
        """
        Returns
        -------
        The settings used to create these risk model.
        """
        ...

    @abc.abstractmethod
    async def get(self) -> AsyncFactorRiskModelApi:
        """

        Returns
        -------
        A built `FactorRiskModelApi` instance for given settings.
        """


class BayeslineFactorRiskModelsApi(
    RegistryBasedApi[
        FactorRiskModelSettings, FactorRiskModelSettingsMenu, FactorRiskEngineApi
    ]
): ...


class AsyncBayeslineFactorRiskModelsApi(
    AsyncRegistryBasedApi[
        FactorRiskModelSettings, FactorRiskModelSettingsMenu, AsyncFactorRiskEngineApi
    ]
): ...
