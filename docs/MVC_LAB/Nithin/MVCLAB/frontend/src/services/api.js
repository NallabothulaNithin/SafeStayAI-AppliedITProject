const BASE = "http://localhost:8000";

export async function fetchTasks(){
    const res = await fetch(`${BASE}/api/tasks/`);
    
    if (!res.ok) throw new Error("Failed to load tasks");
    return res.json();
}

export async function fetchUsers() {
    const res = await fetch(`${BASE}/api/users/`);
    
    if (!res.ok) throw new Error("Failed to load users");
    return res.json();
}

export async function createTask(title, owner_id) {
  const res = await fetch(`${BASE}/api/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, owner_id }),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Create failed: ${res.status} ${detail}`);
  }
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE}/api/tasks/${id}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error("Delete failed");
}

// export async function fetchUsers() {
//   const res = await fetch(`${BASE}/api/users/`);
//   return res.json();
// }