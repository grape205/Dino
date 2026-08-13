// supabase.js — 進度同步（未登入寫 localStorage，登入後合併取較高星數）
const SUPA_URL = 'https://iizaesirhmhfwrjgabnw.supabase.co';
const SUPA_KEY = 'sb_publishable_e5libYdUvxTNKMnBscUvSw_8gj3QxyY';
const LS_KEY = 'tangram_progress_v1';

let sb = null;
let user = null;

function getClient() {
  if (sb) return sb;
  if (window.supabase && window.supabase.createClient) {
    sb = window.supabase.createClient(SUPA_URL, SUPA_KEY);
  }
  return sb;
}

export function loadLocal() {
  try { return JSON.parse(localStorage.getItem(LS_KEY) || '{}'); } catch { return {}; }
}
function saveLocal(map) {
  try { localStorage.setItem(LS_KEY, JSON.stringify(map)); } catch {}
}

// progress = { [levelId]: { stars, best_ms, hints_used } }
let progress = loadLocal();

export function getProgress() { return progress; }
export function getStars(id) { return (progress[id] && progress[id].stars) || 0; }

export function recordClear(id, stars, ms, hints) {
  const prev = progress[id] || { stars: 0, best_ms: null, hints_used: 0 };
  const merged = {
    stars: Math.max(prev.stars, stars),
    best_ms: prev.best_ms == null ? ms : Math.min(prev.best_ms, ms || prev.best_ms),
    hints_used: prev.hints_used + (hints || 0),
  };
  progress[id] = merged;
  saveLocal(progress);
  if (user) syncRow(id, merged);
  return merged;
}

async function syncRow(levelId, row) {
  const c = getClient(); if (!c || !user) return;
  try {
    await c.from('tangram_progress').upsert({
      user_id: user.id, level_id: Number(levelId),
      stars: row.stars, best_ms: row.best_ms, hints_used: row.hints_used,
    }, { onConflict: 'user_id,level_id' });
  } catch (e) { /* 離線可玩，忽略 */ }
}

export async function initAuth() {
  const c = getClient(); if (!c) return null;
  try {
    const { data: { session } } = await c.auth.getSession();
    if (session && session.user) {
      user = session.user;
      await mergeRemote();
    }
  } catch (e) {}
  return user;
}

async function mergeRemote() {
  const c = getClient(); if (!c || !user) return;
  try {
    const { data } = await c.from('tangram_progress').select('*').eq('user_id', user.id);
    if (Array.isArray(data)) {
      for (const r of data) {
        const local = progress[r.level_id];
        if (!local || r.stars > local.stars) {
          progress[r.level_id] = { stars: r.stars, best_ms: r.best_ms, hints_used: r.hints_used || 0 };
        }
      }
      saveLocal(progress);
    }
    // 反向：把本地較高的上傳
    for (const id in progress) syncRow(id, progress[id]);
  } catch (e) {}
}
