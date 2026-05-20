// src/App.jsx
import PublicGists from "./components/PublicGists";
import UserGists from "./components/UserGists";

function App() {
  return (
    <div>
      <h1>React Custom Hooks Lab</h1>
      <PublicGists />
      <hr />
      <UserGists />
    </div>
  );
}

export default App;
