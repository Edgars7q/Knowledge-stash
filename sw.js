/* App shell precache: replace atomically, retain previous functioning cache if install fails. */
const PREFIX=`ks-app-${encodeURIComponent(new URL(self.registration.scope).pathname)}-`;
const CACHE=PREFIX+'v0.3.0';
const ASSETS=['./','./index.html','./style.css?v=0.3.0','./auth.js?v=0.3.0','./demo/accounts.json','./data.js?v=0.3.0','./visuals.js?v=0.3.0','./lessons/builtin.js?v=0.3.0','./app.js?v=0.3.0','./packs/community.json','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)));});
self.addEventListener('message',e=>{if(e.data?.type==='SKIP_WAITING')self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim()})()));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==self.location.origin)return;
 e.respondWith((async()=>{const cache=await caches.open(CACHE);if(e.request.mode==='navigate'){try{const response=await fetch(e.request);if(response.ok)await cache.put(e.request,response.clone());return response}catch{return await cache.match('./index.html')||Response.error()}}
 // Update the published community pack online; use cached version offline.
 if(u.pathname.endsWith('/packs/community.json')){try{const r=await fetch(e.request);if(r.ok){await cache.put(e.request,r.clone());return r}}catch{}return await cache.match(e.request)||Response.error()}
 const existing=await cache.match(e.request);if(existing)return existing;
 try{const r=await fetch(e.request);if(r.ok)await cache.put(e.request,r.clone());return r}catch{return Response.error()}
 })());});
