/**
 * Smart City Nashik — Preloader
 *
 * Drop-in, self-injecting loading screen.
 * Usage: include this script once per page, ideally inside <head>:
 *   <script src="/assets/js/preloader.js"></script>
 *
 * Injects its own styles + DOM, fades out on `window.load`, then removes itself.
 * Honors prefers-reduced-motion.
 */
(function () {
  'use strict';
  if (window.__scnPreloader) return;
  window.__scnPreloader = true;

  const reduceMotion =
    window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const css = `
    #scn-preloader {
      position: fixed; inset: 0; z-index: 2147483000;
      display: grid; place-items: center;
      background:
        radial-gradient(60% 70% at 50% 45%, rgba(232,101,10,0.10), transparent 70%),
        radial-gradient(80% 100% at 50% 100%, rgba(201,146,42,0.08), transparent 70%),
        linear-gradient(180deg, #0A0A12 0%, #0E0E18 50%, #0A0A12 100%);
      color: #F0EDE8;
      opacity: 1;
      transition: opacity 600ms ease, visibility 600ms ease, filter 600ms ease;
    }
    #scn-preloader.is-hiding { opacity: 0; filter: blur(6px); visibility: hidden; pointer-events: none; }

    /* Faint grid */
    #scn-preloader::before {
      content: ''; position: absolute; inset: 0;
      background-image:
        linear-gradient(rgba(232,101,10,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(232,101,10,0.05) 1px, transparent 1px);
      background-size: 48px 48px;
      mask-image: radial-gradient(ellipse at center, #000 30%, transparent 80%);
      -webkit-mask-image: radial-gradient(ellipse at center, #000 30%, transparent 80%);
      pointer-events: none;
    }

    .scn-pl-stack {
      position: relative; z-index: 1;
      display: flex; flex-direction: column; align-items: center; gap: 1.75rem;
      padding: 0 1.25rem; text-align: center;
    }

    .scn-pl-ring {
      position: relative; width: 132px; height: 132px;
      display: grid; place-items: center;
      filter: drop-shadow(0 0 24px rgba(232,101,10,0.35));
    }
    .scn-pl-ring svg { width: 100%; height: 100%; display: block; }
    .scn-pl-ring .scn-track { stroke: rgba(255,255,255,0.08); }
    .scn-pl-ring .scn-arc   {
      stroke: url(#scnGrad);
      stroke-linecap: round;
      transform-origin: 50% 50%;
      animation: scn-rot 2.6s linear infinite, scn-dash 2.6s ease-in-out infinite;
    }
    .scn-pl-ring::after {
      content: ''; position: absolute; inset: 18%;
      border-radius: 50%;
      background: radial-gradient(circle at 50% 50%, rgba(240,192,96,0.22), rgba(232,101,10,0.05) 55%, transparent 75%);
      animation: scn-pulse 2.6s ease-in-out infinite;
    }
    .scn-pl-core {
      position: absolute; width: 10px; height: 10px; border-radius: 50%;
      background: #F0C060;
      box-shadow: 0 0 14px #F0C060, 0 0 28px rgba(232,101,10,0.7);
      animation: scn-pulse 2.6s ease-in-out infinite;
    }

    .scn-pl-text { display: flex; flex-direction: column; align-items: center; gap: .4rem; }
    .scn-pl-deva {
      font-family: 'Noto Sans Devanagari','DM Sans',sans-serif;
      font-size: 1.4rem; font-weight: 700;
      color: #F0C060; letter-spacing: 0.02em;
      opacity: 0; animation: scn-fadein .9s ease .15s forwards;
    }
    .scn-pl-title {
      font-family: 'Playfair Display','DM Sans',serif;
      font-size: 1.05rem; font-weight: 700;
      color: #F0EDE8; letter-spacing: 0.18em; text-transform: uppercase;
      opacity: 0; animation: scn-fadein .9s ease .35s forwards;
    }
    .scn-pl-sub {
      font-family: 'DM Sans', sans-serif;
      font-size: .78rem; color: rgba(240,237,232,0.55);
      letter-spacing: 0.14em; text-transform: uppercase;
      opacity: 0; animation: scn-fadein .9s ease .55s forwards;
    }
    .scn-pl-sub::after {
      content: '...'; display: inline-block; width: 1.2em; text-align: left;
      animation: scn-dots 1.6s steps(4, end) infinite;
    }

    @keyframes scn-rot   { to { transform: rotate(360deg); } }
    @keyframes scn-dash  {
      0%   { stroke-dasharray: 20 260; stroke-dashoffset: 0; }
      50%  { stroke-dasharray: 140 260; stroke-dashoffset: -60; }
      100% { stroke-dasharray: 20 260; stroke-dashoffset: -280; }
    }
    @keyframes scn-pulse {
      0%,100% { opacity: .65; transform: scale(1); }
      50%     { opacity: 1;   transform: scale(1.08); }
    }
    @keyframes scn-fadein { to { opacity: 1; } }
    @keyframes scn-dots   { 0% { content: ''; } 25% { content: '.'; } 50% { content: '..'; } 75%,100% { content: '...'; } }

    @media (prefers-reduced-motion: reduce) {
      .scn-pl-ring .scn-arc { animation: none; }
      .scn-pl-ring::after, .scn-pl-core { animation: none; }
      .scn-pl-sub::after { animation: none; content: '...'; }
    }
    @media (max-width: 480px) {
      .scn-pl-ring { width: 108px; height: 108px; }
      .scn-pl-deva  { font-size: 1.2rem; }
      .scn-pl-title { font-size: .95rem; letter-spacing: 0.14em; }
    }
  `;

  const style = document.createElement('style');
  style.id = 'scn-preloader-style';
  style.textContent = css;
  (document.head || document.documentElement).appendChild(style);

  const html = `
    <div id="scn-preloader" role="status" aria-live="polite" aria-label="Loading Smart City Nashik Portal">
      <div class="scn-pl-stack">
        <div class="scn-pl-ring">
          <svg viewBox="0 0 120 120" aria-hidden="true">
            <defs>
              <linearGradient id="scnGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%"  stop-color="#F0C060"/>
                <stop offset="55%" stop-color="#E8650A"/>
                <stop offset="100%" stop-color="#C9922A"/>
              </linearGradient>
            </defs>
            <circle class="scn-track" cx="60" cy="60" r="50" fill="none" stroke-width="2"/>
            <circle class="scn-arc"   cx="60" cy="60" r="50" fill="none" stroke-width="3"
                    stroke-dasharray="20 260" stroke-dashoffset="0"/>
          </svg>
          <div class="scn-pl-core"></div>
        </div>
        <div class="scn-pl-text">
          <div class="scn-pl-deva">नाशिक स्मार्ट सिटी</div>
          <div class="scn-pl-title">Smart City Portal</div>
          <div class="scn-pl-sub">Loading civic intelligence</div>
        </div>
      </div>
    </div>
  `;

  function mount() {
    if (document.getElementById('scn-preloader')) return;
    const holder = document.createElement('div');
    holder.innerHTML = html;
    (document.body || document.documentElement).prepend(holder.firstElementChild);
  }

  function hide() {
    const el = document.getElementById('scn-preloader');
    if (!el) return;
    el.classList.add('is-hiding');
    const cleanup = () => { el.remove(); };
    if (reduceMotion) cleanup();
    else setTimeout(cleanup, 700);
  }

  // Mount as soon as <body> exists (so it covers the whole render).
  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount, { once: true });

  // Fade out when the page + subresources are ready, with a minimum display
  // so it doesn't flash on fast loads.
  const minVisibleMs = 650;
  const startedAt    = Date.now();

  function scheduleHide() {
    const elapsed = Date.now() - startedAt;
    const wait    = Math.max(0, minVisibleMs - elapsed);
    setTimeout(hide, wait);
  }

  if (document.readyState === 'complete') scheduleHide();
  else window.addEventListener('load', scheduleHide, { once: true });

  // Safety net: never keep the preloader longer than 8 seconds.
  setTimeout(hide, 8000);
})();
