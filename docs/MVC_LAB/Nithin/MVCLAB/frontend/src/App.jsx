import React, { useEffect, useState } from "react";
import "./App.css";
import {
  isLoggedIn, login, logout,
  fetchMe, fetchTasks, createTask, deleteTask,
} from "./services/api";
 
 
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
  <div className="loginBox">
    <h1>Log in</h1>

    <form onSubmit={handleSubmit} className="loginForm">
      <input
        className="input"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Username"
      />

      <input
        className="input"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />

      <button className="button" type="submit">
        Log in
      </button>
    </form>

    {error && <div className="error">{error}</div>}
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
  <div className="container">
    <div className="header">
      <h1 className="title">Tasks</h1>

      {me && (
        <div>
          <span className="subtitle">Hi, {me.name}</span>{" "}
          <button
            className="logout"
            onClick={() => {
              logout();
              window.location.reload();
            }}
          >
            Log out
          </button>
        </div>
      )}
    </div>

    <form onSubmit={handleAdd} className="form">
      <input
        className="input"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New task..."
      />

      <button className="button" type="submit">
        Add
      </button>
    </form>

    {error && <div className="error">{error}</div>}

    <ul className="taskList">
      {tasks.map((t) => (
        <li key={t.id} className="taskItem">
          {t.title}

          <button
            className="deleteBtn"
            onClick={() => handleDelete(t.id)}
          >
            Delete
          </button>
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
