import { useState } from "react";
import Login from "./Login.jsx";
import Chat from "./Chat.jsx";

function App() {
  const [user, setUser] = useState(null);

  return (
    <div className="app">
      {!user ? (
        <Login onLogin={(name) => setUser(name)} />
      ) : (
        <Chat username={user} onLogout={() => setUser(null)} />
      )}
    </div>
  );
}

export default App;
