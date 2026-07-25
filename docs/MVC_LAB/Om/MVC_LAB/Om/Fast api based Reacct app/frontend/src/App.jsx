import React from 'react';
import { useEffect, useState } from "react";
import { fetchTasks, createTask, deleteTask, login, logout, isLoggedIn } from "./services/api";

function LoginScreen({ onLogin }) {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await login(name, password);
      onLogin();
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div style={{ maxWidth: 320, margin: "4rem auto", fontFamily: "system-ui" }}>
      <h1>Log in</h1>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <input value={name} onChange={e => setName(e.target.value)} placeholder="Username" />
        <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="Password" />
        <button type="submit">Log in</button>
      </form>
      {error && <div style={{ color: "crimson", marginTop: 8 }}>{error}</div>}
    </div>
  );
}

export default function App() {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());
  const [tasks, setTasks]       = useState([]);
  const [title, setTitle]       = useState("");
  const [loading, setLoading]   = useState(true);
  const [busy, setBusy]         = useState(false);
  const [error, setError]       = useState(null);

  async function refresh() {
    try {
      const t = await fetchTasks();
      setTasks(t);
      setError(null);
    } catch (e) {
      if (e.message === "Unauthorized") {
        setLoggedIn(false);
        return;
      }
      setError(e.message);
    }
  }

  useEffect(() => {
    if (loggedIn) refresh().finally(() => setLoading(false));
    else setLoading(false);
  }, [loggedIn]);

  if (!loggedIn) {
    return <LoginScreen onLogin={() => setLoggedIn(true)} />;
  }

  async function handleAdd(e) {
    e.preventDefault();
    if (!title.trim()) return;
    setBusy(true);
    try {
      await createTask(title.trim());
      setTitle("");
      await refresh();
    } catch (e) {
      if (e.message === "Unauthorized") setLoggedIn(false);
      else setError(e.message);
    } finally { setBusy(false); }
  }

  async function handleDelete(id) {
    setBusy(true);
    try { await deleteTask(id); await refresh(); }
    catch (e) {
      if (e.message === "Unauthorized") setLoggedIn(false);
      else setError(e.message);
    } finally { setBusy(false); }
  }

  function handleLogout() {
    logout();
    setLoggedIn(false);
  }

  if (loading) return <div>Loading…</div>;

  return (
    <div style={{ maxWidth: 520, margin: "2rem auto", fontFamily: "system-ui" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Tasks</h1>
        <button onClick={handleLogout}>Logout</button>
      </div>
      <form onSubmit={handleAdd} style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input value={title} onChange={e => setTitle(e.target.value)}
               placeholder="New task…" disabled={busy} style={{ flex: 1 }} />
        <button type="submit" disabled={busy || !title.trim()}>Add</button>
      </form>

      {error && <div style={{ color: "crimson" }}>Error: {error}</div>}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {tasks.map(t => (
          <li key={t.id} style={{ display: "flex", justifyContent: "space-between",
                                  padding: "8px 0", borderBottom: "1px solid #eee" }}>
            <span>{t.title}</span>
            <button onClick={() => handleDelete(t.id)} disabled={busy}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
