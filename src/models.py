from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


# Modelos públicos de las partidas
class PublicPlayer(BaseModel):
    name: str
    is_owner: bool


class PublicGame(BaseModel):
    id: str
    players: list[PublicPlayer]


# Modelos de datos entregador por cada usuario al servidor


class PingPayload(BaseModel):
    type: Literal["ping"] = "ping"


class RequestDicePayload(BaseModel):
    type: Literal["request_dice"] = "request_dice"


Payload = Annotated[Union[PingPayload, RequestDicePayload], Field(discriminator="type")]

# Modelos de datos entregados por el servidor a cada usuario


class PingResponse(BaseModel):
    type: Literal["ping"] = "ping"
    data: str


class InvalidPayloadResponse(BaseModel):
    type: Literal["invalid"] = "invalid"


class RequestDiceResponse(BaseModel):
    type: Literal["request_dice"] = "request_dice"
    data: list[int]


Response = Annotated[
    Union[PingResponse, RequestDiceResponse, InvalidPayloadResponse],
    Field(discriminator="type"),
]
