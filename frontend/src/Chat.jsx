import { useState, useEffect, useRef } from "react";

function Chat({ username, onLogout }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [status, setStatus] = useState("Conectando...");

  // Usamos useRef para mantener la conexión persistente sin causar renderizados extra
  const ws = useRef(null);
  // Referencia para bajar el scroll automáticamente al último mensaje
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // 1. CONEXIÓN: Creamos el WebSocket apuntando a nuestro backend
    // Nota: Usamos 'localhost:8000' porque ahí corre Python
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.hostname}:8000/ws/${username}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      setStatus("🟢 Conectado");
      console.log("Conectado al servidor");
    };

    ws.current.onmessage = (event) => {
      // 2. RECIBIR: Cuando llega un mensaje, lo agregamos a la lista
      const newMessage = event.data;
      setMessages((prev) => [...prev, newMessage]);
    };

    ws.current.onclose = () => {
      setStatus("🔴 Desconectado");
    };

    // 3. LIMPIEZA: Si el usuario cierra el componente, cerramos la conexión
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [username]);

  // Efecto para bajar el scroll siempre que llega un mensaje nuevo
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (inputValue.trim() && ws.current) {
      ws.current.send(inputValue);
      setInputValue("");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div>
          <span>
            Hola, <b>{username}</b>
          </span>
          <small style={{ marginLeft: "10px" }}>{status}</small>
        </div>
        <button onClick={onLogout} className="logout-btn">
          Salir
        </button>
      </header>

      <div className="messages-area">
        {messages.map((msg, index) => (
          // Como el backend nos manda texto plano "[Hora] Juan: Hola", lo mostramos directo
          <div key={index} className="message-line">
            {msg}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Escribe un mensaje..."
        />
        <button onClick={sendMessage}>Enviar</button>
      </div>
    </div>
  );
}

export default Chat;
