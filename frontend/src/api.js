const BASE_URL = "http://localhost:8000";

async function request(path, options = {}) {
    const res = await fetch(BASE_URL + path, {
        headers: {"Content-Type": "application/json" },
        ...options,
    });
    if (!res.ok) {
        throw new Error(`${res.status} ${res.statusText}`);
    }
    if (res.status == 204) return null; 
    return res.json();
}

export const getSessions = (module = "") => {
    const query = module ? `?module=${encodeURIComponent(module)}` : "";
    return request("/sessions" + query);
};

export const getModules = () => request("/modules");

export const addSession = (session) => request("/sessions", { method: "POST", body: JSON.stringify(session) });

export const updateSession = (id, session) => request(`/sessions/${id}`, { method: "PUT", body: JSON.stringify(session) });

export const deleteSession = (id) => request(`/sessions/${id}`, { method: "DELETE" });