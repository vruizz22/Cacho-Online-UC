from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from .client import game_client
from .models import PublicGame, PublicPlayer

app = FastAPI(docs_url="/api/docs", description="Ir a [la página principal](/)")


@app.get("/api/games", tags=["Juegos"])
def get_games() -> list[PublicGame]:
    "Devuelve los juegos abiertos"

    public_games: list[PublicGame] = []
    for game_session in game_client.games_sessions.values():
        print(game_session.is_public)
        if not game_session.is_public:
            continue

        public_game = PublicGame(
            id=game_session.id,
            players=[
                PublicPlayer(name=player.user_name, is_owner=player.is_host)
                for player in game_session.game.players
            ],
        )
        public_games.append(public_game)
    return public_games


@app.websocket("/api/ws")
async def websocket_endpoint(ws: WebSocket, user_name: str, game_id: str | None = None):
    "Conecta un usuario a la sesión de juegos"

    print(f"Connecting {user_name} ({id(ws)})")
    await game_client.connect(ws, user_name, game_id)
    print(f"Disconnecting {user_name} ({id(ws)})")


app.mount("/", StaticFiles(directory="web", html=True), name="static")
