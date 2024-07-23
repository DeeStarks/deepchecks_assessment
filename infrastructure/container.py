from itertools import chain

from dependency_injector import containers, providers

from application.services.alert import (
    AlertService,
    OutlierAlertChecker,
    ThresholdAlertChecker,
)
from application.services.interaction import InteractionService
from application.services.metric import LengthMetricCalculator, MetricService
from config import settings
from domain.entities.alert import AlertFactory
from domain.entities.interaction import InteractionFactory
from domain.entities.metric import MetricFactory
from infrastructure.events import Events
from infrastructure.events.runners.negotium import NegotiumDetachedRunner
from infrastructure.handlers import Handlers
from infrastructure.repositories.alert import AlertSQLiteRepository
from infrastructure.repositories.interaction import InteractionSQLiteRepository
from infrastructure.repositories.metric import MetricSQLiteRepository


class Container(containers.DeclarativeContainer):
    # loads all modules using the @inject decorator
    wiring_config = containers.WiringConfiguration(
        modules=chain(Events.modules(), Handlers.modules())
    )

    # factories
    alert_factory = providers.Factory(AlertFactory)
    interaction_factory = providers.Factory(InteractionFactory)
    metric_factory = providers.Factory(MetricFactory)

    # repositories
    alert_repository = providers.Singleton(AlertSQLiteRepository)
    interaction_repository = providers.Singleton(InteractionSQLiteRepository)
    metric_repository = providers.Singleton(MetricSQLiteRepository)

    # event runners
    detached_runner = providers.Singleton(NegotiumDetachedRunner)

    # events
    log_interaction_queue_event = providers.Singleton(Events.log_interaction_queue)

    # services
    alert_service = providers.Factory(AlertService, repository=alert_repository)
    outlier_alert_checker = providers.Singleton(OutlierAlertChecker)
    threshold_alert_checker = providers.Singleton(
        ThresholdAlertChecker, high=settings.high_threshold, low=settings.low_threshold
    )

    interaction_service = providers.Factory(
        InteractionService,
        repository=interaction_repository,
        event=log_interaction_queue_event,
        event_runner=detached_runner,
    )

    metric_service = providers.Factory(MetricService, repository=metric_repository)
    length_metric_calculator = providers.Singleton(LengthMetricCalculator)
