const BASE = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api').replace(/\/$/, '');
const tokenKey = 'hudumalite_access';
export const getToken = () => sessionStorage.getItem(tokenKey);
export const setToken = (token) => sessionStorage.setItem(tokenKey, token);
export const clearToken = () => { sessionStorage.removeItem(tokenKey); sessionStorage.removeItem('hudumalite_refresh'); };

export async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  if (options.body && !(options.body instanceof FormData)) headers['Content-Type'] = 'application/json';
  const response = await fetch(`${BASE}${path}`, { ...options, headers });
  if (response.status === 204) return null;
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = typeof data === 'object' ? Object.entries(data).map(([k,v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : typeof v === 'string' ? v : JSON.stringify(v)}`).join(' · ') : 'Request failed';
    throw new Error(message || `Request failed (${response.status})`);
  }
  return data;
}
export const login = async (username, password) => {
  const result = await api('/auth/token/', { method: 'POST', body: JSON.stringify({ username, password }) });
  setToken(result.access); if (result.refresh) sessionStorage.setItem('hudumalite_refresh', result.refresh); return result;
};
