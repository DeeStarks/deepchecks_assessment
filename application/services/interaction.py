from domain.entities.interaction import InteractionEntity
from domain.events.interaction import LogInteractionEvent
from domain.events.runners.detached import DetachedRunner
from domain.repositories.interaction import InteractionRepository
from domain.usecases.interaction import InteractionUsecase


class InteractionService(InteractionUsecase):
    def __init__(
        self,
        repository: InteractionRepository,
        event: LogInteractionEvent,
        event_runner: DetachedRunner,
    ):
        super().__init__(repository, event, event_runner)

    def all_interactions(
        self, page_number: int, page_size: int
    ) -> list[InteractionEntity]:
        return self.repository.get_all(page_number, page_size)

    def get_interaction(self, interaction_id: str) -> InteractionEntity:
        return self.repository.get(interaction_id)

    def create_interaction(self, interaction: InteractionEntity) -> InteractionEntity:
        return self.repository.create(interaction)

    def batch_create_interactions(
        self, interactions: list[InteractionEntity]
    ) -> list[InteractionEntity]:
        return self.repository.batch_create(interactions)

    def create_interactions_from_file(self, file_path: str) -> list[InteractionEntity]:
        return self.event.send(self.event_runner, file_path)

    def update_interaction(self, interaction: InteractionEntity) -> InteractionEntity:
        return self.repository.update(interaction)

    def delete_interaction(self, interaction_id: str) -> InteractionEntity:
        return self.repository.delete(interaction_id)
