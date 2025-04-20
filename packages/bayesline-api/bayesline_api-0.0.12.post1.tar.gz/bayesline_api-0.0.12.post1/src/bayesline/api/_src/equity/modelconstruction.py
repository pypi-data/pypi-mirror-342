import abc

from bayesline.api._src.equity.modelconstruction_settings import (
    ModelConstructionSettings,
    ModelConstructionSettingsMenu,
)
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi


class ModelConstructionEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ModelConstructionSettings:
        """
        Returns
        -------
        The modelconstruction settings.
        """
        ...


class AsyncModelConstructionEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ModelConstructionSettings:
        """
        Returns
        -------
        The modelconstruction settings.
        """
        ...


class BayeslineModelConstructionApi(
    RegistryBasedApi[
        ModelConstructionSettings,
        ModelConstructionSettingsMenu,
        ModelConstructionEngineApi,
    ],
): ...


class AsyncBayeslineModelConstructionApi(
    AsyncRegistryBasedApi[
        ModelConstructionSettings,
        ModelConstructionSettingsMenu,
        AsyncModelConstructionEngineApi,
    ],
): ...
