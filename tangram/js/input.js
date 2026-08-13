// input.js — 觸控/指標 → world 座標轉換與拖曳手勢
// data 座標 y 向上；SVG 內用 y'=flipY-y，故 world.y = flipY - svgY

// 螢幕座標 → SVG 使用者座標
export function svgPoint(svg, clientX, clientY) {
  const pt = svg.createSVGPoint();
  pt.x = clientX; pt.y = clientY;
  const ctm = svg.getScreenCTM();
  if (!ctm) return { x: 0, y: 0 };
  const p = pt.matrixTransform(ctm.inverse());
  return { x: p.x, y: p.y };
}

// 綁定拖曳/點按/雙擊。callbacks: {onPick, onMove, onDrop, onTap, onDouble}
// 座標一律回傳 world（已還原 y）。
export function attachPointer(svg, getFlipY, callbacks) {
  let active = null; // {id, startWX, startWY, moved, downTime}
  let lastTap = 0;

  const toWorld = (e) => {
    const t = e.touches ? e.touches[0] : e;
    const p = svgPoint(svg, t.clientX, t.clientY);
    return { x: p.x, y: getFlipY() - p.y };
  };

  function down(e) {
    const target = e.target.closest('[data-id]');
    if (!target) { callbacks.onBlank && callbacks.onBlank(); return; }
    const id = target.dataset.id;
    const w = toWorld(e);
    active = { id, sx: w.x, sy: w.y, lastx: w.x, lasty: w.y, moved: false, downTime: Date.now() };
    callbacks.onPick && callbacks.onPick(id, w);
    e.preventDefault();
  }
  function move(e) {
    if (!active) return;
    const w = toWorld(e);
    const dx = w.x - active.lastx, dy = w.y - active.lasty;
    if (Math.abs(w.x - active.sx) > 0.25 || Math.abs(w.y - active.sy) > 0.25) active.moved = true;
    active.lastx = w.x; active.lasty = w.y;
    callbacks.onMove && callbacks.onMove(active.id, dx, dy, w);
    e.preventDefault();
  }
  function up(e) {
    if (!active) return;
    const id = active.id, moved = active.moved;
    const now = Date.now();
    if (!moved) {
      if (now - lastTap < 300) { callbacks.onDouble && callbacks.onDouble(id); lastTap = 0; }
      else { callbacks.onTap && callbacks.onTap(id); lastTap = now; }
    }
    callbacks.onDrop && callbacks.onDrop(id, moved);
    active = null;
    e.preventDefault();
  }

  svg.addEventListener('mousedown', down);
  svg.addEventListener('mousemove', move);
  window.addEventListener('mouseup', up);
  svg.addEventListener('touchstart', down, { passive: false });
  svg.addEventListener('touchmove', move, { passive: false });
  window.addEventListener('touchend', up, { passive: false });

  return () => {
    svg.removeEventListener('mousedown', down);
    svg.removeEventListener('mousemove', move);
    window.removeEventListener('mouseup', up);
    svg.removeEventListener('touchstart', down);
    svg.removeEventListener('touchmove', move);
    window.removeEventListener('touchend', up);
  };
}
