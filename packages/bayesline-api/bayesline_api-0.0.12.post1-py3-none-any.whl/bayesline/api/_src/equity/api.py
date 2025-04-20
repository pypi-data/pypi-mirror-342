import abc

from bayesline.api._src.equity.exposure import (
    AsyncBayeslineEquityExposureApi,
    BayeslineEquityExposureApi,
)
from bayesline.api._src.equity.ids import (
    AsyncBayeslineEquityIdApi,
    BayeslineEquityIdApi,
)
from bayesline.api._src.equity.modelconstruction import (
    AsyncBayeslineModelConstructionApi,
    BayeslineModelConstructionApi,
)
from bayesline.api._src.equity.portfolio import (
    AsyncBayeslineEquityPortfolioApi,
    BayeslineEquityPortfolioApi,
)
from bayesline.api._src.equity.portfoliohierarchy import (
    AsyncBayeslinePortfolioHierarchyApi,
    BayeslinePortfolioHierarchyApi,
)
from bayesline.api._src.equity.portfolioreport import (
    AsyncBayeslinePortfolioReportApi,
    BayeslinePortfolioReportApi,
)
from bayesline.api._src.equity.riskmodels import (
    AsyncBayeslineFactorRiskModelsApi,
    BayeslineFactorRiskModelsApi,
)
from bayesline.api._src.equity.universe import (
    AsyncBayeslineEquityUniverseApi,
    BayeslineEquityUniverseApi,
)


class BayeslineEquityApi(abc.ABC):

    @property
    @abc.abstractmethod
    def ids(self) -> BayeslineEquityIdApi: ...

    @property
    @abc.abstractmethod
    def universes(self) -> BayeslineEquityUniverseApi: ...

    @property
    @abc.abstractmethod
    def exposures(self) -> BayeslineEquityExposureApi: ...

    @property
    @abc.abstractmethod
    def modelconstruction(self) -> BayeslineModelConstructionApi: ...

    @property
    @abc.abstractmethod
    def riskmodels(self) -> BayeslineFactorRiskModelsApi: ...

    @property
    @abc.abstractmethod
    def portfoliohierarchy(self) -> BayeslinePortfolioHierarchyApi: ...

    @property
    @abc.abstractmethod
    def portfolioreport(self) -> BayeslinePortfolioReportApi: ...

    @property
    @abc.abstractmethod
    def portfolios(self) -> BayeslineEquityPortfolioApi: ...


class AsyncBayeslineEquityApi(abc.ABC):

    @property
    @abc.abstractmethod
    def ids(self) -> AsyncBayeslineEquityIdApi: ...

    @property
    @abc.abstractmethod
    def universes(self) -> AsyncBayeslineEquityUniverseApi: ...

    @property
    @abc.abstractmethod
    def exposures(self) -> AsyncBayeslineEquityExposureApi: ...

    @property
    @abc.abstractmethod
    def modelconstruction(self) -> AsyncBayeslineModelConstructionApi: ...

    @property
    @abc.abstractmethod
    def riskmodels(self) -> AsyncBayeslineFactorRiskModelsApi: ...

    @property
    @abc.abstractmethod
    def portfoliohierarchy(self) -> AsyncBayeslinePortfolioHierarchyApi: ...

    @property
    @abc.abstractmethod
    def portfolioreport(self) -> AsyncBayeslinePortfolioReportApi: ...

    @property
    @abc.abstractmethod
    def portfolios(self) -> AsyncBayeslineEquityPortfolioApi: ...
