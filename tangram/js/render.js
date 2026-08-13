// render.js — SVG 繪製
import { PIECES } from './pieces.js';
import { bboxOf, rotatePoint, centroid } from './geometry.js';

export const SVGNS = 'http://www.w3.org/2000/svg';

export function el(name, attrs = {}) {
  const e = document.createElementNS(SVGNS, name);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  return e;
}

// data 座標 y 軸向上；SVG y 向下 → 用 flipY 反轉
export function ptsToStr(verts, flipY) {
  return verts.map(([x, y]) => `${x},${flipY - y}`).join(' ');
}

// 依一組多邊形計算 viewBox（world 座標，y 已翻轉）
export function computeView(polys, pad = 1.4) {
  const b = bboxOf(polys);
  return {
    minX: b.minX - pad, minY: b.minY - pad,
    maxX: b.maxX + pad, maxY: b.maxY + pad,
    w: b.w + pad * 2, h: b.h + pad * 2,
    flipY: b.maxY + b.minY, // 使 y' = flipY - y 保持置中
  };
}

export function drawTargetSlot(g, verts, flipY, { fill, stroke = '#94a3b8', strokeW = 0.12, dash = null, opacity = 1 }) {
  const p = el('polygon', { points: ptsToStr(verts, flipY), fill: fill || 'none', stroke, 'stroke-width': strokeW, 'stroke-linejoin': 'round', opacity });
  if (dash) p.setAttribute('stroke-dasharray', dash);
  g.appendChild(p);
  return p;
}

// 以「質心 (cx,cy)」為錨點：先 flip→rotate，再平移使質心落在 (cx,cy)。
// 如此旋轉/翻面皆為原地進行。
export function pieceVerts(token) {
  const base = PIECES[token.type].verts.map(([x, y]) => [token.flip ? -x : x, y]);
  const rot = base.map((p) => rotatePoint(p, token.rot || 0));
  const c = centroid(rot);
  const cx = token.cx || 0, cy = token.cy || 0;
  return rot.map(([x, y]) => [x - c[0] + cx, y - c[1] + cy]);
}

// 畫一塊可操作的板；回傳 <polygon>
export function drawPiece(token, flipY, { selected = false, placed = false } = {}) {
  const def = PIECES[token.type];
  const verts = pieceVerts(token);
  const poly = el('polygon', {
    points: ptsToStr(verts, flipY),
    fill: def.color,
    stroke: selected ? '#fff' : 'rgba(0,0,0,.25)',
    'stroke-width': selected ? 0.28 : 0.14,
    'stroke-linejoin': 'round',
    opacity: placed ? 1 : 0.96,
    class: 'tg-piece' + (placed ? ' placed' : ''),
  });
  poly.dataset.id = token.id;
  return poly;
}
