/**
 * Smart City Nashik — Frontend config
 *
 * Single source of truth for the backend API base URL.
 * In production, edit the PROD_API_BASE_URL value below (or override
 * window.APP_CONFIG.API_BASE_URL from a deployment-specific script tag
 * loaded BEFORE this file).
 */
'use strict';

(function () {
  const PROD_API_BASE_URL = 'https://smart-city-portal-nashik-v2.onrender.com';
  const DEV_API_BASE_URL  = 'http://localhost:8001';

  const host    = (typeof location !== 'undefined' && location.hostname) || '';
  const isLocal = !host || host === 'localhost' || host === '127.0.0.1' || host === '0.0.0.0';

  const existing = (typeof window !== 'undefined' && window.APP_CONFIG) || {};

  window.APP_CONFIG = Object.assign(
    {
      API_BASE_URL: isLocal ? DEV_API_BASE_URL : PROD_API_BASE_URL,
    },
    existing
  );
})();
