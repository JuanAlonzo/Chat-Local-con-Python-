let ws;
let username;

function startChat() {
  username = document.getElementById("username").value.trim();
  if (username === "") {
    alert("Por favor, ingresa un nombre de usuario.");
    return;
  }

  // Ocultar login y mostrar chat
  document.getElementById("login").style.display = "none";
  document.getElementById("chat-container").style.display = "block";

  ws = new WebSocket(`ws://${window.location.hostname}:8000/ws/${username}`);

  ws.onmessage = (event) => {
    const message = event.data;

    if (message.startsWith("👥 Usuarios conectados: ")) {
      document.getElementById("users").textContent = message;
    } else {
      const msgElement = document.createElement("p");

      if (message.includes("(privado)")) {
        msgElement.style.color = "red";
      }

      msgElement.innerHTML = `<b>${message}</b>`;
      document.getElementById("chat").appendChild(msgElement);
    }
  };
}

function sendMessage() {
  const input = document.getElementById("message");
  const message = input.value.trim();
  if (message !== "") {
    ws.send(message);
    input.value = "";
  }
}
