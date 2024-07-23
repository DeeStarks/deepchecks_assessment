import csv
import os

from dependency_injector.wiring import Provide, inject

from application.services.alert import OutlierAlertChecker, ThresholdAlertChecker
from application.services.metric import LengthMetricCalculator
from domain.entities.alert import AlertFactory, AlertType
from domain.entities.interaction import InteractionFactory, InteractionType
from domain.entities.metric import MetricFactory
from domain.events.interaction import LogInteractionEvent
from domain.events.runners.detached import DetachedRunner
from domain.repositories.alert import AlertRepository
from domain.repositories.interaction import InteractionRepository
from domain.repositories.metric import MetricRepository
from infrastructure.container import Container


class LogInteractionQueueEvent(LogInteractionEvent):
    def send(self, runner: DetachedRunner, filename: str) -> bool:
        # runner.run is a method that runs a function in a separate thread.
        # with the _send method, which contains the logic for logging interactions,
        # we can have the runner run it in a separate thread.
        return runner.run(
            "infrastructure.events.interaction." + self._send.__qualname__, filename
        )

    @staticmethod
    @inject
    def _send(
        filename: str,
        length_metric: LengthMetricCalculator = Provide[
            Container.length_metric_calculator
        ],
        threshold_alert: ThresholdAlertChecker = Provide[
            Container.threshold_alert_checker
        ],
        outlier_alert: OutlierAlertChecker = Provide[Container.outlier_alert_checker],
        alert_factory: AlertFactory = Provide[Container.alert_factory],
        alert_repository: AlertRepository = Provide[Container.alert_repository],
        metric_factory: MetricFactory = Provide[Container.metric_factory],
        metric_repository: MetricRepository = Provide[Container.metric_repository],
        interaction_factory: InteractionFactory = Provide[
            Container.interaction_factory
        ],
        interaction_repository: InteractionRepository = Provide[
            Container.interaction_repository
        ],
    ):
        with open(filename, "r") as f:
            reader = csv.reader(f)

            # ignore the header and get the indexes of the "Input" and "Output" columns
            header = next(reader, None)
            input_index = header.index("Input")
            output_index = header.index("Output")

            # retriving previous metrics to check for alerts
            input_metrics = [m.input_value for m in metric_repository.get_all()]
            output_metrics = [m.output_value for m in metric_repository.get_all()]

            for line in reader:
                # save the interaction
                interaction = interaction_factory.create(
                    input_text=line[input_index], output_text=line[output_index]
                )
                interaction_repository.create(interaction)

                # save the metric values for the interaction
                input_metric_value = length_metric.calculate(interaction.input_text)
                output_metric_value = length_metric.calculate(interaction.output_text)
                metric = metric_factory.create(
                    metric_name="length",
                    interaction_id=interaction.id,
                    input_value=input_metric_value,
                    output_value=output_metric_value,
                )
                metric_repository.create(metric)
                input_metrics.append(input_metric_value)
                output_metrics.append(output_metric_value)

                # check for alerts
                alerts = []
                outlier_alert.prev_inputs = input_metrics
                outlier_alert.prev_outputs = output_metrics

                for value, element in [
                    (input_metric_value, InteractionType.INPUT),
                    (output_metric_value, InteractionType.OUTPUT),
                ]:
                    if threshold_alert.check(value):
                        alert = alert_factory.create(
                            alert_type=AlertType.THRESHOLD,
                            interaction_id=interaction.id,
                            interaction_type=element,
                            value=value,
                        )
                        alerts.append(alert)
                    if outlier_alert.check(value, element):
                        alert = alert_factory.create(
                            alert_type=AlertType.OUTLIER,
                            interaction_id=interaction.id,
                            interaction_type=element,
                            value=value,
                        )
                        alerts.append(alert)

                alert_repository.batch_create(alerts)

        # delete the file after processing
        os.remove(filename)

        return True
