/**
 * Smart City Nashik — Frontend config
 *
 * Single source of truth for the backend API base URL.
 * Resolution order (highest priority wins):
 *   1. localStorage.setItem('API_BASE_URL', '...')     — browser-level override
 *   2. <meta name="api-base-url" content="...">        — per-deployment override
 *   3. Pre-existing window.APP_CONFIG.API_BASE_URL     — inline <script> override
 *   4. DEV_API_BASE_URL if running on localhost/127
 *   5. PROD_API_BASE_URL                                — edit the constant below
 *
 * When deploying:
 *   - Easiest: set <meta name="api-base-url" content="https://your-backend.example.com">
 *     in the <head> of your frontend pages. No code edit needed.
 *   - Or edit PROD_API_BASE_URL below and redeploy.
 */
'use strict';

(function () {
  // ⚠ If your production backend is at a different URL, either set the meta
  //   tag in the HTML head, or change this constant.
  const PROD_API_BASE_URL = 'https://smart-city-portal-nashik-v2.onrender.com';
  const DEV_API_BASE_URL  = 'https://smart-city-portal-nashik-v2.onrender.com';

  const host    = (typeof location !== 'undefined' && location.hostname) || '';
  const isLocal = !host || host === 'localhost' || host === '127.0.0.1' || host === '0.0.0.0';

  function fromLocalStorage() {
    try { return localStorage.getItem('API_BASE_URL') || ''; } catch { return ''; }
  }

  function fromMeta() {
    const m = document.querySelector('meta[name="api-base-url"]');
    return (m && m.getAttribute('content')) || '';
  }

  const existing = (typeof window !== 'undefined' && window.APP_CONFIG) || {};

  const resolved =
    fromLocalStorage() ||
    fromMeta() ||
    existing.API_BASE_URL ||
    (isLocal ? DEV_API_BASE_URL : PROD_API_BASE_URL);

  window.APP_CONFIG = Object.assign({}, existing, {
    API_BASE_URL: (resolved || '').replace(/\/+$/, ''),  // trim trailing slash
    IS_LOCAL:     isLocal,
  });
})();
