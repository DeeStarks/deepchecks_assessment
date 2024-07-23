import uuid

from datetime import datetime
from enum import Enum


class InteractionType(str, Enum):
    INPUT = 'input'
    OUTPUT = 'output'


class InteractionEntity:
    def __init__(
        self,
        interaction_id: str,
        input_text: str,
        output_text: str,
        created_at: datetime = None
    ):
        self.id = interaction_id
        self.input_text = input_text
        self.output_text = output_text
        self.created_at = created_at

    def to_dict(self):
        return {
            'interaction_id': self.id,
            'input_text': self.input_text,
            'output_text': self.output_text,
            'created_at': self.created_at
        }


class InteractionFactory:
    @staticmethod
    def create(input_text: str, output_text: str) -> InteractionEntity:
        return InteractionEntity(
            interaction_id=uuid.uuid4().__str__(),
            input_text=input_text,
            output_text=output_text
        )
