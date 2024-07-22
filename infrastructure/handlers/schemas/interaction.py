from pydantic import BaseModel


class InteractionInput(BaseModel):
    input_text: str
    output_text: str


class InteractionOutput(BaseModel):
    interaction_id: str
    input_text: str
    output_text: str
