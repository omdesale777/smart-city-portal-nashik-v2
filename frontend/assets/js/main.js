/**
 * Smart City Nashik — Shared JS Utilities (main.js)
 * Lightweight helpers used across all 4 module pages.
 * Each module page loads this via <script src="../assets/js/main.js">
 */

'use strict';

/* ─────────────────────────────────────────
   CONFIG
   API base URL comes from window.APP_CONFIG (see assets/js/config.js).
   Pages must load config.js BEFORE main.js.
───────────────────────────────────────── */
const CONFIG = {
  get API_BASE() {
    return (window.APP_CONFIG && window.APP_CONFIG.API_BASE_URL) || '';
  },
  SUPABASE_URL: '',                    // ← not used directly in frontend
};

/* ─────────────────────────────────────────
   TOAST NOTIFICATION
───────────────────────────────────────── */
const Toast = (() => {
  let el = null;
  let timer = null;

  function _ensure() {
    if (el) return;
    el = document.createElement('div');
    el.className = 'toast';
    document.body.appendChild(el);
  }

  function show(message, duration = 3000) {
    _ensure();
    el.textContent = message;
    el.classList.add('show');
    clearTimeout(timer);
    timer = setTimeout(() => el.classList.remove('show'), duration);
  }

  return { show };
})();

/* ─────────────────────────────────────────
   CUSTOM CURSOR
   Call initCursor() on pages that use cursor: none
───────────────────────────────────────── */
function initCursor(accentColor = 'rgba(232,101,10,0.55)') {
  const dot  = document.getElementById('cursor');
  const ring = document.getElementById('cursorRing');
  if (!dot || !ring) return;

  let mx = 0, my = 0, rx = 0, ry = 0;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    dot.style.transform = `translate(${mx - 5}px, ${my - 5}px)`;
  });

  (function follow() {
    rx += (mx - rx) * 0.12;
    ry += (my - ry) * 0.12;
    ring.style.transform = `translate(${rx - 17}px, ${ry - 17}px)`;
    requestAnimationFrame(follow);
  })();

  // Grow on interactive elements
  document.querySelectorAll('a, button, label, [role="button"]').forEach(el => {
    el.addEventListener('mouseenter', () => {
      ring.style.width  = '46px';
      ring.style.height = '46px';
      ring.style.borderColor = accentColor;
    });
    el.addEventListener('mouseleave', () => {
      ring.style.width  = '34px';
      ring.style.height = '34px';
    });
  });
}

/* ─────────────────────────────────────────
   API HELPERS
───────────────────────────────────────── */
const API = {
  /**
   * POST JSON to a backend endpoint.
   * @param {string} path  - e.g. '/api/grievances'
   * @param {object} data  - plain JS object
   */
  async post(path, data) {
    const res = await fetch(`${CONFIG.API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
    return res.json();
  },

  /**
   * POST FormData (for file uploads).
   * @param {string}   path
   * @param {FormData} formData
   */
  async upload(path, formData) {
    const res = await fetch(`${CONFIG.API_BASE}${path}`, {
      method: 'POST',
      body: formData,     // browser sets Content-Type: multipart/form-data automatically
    });
    if (!res.ok) throw new Error(`Upload ${res.status}: ${res.statusText}`);
    return res.json();
  },

  /**
   * GET from a backend endpoint.
   * @param {string} path
   */
  async get(path) {
    const res = await fetch(`${CONFIG.API_BASE}${path}`);
    if (!res.ok) throw new Error(`GET ${res.status}: ${res.statusText}`);
    return res.json();
  },
};

/* ─────────────────────────────────────────
   FORM VALIDATION HELPERS
───────────────────────────────────────── */
const Validate = {
  /** Mark a .field-group as having an error */
  setError(fieldGroupId, message) {
    const fg = document.getElementById(fieldGroupId);
    if (!fg) return;
    fg.classList.add('has-error');
    const errEl = fg.querySelector('.error-msg');
    if (errEl && message) errEl.textContent = message;
  },

  clearError(fieldGroupId) {
    const fg = document.getElementById(fieldGroupId);
    if (fg) fg.classList.remove('has-error');
  },

  clearAll() {
    document.querySelectorAll('.field-group.has-error')
      .forEach(fg => fg.classList.remove('has-error'));
  },

  isPhone(value) {
    return /^\d{10}$/.test(value.trim());
  },

  isEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
  },

  notEmpty(value) {
    return value.trim().length > 0;
  },
};

/* ─────────────────────────────────────────
   GEOLOCATION HELPER
───────────────────────────────────────── */
function getLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation not supported in this browser.'));
      return;
    }
    navigator.geolocation.getCurrentPosition(
      pos => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      err => reject(err),
      { timeout: 10000, maximumAge: 60000 }
    );
  });
}

/* ─────────────────────────────────────────
   TICKET / REFERENCE ID GENERATOR
   Generates a human-readable ID like NMC-384920
───────────────────────────────────────── */
function generateRefId(prefix = 'NSK') {
  const rand = Math.floor(100000 + Math.random() * 900000);
  return `${prefix}-${rand}`;
}

/* ─────────────────────────────────────────
   COPY TO CLIPBOARD
───────────────────────────────────────── */
async function copyToClipboard(text, feedbackEl) {
  try {
    await navigator.clipboard.writeText(text);
    if (feedbackEl) {
      const original = feedbackEl.textContent;
      feedbackEl.textContent = '✓ Copied!';
      setTimeout(() => { feedbackEl.textContent = original; }, 2000);
    }
    Toast.show('Copied to clipboard');
  } catch {
    Toast.show('Could not copy — please copy manually.');
  }
}

/* ─────────────────────────────────────────
   IMAGE FALLBACK HELPER
   Called via onerror on <img> tags.
───────────────────────────────────────── */
function imgFallback(imgEl, emoji, label, bgGradient) {
  imgEl.style.display = 'none';
  const parent = imgEl.parentElement;
  let fb = parent.querySelector('.img-fallback');
  if (!fb) {
    fb = document.createElement('div');
    fb.className = 'img-fallback';
    fb.style.cssText = `
      width:100%; height:100%;
      display:flex; align-items:center; justify-content:center;
      flex-direction:column; gap:.5rem;
      background:${bgGradient || 'linear-gradient(135deg,#1a1a2e,#16213e)'};
    `;
    parent.appendChild(fb);
  }
  fb.innerHTML = `
    <span style="font-size:2.5rem">${emoji}</span>
    <span style="font-size:.82rem;color:rgba(255,255,255,.65);font-weight:500">${label}</span>
  `;
}

/* ─────────────────────────────────────────
   INTERSECTION OBSERVER — Lazy Animations
   Add class 'anim-on-scroll' to elements
   you want to fade up when they enter viewport.
───────────────────────────────────────── */
function initScrollAnimations() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-up');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.anim-on-scroll').forEach(el => observer.observe(el));
}

/* ─────────────────────────────────────────
   CHARACTER COUNTER
───────────────────────────────────────── */
function initCharCounter(textareaId, counterId, max) {
  const ta = document.getElementById(textareaId);
  const ct = document.getElementById(counterId);
  if (!ta || !ct) return;
  function update() {
    const n = ta.value.length;
    ct.textContent = `${n} / ${max}`;
    ct.classList.toggle('warn', n > max * 0.85);
  }
  ta.addEventListener('input', update);
  update();
}

/* ─────────────────────────────────────────
   DRAG-AND-DROP UPLOAD ZONE
───────────────────────────────────────── */
function initDropZone(zoneId, onFiles) {
  const zone = document.getElementById(zoneId);
  if (!zone) return;

  zone.addEventListener('dragover', e => {
    e.preventDefault();
    zone.classList.add('drag-over');
  });
  zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('drag-over');
    const files = [...e.dataTransfer.files];
    if (files.length) onFiles(files);
  });
}

/* ─────────────────────────────────────────
   INIT — runs on every page that loads this file
───────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initScrollAnimations();
});
