import { useEffect, useState } from "react";
import { fetchTasks, fetchUsers, createTask, deleteTask } from "./services/api";
import styles from "./App.module.css";
 
export default function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [users, setUsers] = useState([]);
  const [selectedOwner, setSelectedOwner] = useState("");
 
  async function refresh() {
    try {
      const data = await fetchTasks();
      setTasks(data);
      setError(null);
    } catch (e) {
      setError(e.message);
    }
  }
 
  useEffect(() => {
    Promise.all([fetchTasks(), fetchUsers()])
      .then(([tasksData, usersData]) => {
        setTasks(tasksData);
        setUsers(usersData);})
        .finally(() => setLoading(false));
      }, []);
 
  async function handleAdd(e) {
    e.preventDefault();
    const t = title.trim();
    if (!t) return;
    if (!selectedOwner) {
      setError("Please select a user");
      return;
    }
    try {
      await createTask(t, Number(selectedOwner));
      setTitle("");
      await refresh();
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
 
  async function handleDelete(id) {
    setBusy(true);
    try {
      await deleteTask(id);
      await refresh();
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  const usersById = Object.fromEntries(users.map((u) => [u.id, u]));
 
  return (
    <div className={styles.wrap}>
      <h1 className={styles.h1}>Tasks</h1>
 
      <form onSubmit={handleAdd} className={styles.form}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task title…"
          className={styles.input}
          disabled={busy}
        />
        <select
          value={selectedOwner}
          onChange={(e) => setSelectedOwner(e.target.value)}
          >
          <option value="">Select User</option>
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.name}
            </option>
          ))}
          </select>
        <button
          type="submit"
          className={styles.btn}
          disabled={busy || !title.trim()}
        >
          Add
        </button>
      </form>
 
      {error && <div className={styles.error}>Error: {error}</div>}
 
      {loading ? (
        <div className={styles.muted}>Loading…</div>
      ) : tasks.length === 0 ? (
        <div className={styles.muted}>No tasks yet — add one above.</div>
      ) : (
        <ul className={styles.list}>
          {tasks.map((t) => (
            <li key={t.id} className={styles.item}>
              <span>
                <span className={styles.id}>#{t.id}</span> {t.title} {" - "} {usersById[t.owner_id]?.name}
              </span>
              <button
                onClick={() => handleDelete(t.id)}
                className={styles.del}
                disabled={busy}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}