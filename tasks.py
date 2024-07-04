import csv

from negotium import Negotium
from negotium.brokers import Redis

from config import get_settings
from alerts import threshold_alert, outlier_alert
from metrics import length_metric_calculator
from models import AlertType, Interaction, InteractionType, Metric, Alert, session


settings = get_settings()

# Start the Negotium service to listen for tasks
negotium = Negotium("deepchecks", Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    user=settings.redis_user,
    password=settings.redis_password,
))
negotium.start()


@negotium.task
def log_interaction_from_file(contents: str):
    interactions_logged = 0
    alerts_raised = 0

    reader = csv.DictReader(contents.splitlines())

    for interaction in reader:
        interaction = Interaction(
            input_text=interaction["Input"],
            output_text=interaction["Output"]
        )
        session.add(interaction)
        session.commit()

        input_metric_value = length_metric_calculator.calculate(interaction.input_text)
        output_metric_value = length_metric_calculator.calculate(interaction.output_text)
        metric = Metric(
            interaction_id=interaction.id,
            metric_name='length',
            input_metric_value=input_metric_value,
            output_metric_value=output_metric_value
        )
        session.add(metric)
        session.commit()

        interactions_logged += 1

        outlier_alert.input_values.append(input_metric_value)
        outlier_alert.output_values.append(output_metric_value)

        if threshold_alert.check(input_metric_value):
            alert = Alert(
                interaction_id=interaction.id,
                alert_type=AlertType.THRESHOLD,
                element=InteractionType.INPUT,
                value=input_metric_value
            )
            session.add(alert)
            alerts_raised += 1
        if threshold_alert.check(output_metric_value):
            alert = Alert(
                interaction_id=interaction.id,
                alert_type=AlertType.THRESHOLD,
                element=InteractionType.OUTPUT,
                value=output_metric_value
            )
            session.add(alert)
            alerts_raised += 1
        if outlier_alert.check(input_metric_value, InteractionType.INPUT):
            alert = Alert(
                interaction_id=interaction.id,
                alert_type=AlertType.OUTLIER,
                element=InteractionType.INPUT,
                value=input_metric_value
            )
            session.add(alert)
            alerts_raised += 1
        if outlier_alert.check(output_metric_value, InteractionType.OUTPUT):
            alert = Alert(
                interaction_id=interaction.id,
                alert_type=AlertType.OUTLIER,
                element=InteractionType.OUTPUT,
                value=output_metric_value
            )
            session.add(alert)
            alerts_raised += 1

    session.commit()
    return "Logged {} interactions with {} alerts".format(
        interactions_logged,
        alerts_raised
    )
