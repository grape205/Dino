// validator.js — 關卡驗證器（§5）
import { area, overlapArea, unionOutline, vertsEqualSet, sharesEdge, centroid, EPS } from './geometry.js';
import { PIECES } from './pieces.js';

// 驗證一組已放置的塊（{piece, verts}）是否構成合法拼圖
export function validateSolution(placed, outline) {
  const errors = [];
  const polys = placed.map((p) => p.verts);

  // 1. 面積守恆
  const pieceArea = polys.reduce((s, p) => s + area(p), 0);
  const derived = outline || unionOutline(polys);
  const outArea = derived ? area(derived) : NaN;
  if (!isFinite(outArea)) errors.push('無法計算外輪廓');
  else if (Math.abs(pieceArea - outArea) > 1e-2)
    errors.push(`面積不守恆：塊=${pieceArea.toFixed(2)}，輪廓=${outArea.toFixed(2)}`);

  // 2. 無重疊
  let maxOv = 0;
  for (let i = 0; i < polys.length; i++)
    for (let j = i + 1; j < polys.length; j++)
      maxOv = Math.max(maxOv, overlapArea(polys[i], polys[j]));
  if (maxOv > 1e-2) errors.push(`有重疊，最大交集面積=${maxOv.toFixed(3)}`);

  // 5. 邊接合：每塊至少與另一塊共享一段邊（單塊除外）
  if (polys.length > 1) {
    for (let i = 0; i < polys.length; i++) {
      let touch = false;
      for (let j = 0; j < polys.length; j++) {
        if (i === j) continue;
        if (sharesEdge(polys[i], polys[j])) { touch = true; break; }
      }
      if (!touch) { errors.push(`第 ${i + 1} 塊只有點接觸或分離`); break; }
    }
  }

  return { ok: errors.length === 0, errors, outline: derived, area: pieceArea };
}

// T4：from / to 各自合法，answer = 位置不同的塊集合
export function validateT4(from, to) {
  const errors = [];
  const idOf = (arr) => arr.map((p) => p.piece);
  // 無重疊檢查
  const noOverlap = (arr) => {
    let m = 0;
    for (let i = 0; i < arr.length; i++)
      for (let j = i + 1; j < arr.length; j++)
        m = Math.max(m, overlapArea(arr[i].verts, arr[j].verts));
    return m;
  };
  if (noOverlap(from) > 1e-2) errors.push('from 有重疊');
  if (noOverlap(to) > 1e-2) errors.push('to 有重疊');
  if (idOf(from).sort().join() !== idOf(to).sort().join()) errors.push('from/to 使用的塊不一致');

  const moved = [];
  for (const f of from) {
    const t = to.find((x) => x.piece === f.piece);
    if (!t) continue;
    if (!vertsEqualSet(f.verts, t.verts, 1e-3)) moved.push(PIECES[f.piece].num);
  }
  return { ok: errors.length === 0, errors, answer: moved.sort((a, b) => a - b) };
}
