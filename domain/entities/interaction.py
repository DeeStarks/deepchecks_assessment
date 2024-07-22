import uuid

from enum import Enum


class InteractionType(str, Enum):
    INPUT = 'input'
    OUTPUT = 'output'


class InteractionEntity:
    def __init__(self, interaction_id: str, input_text: str, output_text: str):
        self.id = interaction_id
        self.input_text = input_text
        self.output_text = output_text

    def to_dict(self):
        return {
            'interaction_id': self.id,
            'input_text': self.input_text,
            'output_text': self.output_text
        }


class InteractionFactory:
    @staticmethod
    def create(input_text: str, output_text: str) -> InteractionEntity:
        return InteractionEntity(
            interaction_id=uuid.uuid4().__str__(),
            input_text=input_text,
            output_text=output_text
        )
