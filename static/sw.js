self.addEventListener('install', (e) => {
  self.skipWaiting(); // Darhol yangi versiyaga o'tish
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          return caches.delete(cacheName); // Barcha eski keshlarni o'chirish
        })
      );
    }).then(() => {
      self.clients.claim(); // Barcha ochiq sahifalarni darhol o'ziga bo'ysundirish
    })
  );
});

self.addEventListener('fetch', (e) => {
  // Har doim tarmoqdan yuklash, keshdan foydalanmaslik
  e.respondWith(fetch(e.request).catch(() => {
      // Tarmoq uzilsa ham xatolik qaytarish (keshni qidirmaslik)
      return new Response("Offline", { status: 503, statusText: "Offline" });
  }));
});
