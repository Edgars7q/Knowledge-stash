/* Local demo accounts only. Public fixtures are not real authentication. */
window.KSAuth = (() => {
  'use strict';

  const SESSION_KEY = 'knowledge-stash-demo-session-v1';
  const scriptURL = document.currentScript?.src;
  const fixtureURL = scriptURL ? new URL('./demo/accounts.json', scriptURL).href : './demo/accounts.json';
  let accounts = [];
  let currentUser = null;
  let initialization = null;

  const publicUser = account => account ? {id: account.id, name: account.name, email: account.email} : null;

  function validateAccounts(data) {
    if (!data || data.schemaVersion !== 1 || !Array.isArray(data.accounts) || !data.accounts.length || data.accounts.length > 20) {
      throw new Error('Demo account data is invalid.');
    }
    const ids = new Set(), emails = new Set();
    return data.accounts.map(account => {
      if (!account || typeof account.id !== 'string' || !/^demo-[a-z0-9-]{1,40}$/.test(account.id) ||
          typeof account.name !== 'string' || !account.name.trim() || account.name.length > 80 ||
          typeof account.email !== 'string' || !/^[^\s@]+@[^\s@]+\.test$/.test(account.email.trim()) ||
          typeof account.password !== 'string' || !account.password || account.password.length > 100) {
        throw new Error('Demo account data is invalid.');
      }
      const normalized = {id: account.id, name: account.name.trim(), email: account.email.trim().toLowerCase(), password: account.password};
      if (ids.has(normalized.id) || emails.has(normalized.email)) throw new Error('Demo account data contains duplicate accounts.');
      ids.add(normalized.id);
      emails.add(normalized.email);
      return normalized;
    });
  }

  function readSession() {
    let raw;
    try { raw = localStorage.getItem(SESSION_KEY); }
    catch { throw new Error('Browser storage is unavailable. Demo sign-in cannot start.'); }
    if (!raw) return null;
    let session;
    try { session = JSON.parse(raw); } catch { session = null; }
    const account = session?.schemaVersion === 1 && typeof session.userId === 'string'
      ? accounts.find(candidate => candidate.id === session.userId) : null;
    if (!account) {
      try { localStorage.removeItem(SESSION_KEY); }
      catch { throw new Error('The invalid demo session could not be cleared.'); }
      return null;
    }
    return publicUser(account);
  }

  async function initialize() {
    if (!initialization) {
      initialization = (async () => {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 8000);
        try {
          const response = await fetch(fixtureURL, {cache: 'no-cache', signal: controller.signal});
          if (!response.ok) throw new Error('Demo accounts could not be loaded.');
          accounts = validateAccounts(await response.json());
          currentUser = readSession();
        } catch (error) {
          accounts = [];
          currentUser = null;
          throw error;
        } finally {
          clearTimeout(timeout);
        }
      })();
    }
    try { await initialization; }
    catch (error) { initialization = null; throw error; }
    return publicUser(currentUser);
  }

  async function signIn(email, password) {
    await initialize();
    const normalizedEmail = typeof email === 'string' ? email.trim().toLowerCase() : '';
    const account = accounts.find(candidate => candidate.email === normalizedEmail && candidate.password === password);
    if (!account) throw new Error('Use one of the fictional demo accounts and its demo password.');
    try { localStorage.setItem(SESSION_KEY, JSON.stringify({schemaVersion: 1, userId: account.id})); }
    catch { throw new Error('Browser storage is unavailable. You have not been signed in.'); }
    currentUser = publicUser(account);
    return publicUser(currentUser);
  }

  async function signOut() {
    try { localStorage.removeItem(SESSION_KEY); }
    catch { throw new Error('The demo session could not be cleared. You are still signed in.'); }
    currentUser = null;
    return null;
  }

  return Object.freeze({
    initialize,
    signIn,
    signOut,
    getCurrentUser: () => publicUser(currentUser),
    getDemoAccounts: () => accounts.map(account => ({...account}))
  });
})();
