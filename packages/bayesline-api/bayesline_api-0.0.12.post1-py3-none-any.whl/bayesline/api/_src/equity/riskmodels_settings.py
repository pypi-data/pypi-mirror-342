import os
from typing import Annotated

from pydantic import Field

from bayesline.api._src.equity.exposure_settings import ExposureSettings
from bayesline.api._src.equity.modelconstruction_settings import (
    ModelConstructionSettings,
)
from bayesline.api._src.equity.universe_settings import UniverseSettings
from bayesline.api._src.registry import Settings, SettingsMenu, SettingsTypeMetaData


class FactorRiskModelSettings(Settings):
    """
    Defines all settings needed to build a factor risk model.
    """

    @classmethod
    def default(cls) -> "FactorRiskModelSettings":
        return cls(
            universe=UniverseSettings.default(),
            exposures=ExposureSettings.default(),
            modelconstruction=ModelConstructionSettings.default(),
        )

    universe: Annotated[
        str | int | UniverseSettings,
        Field(
            description="The universe to build the factor risk model on.",
            default_factory=UniverseSettings.default,
        ),
        SettingsTypeMetaData[str | int | UniverseSettings](references=UniverseSettings),
    ]

    exposures: Annotated[
        str | int | ExposureSettings,
        Field(
            description="The exposures to build the factor risk model on.",
            default_factory=ExposureSettings.default,
        ),
        SettingsTypeMetaData[str | int | ExposureSettings](references=ExposureSettings),
    ]

    modelconstruction: Annotated[
        str | int | ModelConstructionSettings,
        Field(
            description="The model construction settings to use for the factor risk model.",
            default_factory=ModelConstructionSettings.default,
        ),
        SettingsTypeMetaData[str | int | ModelConstructionSettings](
            references=ModelConstructionSettings
        ),
    ]


class FactorRiskModelSettingsMenu(SettingsMenu, frozen=True, extra="forbid"):
    """
    Defines available settings to build a factor risk model.
    """

    def describe(self, settings: FactorRiskModelSettings | None = None) -> str:
        if settings:
            result = [
                "Universe: " + str(settings.universe),
                "Exposures: " + str(settings.exposures),
                "Model Construction: " + str(settings.modelconstruction),
            ]
            return os.linesep.join(result)
        else:
            return "This settings menu has no description."

    def validate_settings(self, settings: FactorRiskModelSettings) -> None:
        if not isinstance(settings.exposures, ExposureSettings) or not isinstance(
            settings.modelconstruction, ModelConstructionSettings
        ):
            return

        known_factors = set(settings.modelconstruction.known_factors)
        other_factors = set(settings.exposures.other)
        missing_known_exposures = known_factors - other_factors
        if missing_known_exposures:
            raise ValueError(
                f"Invalid known factor returns: {', '.join(missing_known_exposures)}"
            )
