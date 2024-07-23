from typing import List

from domain.entities.interaction import InteractionEntity
from domain.exceptions import NotFound
from domain.repositories.interaction import InteractionRepository
from infrastructure.repositories.clients.sqlite.base import Session
from infrastructure.repositories.clients.sqlite.models.interaction import Interaction


class InteractionSQLiteRepository(InteractionRepository):
    def get_all(
        self, page_number: int = 1, page_size: int = 30
    ) -> List[InteractionEntity]:
        with Session() as session:
            interactions = (
                session.query(Interaction)
                .order_by(Interaction.created_at.desc())
                .limit(page_size)
                .offset((page_number - 1) * page_size)
                .all()
            )
            return [interaction.to_entity() for interaction in interactions]

    def get(self, interaction_id: str) -> InteractionEntity:
        with Session() as session:
            interaction = (
                session.query(Interaction)
                .filter(Interaction.id == interaction_id)
                .first()
            )
            if not interaction:
                raise NotFound(f"Interaction with id {interaction_id}")
            return interaction.to_entity()

    def create(self, interaction: InteractionEntity) -> InteractionEntity:
        with Session() as session:
            interaction_model = Interaction(
                id=interaction.id,
                input_text=interaction.input_text,
                output_text=interaction.output_text,
            )
            session.add(interaction_model)
            session.commit()
            return interaction_model.to_entity()

    def batch_create(
        self, interactions: List[InteractionEntity]
    ) -> List[InteractionEntity]:
        if not interactions:
            return []

        with Session() as session:
            interaction_models = [
                Interaction(
                    id=interaction.id,
                    input_text=interaction.input_text,
                    output_text=interaction.output_text,
                )
                for interaction in interactions
            ]
            session.add_all(interaction_models)
            session.commit()
            return [interaction.to_entity() for interaction in interaction_models]

    def update(self, interaction: InteractionEntity) -> InteractionEntity:
        with Session() as session:
            interaction_model = (
                session.query(Interaction)
                .filter(Interaction.id == interaction.id)
                .first()
            )
            if not interaction_model:
                raise NotFound(f"Interaction with id {interaction.id}")
            interaction_model.input_text = interaction.input_text
            interaction_model.output_text = interaction.output_text
            session.commit()
            return interaction_model.to_entity()

    def delete(self, interaction_id: str) -> InteractionEntity:
        with Session() as session:
            interaction = (
                session.query(Interaction)
                .filter(Interaction.id == interaction_id)
                .first()
            )
            if not interaction:
                raise NotFound(f"Interaction with id {interaction_id}")
            session.delete(interaction)
            session.commit()
            return interaction.to_entity()
