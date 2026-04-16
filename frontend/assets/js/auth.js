/**
 * Smart City Nashik — Admin auth helpers
 *
 * Depends on: config.js (defines window.APP_CONFIG.API_BASE_URL)
 *
 * Usage:
 *   <script src="../../assets/js/config.js"></script>
 *   <script src="../../assets/js/auth.js"></script>
 *
 *   // Login page:
 *   await Auth.login('nmc', username, password);
 *   // → stores session, redirects to dashboard on success
 *
 *   // Dashboard page (on load):
 *   const session = await Auth.requireRole('nmc', 'login.html');
 *   // → redirects to login.html if token missing/expired/invalid
 *
 *   // Authenticated fetch:
 *   const res = await Auth.fetch('nmc', '/api/admin/grievances');
 *   // → auto-attaches Bearer token; logs out on 401
 */
'use strict';

(function () {
  const API_BASE = (window.APP_CONFIG && window.APP_CONFIG.API_BASE_URL) || '';

  const keys = (role) => ({
    token:    `${role}_token`,
    username: `${role}_username`,
    expires:  `${role}_expires`,
  });

  const loginPathFor = (role) => `/admin/${role}/login.html`;

  function getSession(role) {
    const k = keys(role);
    const token    = localStorage.getItem(k.token);
    const username = localStorage.getItem(k.username);
    const expires  = Number(localStorage.getItem(k.expires)) || 0;
    return { token, username, expires, isExpired: !token || Date.now() > expires };
  }

  function saveSession(role, data) {
    const k = keys(role);
    localStorage.setItem(k.token,    data.access_token);
    localStorage.setItem(k.username, data.username);
    localStorage.setItem(k.expires,  String(Date.now() + data.expires_in * 1000));
  }

  function clearSession(role) {
    const k = keys(role);
    [k.token, k.username, k.expires].forEach((key) => localStorage.removeItem(key));
  }

  function logout(role, redirectPath) {
    clearSession(role);
    const target = redirectPath || loginPathFor(role);
    window.location.href = target;
  }

  function authHeaders(role, extra) {
    const { token } = getSession(role);
    return Object.assign(
      { 'Authorization': `Bearer ${token || ''}`, 'Content-Type': 'application/json' },
      extra || {}
    );
  }

  /** Attempt login. Throws Error on failure with a user-friendly message. */
  async function login(role, username, password) {
    if (!API_BASE) {
      throw new Error('API base URL is not configured. See assets/js/config.js.');
    }
    let res, data;
    try {
      res = await fetch(`${API_BASE}/api/admin/login`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ username, password }),
      });
    } catch (networkErr) {
      console.error('Login network error. Tried:', `${API_BASE}/api/admin/login`, networkErr);
      throw new Error(
        `Cannot reach backend at ${API_BASE}. ` +
        `Check that the backend is running, the URL is correct, and CORS allows this origin.`
      );
    }

    try {
      data = await res.json();
    } catch {
      data = {};
    }

    if (!res.ok) {
      if (res.status === 401)      throw new Error(data.detail || 'Invalid username or password.');
      if (res.status === 422)      throw new Error('Please enter both username and password.');
      if (res.status >= 500)       throw new Error('Server error. Please try again shortly.');
      throw new Error(data.detail || `Login failed (${res.status}).`);
    }

    if (data.role !== role) {
      throw new Error(`Access denied. This portal is for ${role.toUpperCase()} admins only.`);
    }

    saveSession(role, data);
    return data;
  }

  /**
   * Call on dashboard load. Validates local session, then verifies with the
   * backend via GET /api/admin/me. Redirects to login if anything is wrong.
   * Returns the session { token, username, role } on success.
   */
  async function requireRole(role, loginHref) {
    const target = loginHref || loginPathFor(role);
    const session = getSession(role);

    if (session.isExpired) {
      logout(role, target);
      return null;
    }

    try {
      const res = await fetch(`${API_BASE}/api/admin/me`, {
        headers: { 'Authorization': `Bearer ${session.token}` },
      });
      if (!res.ok) {
        logout(role, target);
        return null;
      }
      const me = await res.json();
      if (me.role !== role) {
        logout(role, target);
        return null;
      }
      return { token: session.token, username: me.username, role: me.role };
    } catch {
      logout(role, target);
      return null;
    }
  }

  /**
   * Authenticated fetch. On 401, clears the session and redirects to login.
   * Returns the Response object on success for caller to .json() as needed.
   */
  async function authFetch(role, path, options) {
    const opts = Object.assign({}, options || {});
    opts.headers = authHeaders(role, (options && options.headers) || {});
    const res = await fetch(`${API_BASE}${path}`, opts);
    if (res.status === 401) {
      logout(role);
      throw new Error('Session expired. Please log in again.');
    }
    return res;
  }

  window.Auth = {
    API_BASE,
    getSession,
    saveSession,
    clearSession,
    logout,
    login,
    requireRole,
    authHeaders,
    fetch: authFetch,
  };
})();
