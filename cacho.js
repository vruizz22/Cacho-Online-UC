const diceContainer = document.getElementById("diceContainer");
const rollDiceButton = document.getElementById("rollDiceButton");

rollDiceButton.addEventListener("click", () => {
  // Generar los números de los dados
  const numeros = [];
  for (let i = 0; i < 5; i++) {
    numeros.push(Math.floor(Math.random() * 6) + 1);
  }

  // Eliminar los dados anteriores
  while (diceContainer.firstChild) {
    diceContainer.removeChild(diceContainer.firstChild);
  }

  // Crear y animar los nuevos dados
  numeros.forEach((numero) => {
    const dice = document.createElement("div");
    dice.className = "dice dice-" + numero;
    diceContainer.appendChild(dice);

    gsap.to(dice, {
      duration: 1,
      x: Math.random() * 200 - 100,
      y: Math.random() * 200 - 100,
      rotation: Math.random() * 360,
      ease: "back.out(1.7)",
    });
  });
});
const diceContainer = document.getElementById("diceContainer");
const rollDiceButton = document.getElementById("rollDiceButton");

rollDiceButton.addEventListener("click", () => {
  // Generar los números de los dados
  const numeros = [];
  for (let i = 0; i < 5; i++) {
    numeros.push(Math.floor(Math.random() * 6) + 1);
  }

  // Eliminar los dados anteriores
  while (diceContainer.firstChild) {
    diceContainer.removeChild(diceContainer.firstChild);
  }

  // Crear y animar los nuevos dados
  numeros.forEach((numero) => {
    const dice = document.createElement("div");
    dice.className = "dice dice-" + numero;
    diceContainer.appendChild(dice);

    gsap.to(dice, {
      duration: 1,
      x: Math.random() * 200 - 100,
      y: Math.random() * 200 - 100,
      rotation: Math.random() * 360,
      ease: "back.out(1.7)",
    });
  });
});
