from typing import List

from domain.entities.alert import AlertEntity
from domain.exceptions import NotFound
from domain.repositories.alert import AlertRepository
from infrastructure.repositories.clients.sqlite.base import Session
from infrastructure.repositories.clients.sqlite.models.alert import Alert


class AlertSQLiteRepository(AlertRepository):
    def get_all(self, page_number: int = 1, page_size: int = 30) -> List[AlertEntity]:
        with Session() as session:
            alerts = (
                session.query(Alert)
                .order_by(Alert.created_at.desc())
                .limit(page_size)
                .offset((page_number - 1) * page_size)
                .all()
            )
            return [alert.to_entity() for alert in alerts]

    def get(self, alert_id: str) -> AlertEntity:
        with Session() as session:
            alert = session.query(Alert).filter(Alert.id == alert_id).first()
            if not alert:
                raise NotFound(f"Alert with id {alert_id}")
            return alert.to_entity()

    def filter_by(
        self,
        interaction_id: int = None,
        interaction_type: str = None,
        alert_type: str = None,
        page_number: int = 1,
        page_size: int = 30,
    ) -> List[AlertEntity]:
        with Session() as session:
            query = session.query(Alert)
            if interaction_id:
                query = query.filter(Alert.interaction_id == interaction_id)
            if interaction_type:
                query = query.filter(Alert.interaction_type == interaction_type)
            if alert_type:
                query = query.filter(Alert.alert_type == alert_type)
            alerts = (
                query.order_by(Alert.created_at.desc())
                .limit(page_size)
                .offset((page_number - 1) * page_size)
                .all()
            )
            return [alert.to_entity() for alert in alerts]

    def create(self, alert: AlertEntity) -> AlertEntity:
        with Session() as session:
            alert_model = Alert(
                id=alert.id,
                alert_type=alert.alert_type,
                interaction_id=alert.interaction_id,
                interaction_type=alert.interaction_type,
                value=alert.value,
            )
            session.add(alert_model)
            session.commit()
            return alert_model.to_entity()

    def batch_create(self, alerts: List[AlertEntity]) -> List[AlertEntity]:
        if not alerts:
            return []

        with Session() as session:
            alert_models = [
                Alert(
                    id=alert.id,
                    alert_type=alert.alert_type,
                    interaction_id=alert.interaction_id,
                    interaction_type=alert.interaction_type,
                    value=alert.value,
                )
                for alert in alerts
            ]
            session.add_all(alert_models)
            session.commit()
            return [alert.to_entity() for alert in alert_models]

    def update(self, alert: AlertEntity) -> AlertEntity:
        with Session() as session:
            alert_model = session.query(Alert).filter(Alert.id == alert.id).first()
            if not alert_model:
                raise NotFound(f"Alert with id {alert.id}")
            alert_model.alert_type = alert.alert_type
            alert_model.interaction_id = alert.interaction_id
            alert_model.interaction_type = alert.interaction_type
            alert_model.value = alert.value
            session.commit()
            return alert_model.to_entity()

    def delete(self, alert_id: str) -> AlertEntity:
        with Session() as session:
            alert = session.query(Alert).filter(Alert.id == alert_id).first()
            if not alert:
                raise NotFound(f"Alert with id {alert_id}")
            session.delete(alert)
            session.commit()
            return alert.to_entity()
