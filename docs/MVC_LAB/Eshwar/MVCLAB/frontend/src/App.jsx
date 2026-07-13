import { useEffect, useState } from "react";
import {
  isLoggedIn, login, logout,
  fetchMe, fetchTasks, createTask, deleteTask,
} from "./services/api";
import "./App.module.css"; 
 
function LoginScreen({ onLogin }) {
  const [name, setName]         = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState(null);
 
  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await login(name, password);
      onLogin();
    } catch (e) { setError(e.message); }
  }
 
  return (
    <div style={{ maxWidth: 360, margin: "5rem auto", fontFamily: "system-ui" }}>
      <h1>Log in</h1>
      <form onSubmit={handleSubmit}
            style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <input value={name} onChange={e => setName(e.target.value)}
               placeholder="username" autoFocus />
        <input value={password} onChange={e => setPassword(e.target.value)}
               type="password" placeholder="password" />
        <button type="submit">Log in</button>
      </form>
      {error && <div style={{ color: "crimson", marginTop: 8 }}>{error}</div>}
    </div>
  );
}
 
 
function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [me, setMe]       = useState(null);
  const [title, setTitle] = useState("");
  const [busy, setBusy]   = useState(false);
  const [error, setError] = useState(null);
 
  async function refresh() {
    try {
      const [t, u] = await Promise.all([fetchTasks(), fetchMe()]);
      setTasks(t); setMe(u); setError(null);
    } catch (e) { setError(e.message); }
  }
 
  useEffect(() => { refresh(); }, []);
 
  async function handleAdd(e) {
    e.preventDefault();
    if (!title.trim()) return;
    setBusy(true);
    try { await createTask(title.trim()); setTitle(""); await refresh(); }
    catch (e) { setError(e.message); } finally { setBusy(false); }
  }
 
  async function handleDelete(id) {
    setBusy(true);
    try { await deleteTask(id); await refresh(); }
    catch (e) { setError(e.message); } finally { setBusy(false); }
  }
 
  return (
    <div style={{ maxWidth: 520, margin: "2rem auto", fontFamily: "system-ui" }}>
      <div style={{ display: "flex", justifyContent: "space-between",
                    alignItems: "center" }}>
        <h1>Tasks</h1>
        {me && <div>
          <span style={{ color: "#666" }}>Hi, {me.name}</span>{" "}
          <button onClick={() => { logout(); window.location.reload(); }}>
            Log out
          </button>
        </div>}
      </div>
 
      <form onSubmit={handleAdd} style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input value={title} onChange={e => setTitle(e.target.value)}
               placeholder="New task…" disabled={busy} style={{ flex: 1 }} />
        <button type="submit" disabled={busy || !title.trim()}>Add</button>
      </form>
 
      {error && <div style={{ color: "crimson" }}>{error}</div>}
 
      <ul style={{ listStyle: "none", padding: 0 }}>
        {tasks.map(t => (
          <li key={t.id} style={{ display: "flex", justifyContent: "space-between",
                                  padding: "8px 0", borderBottom: "1px solid #eee" }}>
            {t.title}
            <button onClick={() => handleDelete(t.id)} disabled={busy}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
 
 
export default function App() {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());
  return loggedIn
    ? <TaskList />
    : <LoginScreen onLogin={() => setLoggedIn(true)} />;
}
