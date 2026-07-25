import React, { useEffect, useState } from "react";
import { fetchTasks, createTask, deleteTask } from "./services/api";
import "./App.css";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadTasks() {
    try {
      setError("");
      const data = await fetchTasks();
      setTasks(data);
    } catch (err) {
      console.error(err);
      setError("Could not load tasks. Check if backend is running.");
    }
  }

  useEffect(() => {
    loadTasks().finally(() => setLoading(false));
  }, []);

  async function handleAdd(e) {
    e.preventDefault();

    if (!title.trim()) return;

    try {
      setError("");
      await createTask(title.trim());
      setTitle("");
      await loadTasks();
    } catch (err) {
      console.error(err);
      setError("Could not create task.");
    }
  }

  async function handleDelete(id) {
    try {
      setError("");
      await deleteTask(id);
      await loadTasks();
    } catch (err) {
      console.error(err);
      setError("Could not delete task.");
    }
  }

  if (loading) {
    return <p className="loading">Loading tasks...</p>;
  }

  return (
    <div className="page">
      <div className="todo-card">
        <h1>Todo List</h1>
        <p className="subtitle">Manage your daily tasks</p>

        <form onSubmit={handleAdd} className="task-form">
          <input
            type="text"
            placeholder="Enter task title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <button type="submit">Add</button>
        </form>

        {error && <p className="error">{error}</p>}

        <div className="task-list">
          {tasks.length === 0 ? (
            <p className="empty">No tasks yet. Add one above.</p>
          ) : (
            tasks.map((task) => (
              <div className="task-item" key={task.id}>
                <span>{task.title}</span>
                <button onClick={() => handleDelete(task.id)}>Delete</button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}