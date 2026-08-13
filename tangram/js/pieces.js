// pieces.js — 七塊板定義（局部座標，單位：基準正方形邊長 8）
// 代號對照：LT_A=① LT_B=② MT=③ ST_A=④ ST_B=⑤ SQ=⑥ PG=⑦
export const PIECES = {
  LT_A: { symbol: '①', name: '大三角形', num: 1, verts: [[0, 0], [8, 0], [4, 4]], color: '#ef4444', flippable: false },
  LT_B: { symbol: '②', name: '大三角形', num: 2, verts: [[0, 0], [8, 0], [4, 4]], color: '#3b82f6', flippable: false },
  MT:   { symbol: '③', name: '中三角形', num: 3, verts: [[0, 0], [4, 0], [0, 4]], color: '#22c55e', flippable: false },
  ST_A: { symbol: '④', name: '小三角形', num: 4, verts: [[0, 0], [4, 0], [2, 2]], color: '#f59e0b', flippable: false },
  ST_B: { symbol: '⑤', name: '小三角形', num: 5, verts: [[0, 0], [4, 0], [2, 2]], color: '#a855f7', flippable: false },
  SQ:   { symbol: '⑥', name: '正方形',   num: 6, verts: [[2, 0], [4, 2], [2, 4], [0, 2]], color: '#eab308', flippable: false },
  PG:   { symbol: '⑦', name: '平行四邊形', num: 7, verts: [[0, 0], [4, 0], [6, 2], [2, 2]], color: '#ec4899', flippable: true },
};

export const PIECE_ORDER = ['LT_A', 'LT_B', 'MT', 'ST_A', 'ST_B', 'SQ', 'PG'];
export const NUM_TO_KEY = { 1: 'LT_A', 2: 'LT_B', 3: 'MT', 4: 'ST_A', 5: 'ST_B', 6: 'SQ', 7: 'PG' };
export const SYMBOLS = ['', '①', '②', '③', '④', '⑤', '⑥', '⑦'];
