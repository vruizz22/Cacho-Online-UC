async function loadGames() {
  const response = await fetch("/api/games");

  /** @type {Array<{id: string, players: { name: string, is_owner: boolean }[]}>} */
  const games = await response.json();

  const gamesList = document.getElementById("games");

  for (const game of games) {
    const gameElement = document.createElement("li");
    gameElement.classList.add("game");

    const playersList = document.createElement("ul");
    playersList.classList.add("players");

    for (const player of game.players) {
      const playerLi = document.createElement("li");
      playerLi.innerText = player.name;
      playersList.appendChild(playerLi);

      if (player.is_owner) playerLi.classList.add("owner");
    }

    const joinButton = document.createElement("button");
    joinButton.innerText = "Unirse";
    joinButton.addEventListener("click", () => connect(game.id));

    gameElement.appendChild(playersList);
    gameElement.appendChild(joinButton);

    gamesList.appendChild(gameElement);
  }
}

/** @param {string | undefined} gameId */
function connect(gameId = undefined) {
  const userName = document.getElementById("userName").value;

  const wsUrl = new URL("/api/ws", window.location.href);
  wsUrl.protocol = wsUrl.protocol.replace("http", "ws");

  wsUrl.searchParams.set("user_name", userName);
  if (gameId) wsUrl.searchParams.set("game_id", gameId);
  const ws = new WebSocket(wsUrl);

  // Show game screen
  attachGameEvents(ws);
}

/** @param {WebSocket} ws */
function attachGameEvents(ws) {
  /**  @param {object} data */
  const send = (data) => ws.send(JSON.stringify(data));

  document.getElementById("game-lobby").hidden = true;
  document.getElementById("game-screen").hidden = false;

  const pingBtn = document.getElementById("ping");
  pingBtn.addEventListener("click", () => send({ type: "ping" }));

  ws.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    console.log(data);
  });
}

window.addEventListener("load", () => {
  loadGames();
  document.getElementById("create-game").addEventListener("click", () => connect());
});
