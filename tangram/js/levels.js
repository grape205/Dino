// levels.js — 關卡資料（每題解答皆已通過 validator.js 驗證）
// T1/T2/T3：solution = [{piece, verts}]，外輪廓由 geometry.unionOutline 自動導出
// T4：from / to / answer（移動的塊序號）
export const CHAPTERS = [
  { id: 1, name: '蛋巢區', emoji: '🥚', dino: '🦖', color: '#4caf50' },
  { id: 2, name: '蕨葉森林', emoji: '🌿', dino: '🦕', color: '#22c55e' },
  { id: 3, name: '草食龍谷', emoji: '🏞️', dino: '🦕', color: '#16a34a' },
  { id: 4, name: '化石挖掘場', emoji: '🦴', dino: '🦴', color: '#a16207' },
  { id: 5, name: '恐龍博物館', emoji: '🏛️', dino: '🦖', color: '#f59e0b' },
  { id: 6, name: '移動辨識', emoji: '🔍', dino: '🦎', color: '#ec4899' },
];

export const LEVELS = [
  // ── 第 1 章 蛋巢區（T1 彩色輔助）──
  { id: 1, chapter: 1, name: '第一顆蛋', type: 'T1', difficulty: 1, teach: '兩個小三角形可以合成一個正方形！',
    solution: [ { piece: 'ST_A', verts: [[0,2],[2,0],[4,2]] }, { piece: 'ST_B', verts: [[0,2],[4,2],[2,4]] } ] },
  { id: 2, chapter: 1, name: '尖尖山', type: 'T1', difficulty: 1, teach: '兩個小三角形也能合成一個中三角形。',
    solution: [ { piece: 'ST_A', verts: [[0,0],[4,0],[2,2]] }, { piece: 'ST_B', verts: [[0,0],[2,2],[0,4]] } ] },
  { id: 3, chapter: 1, name: '蛋窩', type: 'T1', difficulty: 1, teach: '斜斜地放，就變成平行四邊形。',
    solution: [ { piece: 'ST_A', verts: [[0,0],[4,0],[2,2]] }, { piece: 'ST_B', verts: [[4,0],[6,2],[2,2]] } ] },
  { id: 4, chapter: 1, name: '恐龍腳印', type: 'T1', difficulty: 2, teach: '不同形狀的塊也能拼在一起。',
    solution: [ { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] }, { piece: 'PG', verts: [[2,2],[6,2],[8,0],[4,0]] } ] },
  { id: 5, chapter: 1, name: '大山坡', type: 'T1', difficulty: 2, teach: '一塊中三角＋兩塊小三角＝大三角形。',
    solution: [ { piece: 'MT', verts: [[0,0],[4,0],[4,4]] }, { piece: 'ST_A', verts: [[4,0],[8,0],[6,2]] }, { piece: 'ST_B', verts: [[4,0],[6,2],[4,4]] } ] },

  // ── 第 2 章 蕨葉森林（T1→T2）──
  { id: 6, chapter: 2, name: '嫩芽', type: 'T1', difficulty: 2, teach: '正方形和小三角形做出一個小箭頭。',
    solution: [ { piece: 'SQ', verts: [[8,0],[10,2],[8,4],[6,2]] }, { piece: 'ST_A', verts: [[4,4],[6,2],[8,4]] } ] },
  { id: 7, chapter: 2, name: '蕨葉', type: 'T1', difficulty: 2, teach: '三塊拼出一個梯形。',
    solution: [ { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] } ] },
  { id: 8, chapter: 2, name: '小山丘', type: 'T2', difficulty: 2, teach: '沒有顏色也難不倒你！',
    solution: [ { piece: 'MT', verts: [[0,0],[0,4],[4,0]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] } ] },
  { id: 9, chapter: 2, name: '飛鏢', type: 'T2', difficulty: 3, teach: '大三角形是最大的一塊喔。',
    solution: [ { piece: 'LT_A', verts: [[0,0],[8,0],[4,4]] }, { piece: 'ST_A', verts: [[4,4],[6,2],[8,4]] }, { piece: 'MT', verts: [[4,4],[8,8],[8,4]] } ] },
  { id: 10, chapter: 2, name: '大帆', type: 'T2', difficulty: 3, teach: '兩個大三角形合成一個大三角形。',
    solution: [ { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] }, { piece: 'LT_B', verts: [[8,8],[8,0],[4,4]] } ] },

  // ── 第 3 章 草食龍谷（T2，4 塊）──
  { id: 11, chapter: 3, name: '梯形石', type: 'T2', difficulty: 3, teach: '四塊拼出一個大梯形。',
    solution: [ { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] }, { piece: 'PG', verts: [[2,2],[6,2],[8,0],[4,0]] } ] },
  { id: 12, chapter: 3, name: '山谷', type: 'T2', difficulty: 3, teach: '先放大塊，再補小塊。',
    solution: [ { piece: 'MT', verts: [[0,0],[0,4],[4,0]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] }, { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] } ] },
  { id: 13, chapter: 3, name: '小帆船', type: 'T2', difficulty: 3, teach: '平行四邊形只有它可以翻面。',
    solution: [ { piece: 'MT', verts: [[4,4],[8,8],[8,4]] }, { piece: 'SQ', verts: [[8,0],[10,2],[8,4],[6,2]] }, { piece: 'ST_A', verts: [[4,4],[6,2],[8,4]] }, { piece: 'PG', verts: [[8,4],[8,8],[10,6],[10,2]] } ] },
  { id: 14, chapter: 3, name: '高塔', type: 'T2', difficulty: 4, teach: '大三角形當底座最穩。',
    solution: [ { piece: 'LT_A', verts: [[0,0],[8,0],[4,4]] }, { piece: 'MT', verts: [[4,4],[8,8],[8,4]] }, { piece: 'ST_A', verts: [[4,4],[6,2],[8,4]] }, { piece: 'SQ', verts: [[8,0],[10,2],[8,4],[6,2]] } ] },

  // ── 第 4 章 化石挖掘場（T2→T3，5–6 塊）──
  { id: 15, chapter: 4, name: '大梯形', type: 'T2', difficulty: 4, teach: '五塊也要一步一步來。',
    solution: [ { piece: 'MT', verts: [[0,0],[0,4],[4,0]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] }, { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] }, { piece: 'LT_B', verts: [[8,8],[8,0],[4,4]] } ] },
  { id: 16, chapter: 4, name: '長船', type: 'T2', difficulty: 4, teach: '慢慢對齊每一條邊。',
    solution: [ { piece: 'MT', verts: [[4,4],[8,8],[8,4]] }, { piece: 'SQ', verts: [[8,0],[10,2],[8,4],[6,2]] }, { piece: 'ST_A', verts: [[4,4],[6,2],[8,4]] }, { piece: 'PG', verts: [[8,4],[8,8],[10,6],[10,2]] }, { piece: 'ST_B', verts: [[10,6],[12,4],[10,2]] } ] },
  { id: 17, chapter: 4, name: '恐龍山', type: 'T3', difficulty: 4, teach: '只有外框線，靠自己想！',
    solution: [ { piece: 'LT_A', verts: [[0,0],[8,0],[4,4]] }, { piece: 'LT_B', verts: [[8,0],[16,0],[12,4]] }, { piece: 'SQ', verts: [[8,0],[10,2],[8,4],[6,2]] }, { piece: 'ST_A', verts: [[4,4],[6,2],[8,4]] }, { piece: 'MT', verts: [[4,4],[8,8],[8,4]] } ] },
  { id: 18, chapter: 4, name: '六塊拼圖', type: 'T3', difficulty: 5, teach: '六塊的大挑戰！',
    solution: [ { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] }, { piece: 'LT_B', verts: [[8,8],[8,0],[4,4]] }, { piece: 'MT', verts: [[0,0],[0,4],[4,0]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] } ] },

  // ── 第 5 章 恐龍博物館（T3，7 塊大師關）──
  { id: 19, chapter: 5, name: '恐龍方塊', type: 'T3', difficulty: 5, teach: '完整七巧板：大正方形！',
    solution: [ { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] }, { piece: 'LT_B', verts: [[8,8],[8,0],[4,4]] }, { piece: 'MT', verts: [[0,0],[0,4],[4,0]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] }, { piece: 'PG', verts: [[2,2],[6,2],[8,0],[4,0]] } ] },
  { id: 20, chapter: 5, name: '恐龍尖山', type: 'T3', difficulty: 5, teach: '完整七巧板：大三角形！',
    solution: [ { piece: 'LT_A', verts: [[0,0],[8,0],[4,4]] }, { piece: 'LT_B', verts: [[8,0],[16,0],[12,4]] }, { piece: 'MT', verts: [[4,4],[8,8],[8,4]] }, { piece: 'SQ', verts: [[8,0],[10,2],[8,4],[6,2]] }, { piece: 'ST_A', verts: [[4,4],[6,2],[8,4]] }, { piece: 'ST_B', verts: [[10,6],[12,4],[10,2]] }, { piece: 'PG', verts: [[8,4],[8,8],[10,6],[10,2]] } ] },

  // ── 第 6 章 移動辨識（T4）──
  { id: 21, chapter: 6, name: '一步之遙', type: 'T4', difficulty: 4, teach: '先找出「沒有動」的塊，剩下的就是答案！', answer: [4],
    from: [ { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] }, { piece: 'LT_B', verts: [[8,8],[8,0],[4,4]] }, { piece: 'MT', verts: [[0,0],[0,4],[4,0]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] }, { piece: 'PG', verts: [[2,2],[6,2],[8,0],[4,0]] } ],
    to:   [ { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] }, { piece: 'LT_B', verts: [[8,8],[8,0],[4,4]] }, { piece: 'MT', verts: [[0,0],[0,4],[4,0]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[-2,6]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] }, { piece: 'PG', verts: [[2,2],[6,2],[8,0],[4,0]] } ] },
  { id: 22, chapter: 6, name: '兩步挑戰', type: 'T4', difficulty: 5, teach: '這次有兩塊搬家了，找找看！', answer: [3, 4],
    from: [ { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] }, { piece: 'LT_B', verts: [[8,8],[8,0],[4,4]] }, { piece: 'MT', verts: [[0,0],[0,4],[4,0]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[2,6]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] }, { piece: 'PG', verts: [[2,2],[6,2],[8,0],[4,0]] } ],
    to:   [ { piece: 'LT_A', verts: [[0,8],[8,8],[4,4]] }, { piece: 'LT_B', verts: [[8,8],[8,0],[4,4]] }, { piece: 'MT', verts: [[0,0],[0,-4],[4,0]] }, { piece: 'ST_A', verts: [[0,4],[0,8],[-2,6]] }, { piece: 'SQ', verts: [[0,4],[2,6],[4,4],[2,2]] }, { piece: 'ST_B', verts: [[2,2],[4,4],[6,2]] }, { piece: 'PG', verts: [[2,2],[6,2],[8,0],[4,0]] } ] },
];
