from .client_types import SendFn
from .models import InvalidPayloadResponse, Payload


class Player:
    def __init__(self, user_name: str, send: SendFn, is_host=False) -> None:
        self.send = send
        self.user_name = user_name
        self.is_host = is_host


class Game:
    def __init__(self, host_user_name: str, host_send: SendFn) -> None:
        self.has_started = False
        self.host = Player(host_user_name, send=host_send, is_host=True)
        self.players: list[Player] = [self.host]
        self.game_state = "esperando jugadores"

        self.current_context_handler = self.wait_for_players

    # Eventos

    async def on_player_join(self, user_name: str, send: SendFn) -> Player:
        player = Player(user_name, send)
        self.players.append(player)
        return player

    async def on_player_exit(self, event_player: Player):
        "Función que es llamada cuando un jugador se desconecta"
        self.players.remove(event_player)

    async def on_player_action(self, event_player: Player, action: Payload):
        "Función que es llamada cuando un jugador envía una acción"
        if action.type == "ping":
            payload = {"type": "ping", "data": f"pong from {event_player.user_name}"}
            for player in self.players:
                await player.send(payload)
        else:
            ok = await self.current_context_handler(event_player, action)
            if ok:
                return
            for player in self.players:
                await player.send(InvalidPayloadResponse())

    # Eventos manejados dentro del contexto actual

    async def wait_for_players(self, event_player: Player, action: Payload):
        "Contexto de espera de jugadores"
        if action.type == "start" and event_player.is_host:
            self.has_started = True
            self.current_context_handler = self.wait_for_dice
            return True

    async def wait_for_dice(self, event_player: Player, action: Payload):
        "Contexto de espera que todos los jugadores tiren el dado"
        if action.type == "request_dice":
            # ToDo: asignarle dados al usuario que los pide y enviarle sus dados
            return True
