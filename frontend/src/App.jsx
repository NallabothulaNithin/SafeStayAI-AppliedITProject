import { useEffect, useMemo, useState } from "react";
import { fetchTasks, fetchUsers, createTask, deleteTask } from "./services/api";
 
export default function App() {
  const [tasks, setTasks]       = useState([]);
  const [users, setUsers]       = useState([]);
  const [title, setTitle]       = useState("");
  const [ownerId, setOwnerId]   = useState("");
  const [loading, setLoading]   = useState(true);
  const [busy, setBusy]         = useState(false);
  const [error, setError]       = useState(null);
 
  const usersById = useMemo(
    () => Object.fromEntries(users.map(u => [u.id, u])),
    [users]
  );
 
  async function refresh() {
    try {
      const [t, u] = await Promise.all([fetchTasks(), fetchUsers()]);
      setTasks(t);
      setUsers(u);
      if (!ownerId && u.length) setOwnerId(String(u[0].id));
      setError(null);
    } catch (e) { setError(e.message); }
  }
 
  useEffect(() => { refresh().finally(() => setLoading(false)); }, []);
 
  async function handleAdd(e) {
    e.preventDefault();
    if (!title.trim() || !ownerId) return;
    setBusy(true);
    try {
      await createTask(title.trim(), Number(ownerId));
      setTitle("");
      await refresh();
    } catch (e) { setError(e.message); } finally { setBusy(false); }
  }
 
  async function handleDelete(id) {
    setBusy(true);
    try { await deleteTask(id); await refresh(); }
    catch (e) { setError(e.message); } finally { setBusy(false); }
  }
 
  if (loading) return <div>Loading…</div>;
 
  return (
    <div style={{ maxWidth: 520, margin: "2rem auto", fontFamily: "system-ui" }}>
      <h1>Tasks</h1>
      <form onSubmit={handleAdd} style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input value={title} onChange={e => setTitle(e.target.value)}
               placeholder="New task…" disabled={busy} style={{ flex: 1 }} />
        <select value={ownerId} onChange={e => setOwnerId(e.target.value)} disabled={busy}>
          {users.map(u => <option key={u.id} value={u.id}>{u.name}</option>)}
        </select>
        <button type="submit" disabled={busy || !title.trim()}>Add</button>
      </form>
 
      {error && <div style={{ color: "crimson" }}>Error: {error}</div>}
 
      <ul style={{ listStyle: "none", padding: 0 }}>
        {tasks.map(t => (
          <li key={t.id} style={{ display: "flex", justifyContent: "space-between",
                                  padding: "8px 0", borderBottom: "1px solid #eee" }}>
            <span>
              {t.title}{" "}
              <small style={{ color: "#888" }}>
                — {usersById[t.owner_id]?.name ?? "?"}
              </small>
            </span>
            <button onClick={() => handleDelete(t.id)} disabled={busy}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
