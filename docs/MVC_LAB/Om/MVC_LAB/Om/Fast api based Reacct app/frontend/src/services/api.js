const BASE = "http://localhost:8000";

function authHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Call after every authenticated fetch. If the token expired or is invalid,
// clear it and throw a distinct error the UI can key off of.
function checkAuth(res) {
  if (res.status === 401) {
    logout();
    throw new Error("Unauthorized");
  }
}

export async function login(name, password) {
  // OAuth2 expects form-encoded with field names 'username' and 'password'.
  const body = new URLSearchParams({ username: name, password });
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!res.ok) throw new Error("Login failed");
  const { access_token } = await res.json();
  localStorage.setItem("token", access_token);
}

export function logout() {
  localStorage.removeItem("token");
}

export function isLoggedIn() {
  return !!localStorage.getItem("token");
}

export async function fetchTasks() {
  const res = await fetch(`${BASE}/tasks/`, {
    headers: { ...authHeaders() },
  });
  checkAuth(res);
  if (!res.ok) throw new Error("Fetch failed");
  return res.json();
}

export async function createTask(title) {
  const res = await fetch(`${BASE}/tasks/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify({ title }),
  });

  checkAuth(res);
  if (!res.ok) throw new Error("Create failed");
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE}/tasks/${id}`, {
    method: "DELETE",
    headers: { ...authHeaders() },
  });

  checkAuth(res);
  if (!res.ok) throw new Error("Delete failed");
}


export async function fetchUsers() {
  const res = await fetch(`${BASE}/users/`, {
    headers: { ...authHeaders() },
  });
  checkAuth(res);
  if (!res.ok) throw new Error("Fetch failed");
  return res.json();
}