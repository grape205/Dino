// game.js — 遊戲流程、渲染協調、計分
import { PIECES, SYMBOLS } from './pieces.js';
import { LEVELS, CHAPTERS } from './levels.js';
import { centroid, bboxOf, vertsEqualSet, unionOutline } from './geometry.js';
import { el, ptsToStr, drawPiece, drawTargetSlot, pieceVerts } from './render.js';
import { attachPointer } from './input.js';
import { getProgress, getStars, recordClear } from './supabase.js';

const $ = (id) => document.getElementById(id);
const SNAP_R = 1.9;      // 吸附半徑（world 單位）
const SNAP_TOL = 0.28;   // 頂點集合比對容差

// ---------- 音效 ----------
let AC = null;
function ac() { if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch {} } return AC; }
function beep(freq, dur = 0.12, type = 'sine', vol = 0.18, delay = 0) {
  const c = ac(); if (!c) return;
  const o = c.createOscillator(), g = c.createGain();
  o.type = type; o.frequency.value = freq;
  o.connect(g); g.connect(c.destination);
  const t = c.currentTime + delay;
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(vol, t + 0.01);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.start(t); o.stop(t + dur + 0.02);
}
const sndSelect = () => beep(520, 0.06, 'triangle', 0.12);
const sndSnap = () => { beep(660, 0.08, 'square', 0.16); beep(880, 0.1, 'square', 0.16, 0.06); };
const sndWin = () => [523, 659, 784, 1046].forEach((f, i) => beep(f, 0.16, 'triangle', 0.2, i * 0.12));
const sndTry = () => beep(300, 0.14, 'sine', 0.12);

// ---------- 狀態 ----------
let level = null, tokens = [], slots = [], view = null;
let selectedId = null, hintTier = 0, startTime = 0, detach = null;
let t4Selected = new Set(), t4HintTier = 0;

// ---------- 選單 ----------
export function showMenu() {
  $('play').style.display = 'none';
  $('menu').style.display = 'block';
  const prog = getProgress();
  const wrap = $('chapterList');
  wrap.innerHTML = '';
  for (const ch of CHAPTERS) {
    const lvls = LEVELS.filter((l) => l.chapter === ch.id);
    const card = document.createElement('div');
    card.className = 'chapter';
    card.style.borderColor = ch.color + '55';
    const done = lvls.filter((l) => getStars(l.id) > 0).length;
    card.innerHTML = `<div class="ch-hd"><span class="ch-emoji">${ch.emoji}</span>
      <span class="ch-name">第 ${ch.id} 章 ${ch.name}</span>
      <span class="ch-prog">${done}/${lvls.length}</span></div>`;
    const grid = document.createElement('div');
    grid.className = 'lv-grid';
    for (const l of lvls) {
      const s = getStars(l.id);
      const btn = document.createElement('button');
      btn.className = 'lv-btn' + (s > 0 ? ' cleared' : '');
      btn.innerHTML = `<span class="lv-num">${l.id}</span><span class="lv-nm">${l.name}</span>
        <span class="lv-stars">${'★'.repeat(s)}${'☆'.repeat(3 - s)}</span>`;
      btn.onclick = () => startLevel(l.id);
      grid.appendChild(btn);
    }
    card.appendChild(grid);
    wrap.appendChild(card);
  }
}

// ---------- 開始關卡 ----------
export function startLevel(id) {
  level = LEVELS.find((l) => l.id === id);
  if (!level) return;
  if (detach) { detach(); detach = null; }
  $('menu').style.display = 'none';
  $('play').style.display = 'flex';
  $('lvName').textContent = `第 ${level.id} 關・${level.name}`;
  $('lvTeach').textContent = level.teach || '';
  hintTier = 0; selectedId = null; startTime = Date.now();
  $('winOverlay').classList.remove('show');

  if (level.type === 'T4') { setupT4(); }
  else { setupPuzzle(); }
}

// =====================================================
//  T1 / T2 / T3 — 拼圖
// =====================================================
function setupPuzzle() {
  $('t4bar').style.display = 'none';
  $('ctrlbar').style.display = 'flex';

  slots = level.solution.map((s) => ({ piece: s.piece, verts: s.verts, filled: false }));

  // 建立托盤中的可操作塊（rot0/flip0），置於棋盤下方
  const boardB = bboxOf(level.solution.map((s) => s.verts));
  const boardCX = (boardB.minX + boardB.maxX) / 2;
  const n = level.solution.length;
  const perRow = Math.min(4, n);
  const spacing = 5, rowH = 5.2;
  tokens = level.solution.map((s, i) => {
    const row = Math.floor(i / perRow);
    const inThisRow = Math.min(perRow, n - row * perRow);
    const col = i % perRow;
    const cx = boardCX + (col - (inThisRow - 1) / 2) * spacing;
    const cy = boardB.minY - 3.5 - row * rowH;
    return { id: 'p' + i, type: s.piece, rot: 0, flip: false, cx, cy, placed: false };
  });

  // 視圖：涵蓋棋盤 + 所有初始塊
  const all = level.solution.map((s) => s.verts).concat(tokens.map((t) => pieceVerts(t)));
  const b = bboxOf(all); const pad = 1.6;
  view = {
    minX: b.minX - pad, minY: b.minY - pad, maxX: b.maxX + pad, maxY: b.maxY + pad,
    flipY: b.maxY + b.minY,
  };
  buildSvg();
  renderPuzzle();

  detach = attachPointer($('svg'), () => view.flipY, {
    onPick: (id) => { const t = tokens.find((x) => x.id === id); if (t && !t.placed) { selectedId = id; sndSelect(); renderPuzzle(); } },
    onBlank: () => { selectedId = null; renderPuzzle(); },
    onMove: (id, dx, dy) => {
      const t = tokens.find((x) => x.id === id);
      if (t && !t.placed) { t.cx += dx; t.cy += dy; renderPuzzle(); }
    },
    onDrop: (id, moved) => { if (moved) trySnap(id); },
    onDouble: (id) => rotateToken(id),
  });
}

function buildSvg() {
  const wrap = $('boardWrap');
  wrap.innerHTML = '';
  const svg = el('svg', {
    id: 'svg', viewBox: `${view.minX} ${view.minY} ${view.maxX - view.minX} ${view.maxY - view.minY}`,
  });
  svg.style.touchAction = 'none';
  wrap.appendChild(svg);
}

function renderPuzzle() {
  const svg = $('svg');
  svg.innerHTML = '';
  const gTarget = el('g'); svg.appendChild(gTarget);

  // 目標區
  const outline = unionOutline(level.solution.map((s) => s.verts));
  if (level.type === 'T3') {
    if (outline) drawTargetSlot(gTarget, outline, view.flipY, { fill: 'rgba(148,163,184,.18)', stroke: '#cbd5e1', strokeW: 0.22 });
  } else {
    // T1 上色 / T2 只分割線
    for (const s of slots) {
      const filled = s.filled;
      drawTargetSlot(gTarget, s.verts, view.flipY, {
        fill: level.type === 'T1' && !filled ? PIECES[s.piece].color + '3a' : 'rgba(148,163,184,.14)',
        stroke: filled ? 'transparent' : '#cbd5e1',
        strokeW: 0.16, dash: filled ? null : '0.5,0.4',
      });
    }
    if (outline) drawTargetSlot(gTarget, outline, view.flipY, { fill: 'none', stroke: '#94a3b8', strokeW: 0.22 });
  }

  // 提示 ghost
  if (hintGhost) drawTargetSlot(gTarget, hintGhost.verts, view.flipY,
    { fill: PIECES[hintGhost.piece].color + '99', stroke: '#fff', strokeW: 0.2 });

  // 已放置的塊（在目標上）
  const gPieces = el('g'); svg.appendChild(gPieces);
  for (const t of tokens) if (t.placed) gPieces.appendChild(drawPiece(t, view.flipY, { placed: true }));
  // 未放置的塊（在托盤）— 選中的最後畫（最上層）
  const unplaced = tokens.filter((t) => !t.placed).sort((a, b) => (a.id === selectedId ? 1 : 0) - (b.id === selectedId ? 1 : 0));
  for (const t of unplaced) {
    const p = drawPiece(t, view.flipY, { selected: t.id === selectedId });
    gPieces.appendChild(p);
    // ⑦ 可翻面提示
  }
  updateStarPreview();
}

function rotateToken(id) {
  const t = tokens.find((x) => x.id === id);
  if (!t || t.placed) return;
  t.rot = (t.rot + 1) % 8;
  sndSelect(); selectedId = id; renderPuzzle();
}
function flipToken(id) {
  const t = tokens.find((x) => x.id === id);
  if (!t || t.placed) return;
  if (!PIECES[t.type].flippable) { sndTry(); return; }
  t.flip = !t.flip; sndSelect(); selectedId = id; renderPuzzle();
}

function trySnap(id) {
  const t = tokens.find((x) => x.id === id);
  if (!t || t.placed) return;
  const tv = pieceVerts(t);
  const cTok = centroid(tv);
  let best = null, bestDist = SNAP_R;
  for (const s of slots) {
    if (s.filled) continue;
    const cSlot = centroid(s.verts);
    const dist = Math.hypot(cSlot[0] - cTok[0], cSlot[1] - cTok[1]);
    if (dist > bestDist) continue;
    const aligned = tv.map(([x, y]) => [x + cSlot[0] - cTok[0], y + cSlot[1] - cTok[1]]);
    if (vertsEqualSet(aligned, s.verts, SNAP_TOL)) { best = { s, cx: cSlot[0], cy: cSlot[1] }; bestDist = dist; }
  }
  if (best) {
    t.cx = best.cx; t.cy = best.cy; t.placed = true; best.s.filled = t;
    selectedId = null; hintGhost = null; sndSnap(); renderPuzzle();
    if (slots.every((s) => s.filled)) setTimeout(win, 260);
  }
}

// ---------- 提示 ----------
let hintGhost = null, hintTimer = null;
export function useHint() {
  if (!level) return;
  if (level.type === 'T4') return t4Hint();
  hintTier++;
  const openSlot = slots.find((s) => !s.filled);
  if (!openSlot) return;
  if (hintTier >= 3) {
    // 自動放一塊
    const tok = tokens.find((t) => !t.placed && PIECES[t.type].verts.length === PIECES[openSlot.piece].verts.length);
    if (tok) {
      // 找出能對到 openSlot 的旋轉/翻面
      placeIntoSlot(tok, openSlot);
      return;
    }
  }
  hintGhost = { verts: openSlot.verts, piece: openSlot.piece };
  clearTimeout(hintTimer);
  hintTimer = setTimeout(() => { hintGhost = null; renderPuzzle(); }, 2600);
  renderPuzzle();
}
function placeIntoSlot(tok, slot) {
  // 暴力嘗試 8 旋轉 × 2 翻面，對到 slot
  const cs = centroid(slot.verts);
  const flips = PIECES[tok.type].flippable ? [false, true] : [false];
  for (const fl of flips) for (let r = 0; r < 8; r++) {
    const test = { ...tok, rot: r, flip: fl, cx: cs[0], cy: cs[1] };
    if (vertsEqualSet(pieceVerts(test), slot.verts, SNAP_TOL)) {
      tok.rot = r; tok.flip = fl; tok.cx = cs[0]; tok.cy = cs[1];
      tok.placed = true; slot.filled = tok; hintGhost = null; sndSnap(); renderPuzzle();
      if (slots.every((s) => s.filled)) setTimeout(win, 260);
      return;
    }
  }
}

// ---------- 勝利 ----------
function starsFor() {
  if (hintTier === 0) return 3;
  if (hintTier <= 2) return 2;
  return 1;
}
function updateStarPreview() {
  const filled = slots.filter((s) => s.filled).length;
  $('progressPill').textContent = `${filled} / ${slots.length}`;
}
function win() {
  const ms = Date.now() - startTime;
  const stars = starsFor();
  recordClear(level.id, stars, ms, hintTier);
  sndWin();
  const ov = $('winOverlay');
  $('winStars').textContent = '★'.repeat(stars) + '☆'.repeat(3 - stars);
  $('winTitle').textContent = stars === 3 ? '太棒了！完美通關！' : '完成囉！';
  const next = LEVELS.find((l) => l.id === level.id + 1);
  $('nextBtn').style.display = next ? 'inline-block' : 'none';
  $('nextBtn').onclick = () => next && startLevel(next.id);
  ov.classList.add('show');
  // 撒星星
  const fx = $('winFx'); fx.innerHTML = '';
  for (let i = 0; i < 18; i++) {
    const s = document.createElement('div');
    s.className = 'confetti';
    s.textContent = ['⭐', '🌟', '✨', '🦖', '🥚'][i % 5];
    s.style.left = Math.random() * 100 + '%';
    s.style.animationDelay = (Math.random() * 0.5) + 's';
    s.style.fontSize = (0.8 + Math.random()) + 'rem';
    fx.appendChild(s);
  }
}

// =====================================================
//  T4 — 移動辨識
// =====================================================
function setupT4() {
  $('ctrlbar').style.display = 'none';
  $('t4bar').style.display = 'flex';
  t4Selected = new Set(); t4HintTier = 0;

  const all = level.from.map((p) => p.verts).concat(level.to.map((p) => p.verts));
  const b = bboxOf(all); const pad = 1.4;
  const flipY = b.maxY + b.minY;

  const wrap = $('boardWrap');
  wrap.innerHTML = '';
  const mk = (list, label) => {
    const box = document.createElement('div');
    box.className = 't4-board';
    const svg = el('svg', { viewBox: `${b.minX - pad} ${b.minY - pad} ${b.w + pad * 2} ${b.h + pad * 2}` });
    for (const p of list) {
      const poly = el('polygon', {
        points: ptsToStr(p.verts, flipY), fill: PIECES[p.piece].color,
        stroke: 'rgba(0,0,0,.3)', 'stroke-width': 0.14, 'stroke-linejoin': 'round',
        class: 't4-poly', 'data-piece': PIECES[p.piece].num,
      });
      svg.appendChild(poly);
      const c = centroid(p.verts);
      const tx = el('text', { x: c[0], y: flipY - c[1], class: 't4-label',
        'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 1.5 });
      tx.textContent = PIECES[p.piece].num;
      svg.appendChild(tx);
    }
    const cap = document.createElement('div'); cap.className = 't4-cap'; cap.textContent = label;
    box.appendChild(cap); box.appendChild(svg);
    return box;
  };
  wrap.appendChild(mk(level.from, '① 原本'));
  wrap.appendChild(mk(level.to, '② 變化後'));

  // 序號按鈕
  const numRow = $('t4nums'); numRow.innerHTML = '';
  const used = level.from.map((p) => PIECES[p.piece].num).sort((a, b) => a - b);
  for (const num of used) {
    const btn = document.createElement('button');
    btn.className = 't4-num'; btn.textContent = SYMBOLS[num];
    btn.onclick = () => {
      if (t4Selected.has(num)) t4Selected.delete(num); else t4Selected.add(num);
      btn.classList.toggle('on', t4Selected.has(num)); sndSelect();
    };
    numRow.appendChild(btn);
  }
  $('t4msg').textContent = '哪幾塊移動了？點選序號後送出';
}

export function submitT4() {
  if (!level || level.type !== 'T4') return;
  const sel = [...t4Selected].sort((a, b) => a - b);
  const ans = [...level.answer].sort((a, b) => a - b);
  if (sel.length === 0) { $('t4msg').textContent = '先點選你覺得移動的塊喔！'; sndTry(); return; }
  if (JSON.stringify(sel) === JSON.stringify(ans)) {
    const stars = t4HintTier === 0 ? 3 : t4HintTier <= 2 ? 2 : 1;
    recordClear(level.id, stars, Date.now() - startTime, t4HintTier);
    sndWin();
    $('winStars').textContent = '★'.repeat(stars) + '☆'.repeat(3 - stars);
    $('winTitle').textContent = '答對了！';
    const next = LEVELS.find((l) => l.id === level.id + 1);
    $('nextBtn').style.display = next ? 'inline-block' : 'none';
    $('nextBtn').onclick = () => next && startLevel(next.id);
    $('winFx').innerHTML = '';
    $('winOverlay').classList.add('show');
  } else {
    $('t4msg').textContent = '再想想看～提示：先找出「沒有動」的塊！';
    sndTry();
  }
}

function t4Hint() {
  t4HintTier++;
  const moved = new Set(level.answer);
  const polys = $('boardWrap').querySelectorAll('.t4-poly');
  polys.forEach((p) => p.classList.remove('hi-stay', 'hi-move', 'dim'));
  if (t4HintTier === 1) {
    // 高亮沒動的塊
    polys.forEach((p) => { if (!moved.has(+p.dataset.piece)) p.classList.add('hi-stay'); });
    $('t4msg').textContent = '綠色的塊「沒有移動」，其他的就是候選！';
  } else if (t4HintTier === 2) {
    polys.forEach((p) => { if (moved.has(+p.dataset.piece)) p.classList.add('hi-move'); else p.classList.add('dim'); });
    $('t4msg').textContent = '閃爍的塊就是移動了的塊！';
  } else {
    polys.forEach((p) => { if (moved.has(+p.dataset.piece)) p.classList.add('hi-move'); });
    $('t4msg').textContent = '答案：' + level.answer.map((n) => SYMBOLS[n]).join('、');
    level.answer.forEach((n) => t4Selected.add(n));
    $('t4nums').querySelectorAll('.t4-num').forEach((b, i) => {});
  }
}

// ---------- 目前選中塊的旋轉/翻面（控制列按鈕）----------
export function rotateSelected() { if (selectedId) rotateToken(selectedId); else sndTry(); }
export function flipSelected() { if (selectedId) flipToken(selectedId); else sndTry(); }
