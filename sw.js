/* Paradox — audioguía: caché para que funcione sin cobertura (sótano incluido).
   IMPORTANTE: sube el número de VERSION cada vez que publiques cambios,
   o los visitantes seguirán viendo la versión antigua guardada en su móvil. */
const VERSION = "pdx-guia-v18";

const SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./img/logo.png",
  "./img/icon-192.png",
  "./fonts/jokker-400.woff2",
  "./fonts/jokker-600.woff2",
  "./fonts/jokker-700.woff2",
  "./fonts/jokker-800.woff2"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(VERSION)
      .then(c => c.addAll(SHELL))
      .then(() => self.skipWaiting())
      .catch(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* Primero la caché (rápido y funciona sin datos); en segundo plano se
   refresca desde la red para la próxima visita. */
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;

  e.respondWith(
    caches.match(req).then(hit => {
      const net = fetch(req).then(res => {
        if (res && res.status === 200 && (res.type === "basic" || res.type === "cors")) {
          const copy = res.clone();
          caches.open(VERSION).then(c => c.put(req, copy)).catch(() => {});
        }
        return res;
      }).catch(() => hit);
      return hit || net;
    })
  );
});
