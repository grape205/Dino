// geometry.js — 七巧板幾何核心
// 座標系 y 軸向上；旋轉僅允許 45° 倍數；比較用 EPS。
export const EPS = 1e-6;
export const DEG45 = Math.PI / 4;

// ---- 基本 ----
export function signedArea(poly) {
  let a = 0;
  for (let i = 0; i < poly.length; i++) {
    const [x1, y1] = poly[i], [x2, y2] = poly[(i + 1) % poly.length];
    a += x1 * y2 - x2 * y1;
  }
  return a / 2;
}
export const area = (poly) => Math.abs(signedArea(poly));
export function ensureCCW(poly) {
  return signedArea(poly) < 0 ? poly.slice().reverse() : poly.slice();
}
export function centroid(poly) {
  let x = 0, y = 0;
  for (const p of poly) { x += p[0]; y += p[1]; }
  return [x / poly.length, y / poly.length];
}
export function bbox(poly) {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const [x, y] of poly) {
    if (x < minX) minX = x; if (x > maxX) maxX = x;
    if (y < minY) minY = y; if (y > maxY) maxY = y;
  }
  return { minX, minY, maxX, maxY, w: maxX - minX, h: maxY - minY };
}
export function bboxOf(polys) {
  return bbox(polys.flat());
}

// ---- 變換（皆 45° 步進）----
export function rotatePoint([x, y], steps) {
  const a = ((steps % 8) + 8) % 8 * DEG45;
  const c = Math.cos(a), s = Math.sin(a);
  return [x * c - y * s, x * s + y * c];
}
export function translate(poly, dx, dy) {
  return poly.map(([x, y]) => [x + dx, y + dy]);
}
// 把某塊（局部座標）套用 flip→rotate(steps*45)→translate
export function transformPiece(localVerts, { rot = 0, flip = false, tx = 0, ty = 0 } = {}) {
  return localVerts.map(([x, y]) => {
    const fx = flip ? -x : x;
    const [rx, ry] = rotatePoint([fx, y], rot);
    return [rx + tx, ry + ty];
  });
}

// ---- 頂點集合比對（與順序無關，EPS）----
export function vertsEqualSet(a, b, tol = 1e-4) {
  if (a.length !== b.length) return false;
  const used = new Array(b.length).fill(false);
  for (const p of a) {
    let found = -1;
    for (let j = 0; j < b.length; j++) {
      if (used[j]) continue;
      if (Math.abs(p[0] - b[j][0]) < tol && Math.abs(p[1] - b[j][1]) < tol) { found = j; break; }
    }
    if (found < 0) return false;
    used[found] = true;
  }
  return true;
}

// ---- 凸多邊形交集面積（Sutherland–Hodgman）----
function insideEdge(p, A, B) {
  return (B[0] - A[0]) * (p[1] - A[1]) - (B[1] - A[1]) * (p[0] - A[0]) >= -EPS;
}
function edgeInter(p1, p2, A, B) {
  const d1 = [p2[0] - p1[0], p2[1] - p1[1]], d2 = [B[0] - A[0], B[1] - A[1]];
  const den = d1[0] * d2[1] - d1[1] * d2[0];
  const t = ((A[0] - p1[0]) * d2[1] - (A[1] - p1[1]) * d2[0]) / den;
  return [p1[0] + t * d1[0], p1[1] + t * d1[1]];
}
export function clipConvex(subject, clipPoly) {
  let out = subject;
  const cp = ensureCCW(clipPoly);
  for (let i = 0; i < cp.length; i++) {
    const A = cp[i], B = cp[(i + 1) % cp.length];
    const input = out; out = [];
    for (let j = 0; j < input.length; j++) {
      const cur = input[j], prev = input[(j + input.length - 1) % input.length];
      const curIn = insideEdge(cur, A, B), prevIn = insideEdge(prev, A, B);
      if (curIn) { if (!prevIn) out.push(edgeInter(prev, cur, A, B)); out.push(cur); }
      else if (prevIn) out.push(edgeInter(prev, cur, A, B));
    }
    if (out.length === 0) return [];
  }
  return out;
}
export function overlapArea(a, b) {
  const c = clipConvex(ensureCCW(a), ensureCCW(b));
  return c.length < 3 ? 0 : area(c);
}

// ---- 聯集外輪廓（切邊 + 對消 + 串接）----
const keyPt = (p) => p[0].toFixed(4) + ',' + p[1].toFixed(4);
function onSegment(p, a, b) {
  const cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]);
  if (Math.abs(cross) > 1e-4) return false;
  const dot = (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1]);
  const len = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2;
  return dot > EPS && dot < len - EPS;
}
export function unionOutline(polys) {
  const verts = []; const seen = new Set();
  for (const poly of polys) for (const p of poly) {
    const k = keyPt(p); if (!seen.has(k)) { seen.add(k); verts.push(p); }
  }
  let segs = [];
  for (const poly of polys) {
    const cc = ensureCCW(poly);
    for (let i = 0; i < cc.length; i++) {
      const a = cc[i], b = cc[(i + 1) % cc.length];
      const mids = verts.filter((v) => onSegment(v, a, b))
        .sort((u, v) => ((u[0] - a[0]) ** 2 + (u[1] - a[1]) ** 2) - ((v[0] - a[0]) ** 2 + (v[1] - a[1]) ** 2));
      const chain = [a, ...mids, b];
      for (let j = 0; j < chain.length - 1; j++) segs.push([chain[j], chain[j + 1]]);
    }
  }
  const alive = segs.map(() => true);
  for (let i = 0; i < segs.length; i++) {
    if (!alive[i]) continue;
    for (let j = 0; j < segs.length; j++) {
      if (i === j || !alive[j]) continue;
      if (keyPt(segs[i][0]) === keyPt(segs[j][1]) && keyPt(segs[i][1]) === keyPt(segs[j][0])) {
        alive[i] = false; alive[j] = false; break;
      }
    }
  }
  const bnd = segs.filter((_, i) => alive[i]);
  if (bnd.length === 0) return null;
  const byStart = new Map();
  for (const s of bnd) { const k = keyPt(s[0]); if (!byStart.has(k)) byStart.set(k, []); byStart.get(k).push(s); }
  const start = bnd[0][0]; let cur = start; const loop = [start]; let guard = 0;
  while (guard++ < 2000) {
    const opts = byStart.get(keyPt(cur));
    if (!opts || opts.length === 0) break;
    const s = opts.shift(); const nxt = s[1];
    if (keyPt(nxt) === keyPt(start)) break;
    loop.push(nxt); cur = nxt;
  }
  // 移除共線點
  const clean = [];
  for (let i = 0; i < loop.length; i++) {
    const p = loop[(i + loop.length - 1) % loop.length], q = loop[i], r = loop[(i + 1) % loop.length];
    const cross = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]);
    if (Math.abs(cross) > 1e-4) clean.push(q);
  }
  return clean.length >= 3 ? clean : loop;
}

// 兩塊是否共享一段長度 > 0 的邊
export function sharesEdge(polyA, polyB) {
  const a = ensureCCW(polyA), b = ensureCCW(polyB);
  for (let i = 0; i < a.length; i++) {
    const a1 = a[i], a2 = a[(i + 1) % a.length];
    for (let j = 0; j < b.length; j++) {
      const b1 = b[j], b2 = b[(j + 1) % b.length];
      // 是否共線且有重疊段
      if (collinearOverlap(a1, a2, b1, b2)) return true;
    }
  }
  return false;
}
function collinearOverlap(a1, a2, b1, b2) {
  const d = [a2[0] - a1[0], a2[1] - a1[1]];
  const len2 = d[0] * d[0] + d[1] * d[1];
  if (len2 < EPS) return false;
  const online = (p) => {
    const cross = d[0] * (p[1] - a1[1]) - d[1] * (p[0] - a1[0]);
    return Math.abs(cross) < 1e-3;
  };
  if (!online(b1) || !online(b2)) return false;
  const proj = (p) => ((p[0] - a1[0]) * d[0] + (p[1] - a1[1]) * d[1]) / len2;
  let lo = Math.max(0, Math.min(proj(b1), proj(b2)));
  let hi = Math.min(1, Math.max(proj(b1), proj(b2)));
  return hi - lo > 1e-3;
}
