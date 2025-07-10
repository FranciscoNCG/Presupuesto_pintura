const CACHE_NAME = "presupuesto-cache-v1";
const FILES_TO_CACHE = [
  "./",
  "./index.html",
  "./style.css",
  "./script.js",
  "./manifest.json",
  "./img/logo.png"
];

// ✅ Instala y cachea archivos esenciales
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(FILES_TO_CACHE))
  );
  self.skipWaiting(); // Forza activación inmediata
});

// 🔄 Elimina versiones viejas del cache
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim(); // Toma control de todas las páginas abiertas
});

// 📦 Intercepta peticiones y sirve desde cache si es posible
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request).catch(() => {
        // 👉 Si no hay conexión y no está en caché
        return new Response("<h1>Sin conexión a internet</h1><p>Algunos recursos pueden no estar disponibles.</p>", {
          headers: { "Content-Type": "text/html" }
        });
      });
    })
  );
});