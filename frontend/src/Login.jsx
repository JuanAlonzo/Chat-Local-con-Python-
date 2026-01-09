import { useState } from "react";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim()) {
      onLogin(username);
    } else {
      alert("Por favor ingresa un nombre de usuario.");
    }
  };
  return (
    <div className="login-container">
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nombre de usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          maxLength={15}
        />
        <button type="submit">Iniciar Sesión</button>
      </form>
    </div>
  );
}

export default Login;
