import abc
import datetime as dt
import os
from functools import cached_property
from logging import getLogger

import polars as pl

from bayesline.api._src.equity.portfoliohierarchy_settings import (
    PortfolioHierarchySettings,
)
from bayesline.api._src.equity.report_settings import (
    PortfolioReportAccessorSettings,
    ReportSettings,
    ReportSettingsMenu,
)
from bayesline.api._src.registry import (
    AsyncReadOnlyRegistry,
    AsyncRegistryBasedApi,
    ReadOnlyRegistry,
    RegistryBasedApi,
)
from bayesline.api._src.types import DateLike, DNFFilterExpressions

logger = getLogger(__name__)


class IllegalPathError(Exception):
    pass


class BasePortfolioReportAccessor(abc.ABC):

    @property
    @abc.abstractmethod
    def axes(self) -> dict[str, list[str]]: ...

    @property
    @abc.abstractmethod
    def metric_cols(self) -> list[str]: ...

    @property
    @abc.abstractmethod
    def pivot_cols(self) -> list[str]: ...

    @cached_property
    def axis_lookup(self) -> dict[str, str]:
        return {
            level: dimension
            for dimension, levels in self.axes.items()
            for level in levels
        }

    def is_path_valid(
        self,
        path_levels: list[str],
        *,
        expand: tuple[str, ...] = (),
    ) -> bool:
        try:
            self.validate_path(path_levels, expand)
            return True
        except AssertionError:
            return False

    def _validate_path(self, path_levels: list[str]) -> list[str]:
        msgs = []
        unknown_levels = [
            level for level in path_levels if level not in self.axis_lookup
        ]
        if unknown_levels:
            msgs.append(f"Unknown levels: {unknown_levels}")

        seen_axes = set()
        prev_axis = ""
        for level in path_levels:
            axis = self.axis_lookup.get(level)
            if not axis:
                msgs.append(f"Level {level} does not exist")
                break

            if axis != prev_axis and axis in seen_axes:
                msgs.append(
                    "Mixed axis groups: "
                    f"{', '.join([self.axis_lookup[level] for level in path_levels])}",
                )
                break

            seen_axes.add(axis)
            prev_axis = axis

        # check that for each dimension the levels are in the right order
        for dimension, levels in self.axes.items():
            path_levels_for_dimension = [
                level for level in path_levels if self.axis_lookup[level] == dimension
            ]
            correct_order = [
                level for level in levels if level in path_levels_for_dimension
            ]
            if path_levels_for_dimension != correct_order:
                msgs.append(
                    f"Invalid order for {dimension}: "
                    f"{', '.join(path_levels_for_dimension)} "
                    f"should be in {', '.join(correct_order)}",
                )

        return msgs

    def validate_path(
        self,
        path_levels: list[str],
        expand: tuple[str, ...] = (),
    ) -> None:
        self._validate_path(path_levels)
        msgs = []
        seen = set()
        for e in expand:
            if e in seen:
                msgs.append(f"Duplicate expand: {e}")
            msgs.extend(self._validate_path([*path_levels, e]))
            seen.add(e)

        if msgs:
            raise IllegalPathError(os.linesep.join(msgs))


class PortfolioReportAccessor(BasePortfolioReportAccessor):

    @abc.abstractmethod
    def get_level_values(
        self,
        levels: tuple[str, ...] = (),
        include_totals: bool = False,
        filters: DNFFilterExpressions | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    def get_data(
        self,
        path: list[tuple[str, str]],
        *,
        expand: tuple[str, ...] = (),
        pivot_cols: tuple[str, ...] = (),
        value_cols: tuple[str, ...] = (),
        filters: DNFFilterExpressions | None = None,
        pivot_total: bool = False,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    def persist(self, name: str) -> int:
        """
        Persists the given report for the given name.

        Parameters
        ----------
        name : str
            The name to persist the report under. Will throw if the name already exists.

        Returns
        -------
        int
            A globally unique identifier of the persisted report.
        """


class AsyncPortfolioReportAccessor(BasePortfolioReportAccessor):

    @abc.abstractmethod
    async def get_level_values(
        self,
        levels: tuple[str, ...] = (),
        include_totals: bool = False,
        filters: DNFFilterExpressions | None = None,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def get_data(
        self,
        path: list[tuple[str, str]],
        *,
        expand: tuple[str, ...] = (),
        pivot_cols: tuple[str, ...] = (),
        value_cols: tuple[str, ...] = (),
        filters: DNFFilterExpressions | None = None,
        pivot_total: bool = False,
    ) -> pl.DataFrame: ...

    @abc.abstractmethod
    async def persist(self, name: str) -> int:
        """
        Persists the given report for the given name.

        Parameters
        ----------
        name : str
            The name to persist the report under. Will throw if the name already exists.

        Returns
        -------
        int
            A globally unique identifier of the persisted report.
        """


class ReportPersister(abc.ABC):

    @abc.abstractmethod
    def persist(
        self,
        name: str,
        settings: PortfolioReportAccessorSettings,
        accessors: list[PortfolioReportAccessor],
    ) -> int: ...

    @abc.abstractmethod
    def load_persisted(self, name_or_id: str | int) -> AsyncPortfolioReportAccessor: ...

    @abc.abstractmethod
    def delete_persisted(self, name_or_id: list[str | int]) -> None: ...


class AsyncReportPersister(abc.ABC):

    @abc.abstractmethod
    async def persist(
        self,
        name: str,
        settings: PortfolioReportAccessorSettings,
        accessors: list[AsyncPortfolioReportAccessor],
    ) -> int: ...

    @abc.abstractmethod
    async def load_persisted(
        self, name_or_id: str | int
    ) -> AsyncPortfolioReportAccessor: ...

    @abc.abstractmethod
    async def delete_persisted(self, name_or_id: list[str | int]) -> None: ...


class PortfolioReportApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ReportSettings:
        """
        Returns
        -------
        The settings used to create this report.
        """
        ...

    @abc.abstractmethod
    def dates(self) -> list[dt.date]: ...

    @abc.abstractmethod
    def get_report(
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
    ) -> PortfolioReportAccessor: ...


class AsyncPortfolioReportApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ReportSettings:
        """
        Returns
        -------
        The settings used to create this report.
        """
        ...

    @abc.abstractmethod
    async def dates(self) -> list[dt.date]: ...

    @abc.abstractmethod
    async def get_report(
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
    ) -> AsyncPortfolioReportAccessor: ...


class BayeslinePortfolioReportApi(
    RegistryBasedApi[ReportSettings, ReportSettingsMenu, PortfolioReportApi],
):

    @abc.abstractmethod
    def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
    ) -> PortfolioReportApi: ...

    @property
    @abc.abstractmethod
    def persisted_report_settings(
        self,
    ) -> ReadOnlyRegistry[PortfolioReportAccessorSettings]: ...

    @abc.abstractmethod
    def load_persisted(self, name_or_id: str | int) -> PortfolioReportAccessor: ...

    @abc.abstractmethod
    def delete_persisted(self, name_or_id: list[str | int]) -> None: ...


class AsyncBayeslinePortfolioReportApi(
    AsyncRegistryBasedApi[ReportSettings, ReportSettingsMenu, AsyncPortfolioReportApi],
):

    @abc.abstractmethod
    async def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
    ) -> AsyncPortfolioReportApi: ...

    @property
    @abc.abstractmethod
    def persisted_report_settings(
        self,
    ) -> AsyncReadOnlyRegistry[PortfolioReportAccessorSettings]: ...

    @abc.abstractmethod
    async def load_persisted(
        self, name_or_id: str | int
    ) -> AsyncPortfolioReportAccessor: ...

    @abc.abstractmethod
    async def delete_persisted(self, name_or_id: list[str | int]) -> None: ...
