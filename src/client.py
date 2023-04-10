from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError, parse_obj_as, parse_raw_as

from .client_types import SupportsJSON
from .game import Game, Player
from .models import Payload, Response


class GameConnection:
    "Conecta el usuario con la partida"

    def __init__(self, ws: WebSocket, player: Player) -> None:
        self.ws = ws
        self.player = player


def send_message_wrapped(ws: WebSocket):
    "Validamos los mensajes que salen del servidor"

    async def send_message(message: dict | SupportsJSON):
        try:
            if isinstance(message, dict):
                msg = parse_obj_as(Response, message).json()
            else:
                msg = message.json()
            await ws.send_text(msg)
        except ValidationError as e:
            print("Invalid message:", e.errors())

    return send_message


class GameSession:
    "Guarda la partida y las conexiones de los usuarios"

    def __init__(self, host_user_name, host_send) -> None:
        self.id = uuid4().hex
        self.game = Game(host_user_name, host_send)
        self.__connections: list[GameConnection] = []

    @classmethod
    def create(cls, ws: WebSocket, user_name: str):
        session = cls(host_user_name=user_name, host_send=send_message_wrapped(ws))
        connection = GameConnection(ws, session.game.host)
        session.__connections.append(connection)
        return session, connection

    async def join(self, ws: WebSocket, user_name: str):
        player = await self.game.on_player_join(user_name, send_message_wrapped(ws))
        connection = GameConnection(ws, player)
        self.__connections.append(connection)
        return connection

    def remove_connection(self, connection: GameConnection):
        self.__connections.remove(connection)

    @property
    def is_public(self):
        return not self.game.has_started

    @property
    def should_be_removed(self):
        return len(self.__connections) == 0


class GameClient:
    "Maneja las partidas y las conexiones de los usuarios"

    def __init__(self):
        self.games_sessions: dict[str, GameSession] = {}

    async def __start_game_session(self, ws: WebSocket, user: str, game_id: str | None):
        "Se crea la sesión de juego si no existe y se conecta el usuario"
        if game_id is None:
            game_session, connection = GameSession.create(ws, user)
            print(f"Creating game session ({game_session.id}) by {user}")
            self.games_sessions[game_session.id] = game_session
            return game_session, connection

        game_session = self.games_sessions.get(game_id)
        if game_session is None or game_session.game.has_started:
            await ws.send_json({"error": "Game not found"})
            raise WebSocketDisconnect(reason="Game not found")

        connection = await game_session.join(ws, user)

        return game_session, connection

    async def connect(self, ws: WebSocket, user: str, game_id: str | None):
        await ws.accept()
        try:
            session, cn = await self.__start_game_session(ws, user, game_id)
        except WebSocketDisconnect:
            return

        try:
            await self.__loop(session, cn)
        except WebSocketDisconnect:
            session.remove_connection(cn)
            await session.game.on_player_exit(cn.player)
            print(f"Connection of user {cn.player.user_name} ({id(ws)}) closed")
            if session.should_be_removed:
                print(f"Removing game session {session.id}")
                del self.games_sessions[session.id]

    async def __loop(self, session: GameSession, cn: GameConnection):
        while True:
            try:
                data = parse_raw_as(Payload, await cn.ws.receive_text())
                await session.game.on_player_action(cn.player, data)
            except ValidationError as e:
                print("Invalid message:", e.errors())
                await cn.ws.send_json({"type": "error", "error": e.errors()})


game_client = GameClient()
