const BASE = "http://localhost:8000";

export async function fetchTasks() {
  const res = await fetch(`${BASE}/tasks/`);
  if (!res.ok) throw new Error("Fetch failed");
  return res.json();
}

export async function createTask(title) {
  const res = await fetch(`${BASE}/tasks/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title }),
  });

  if (!res.ok) throw new Error("Create failed");
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE}/tasks/${id}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error("Delete failed");
}