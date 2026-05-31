import sys, random
sys.path.insert(0, '/home/user/Dino')
from solver import solve, make_piece, LEVELS as BASE_LEVELS

random.seed(42)

# ─── helpers ────────────────────────────────────────────────────────────────

def build_lv(cols, rows, exitRow, pieces_def, name, icon):
    pieces = [make_piece(pid, pt, r, c, l, d) for pid,pt,r,c,l,d in pieces_def]
    lv = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,'name':name,'icon':icon,'pieces':pieces}
    result = solve(lv)
    lv['par'] = result
    return lv, result

def random_6x6(target_par, exitRow=2, max_tries=30000, seed_offset=0):
    rng = random.Random(42 + seed_offset)
    cols, rows = 6, 6
    for attempt in range(max_tries):
        grid = [[False]*cols for _ in range(rows)]
        tx_col = rng.choice([0, 1])
        for i in range(2):
            grid[exitRow][tx_col+i] = True
        pdef = [('tx','t',exitRow,tx_col,2,'H')]

        n_pieces = rng.randint(3, 8)
        cnts = {}
        bad = False
        for _ in range(n_pieces):
            pt = rng.choice(['r','r','r','c','c','c','b','e'])
            plen = 3 if pt=='b' else (1 if pt=='e' else 2)
            pdir = rng.choice(['H','V']) if pt not in ('e',) else 'H'
            ok2 = False
            for __ in range(150):
                if pdir == 'H':
                    r = rng.randint(0, rows-1)
                    c = rng.randint(0, cols-plen)
                    cells = [(r,c+i) for i in range(plen)]
                else:
                    r = rng.randint(0, rows-plen)
                    c = rng.randint(0, cols-1)
                    cells = [(r+i,c) for i in range(plen)]
                if all(not grid[rr][cc] for rr,cc in cells):
                    for rr,cc in cells: grid[rr][cc]=True
                    cnts[pt] = cnts.get(pt,0)+1
                    pid = f"{pt}{cnts[pt]}" if pt!='tx' else 'tx'
                    pdef.append((pid,pt,r,c,plen,pdir))
                    ok2=True; break
            if not ok2: bad=True; break
        if bad: continue

        test = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,'name':'t','icon':'🦕',
                'pieces':[make_piece(pid,pt,r,c,l,d) for pid,pt,r,c,l,d in pdef]}
        res = solve(test)
        if res == target_par:
            return pdef, res
    return None, -1

icons = ['🦕','🦖','🐊','🦎','⭐','🏆','👑']
def icon_for(n): return icons[n % len(icons)]

names = {
    7:'初學者',8:'恐龍迷',9:'小探險家',10:'冒險開始',
    11:'越來越難',12:'動動腦筋',13:'挑戰開始',14:'恐龍博士',15:'智力測驗',
    16:'進階玩家',17:'高手之路',18:'恐龍達人',19:'頭腦體操',20:'解謎高手',
    21:'思考訓練',22:'推理高手',23:'智慧勇士',24:'腦力激盪',25:'謎題挑戰',
    26:'困難模式',27:'超難挑戰',28:'恐龍難題',29:'腦筋急轉',30:'智力競賽',
    31:'困難關卡',32:'超級難關',33:'極限挑戰',34:'恐龍勇者',35:'邏輯大師',
    36:'恐龍天才',37:'超級大腦',38:'最強挑戰',39:'傳奇玩家',40:'恐龍霸主',
    41:'傳說開始',42:'史詩難題',43:'頂尖高手',44:'終極挑戰',45:'恐龍王者',
    46:'最強大腦',47:'恐龍傳說',48:'無敵挑戰',49:'終極難關',50:'恐龍冠軍',
}

ALL = list(BASE_LEVELS)  # lv1-6 already verified

# ─── Levels 7-15: 5x5, par 4-7 ────────────────────────────────────────────

# Lv7: 5x5 exitRow=2 par=4
# c1 left 2 -> r1 up -> r2 up -> T
lv, p = build_lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),
    ('c1','c',0,2,2,'H'),
], names[7], icon_for(0))
ALL.append(lv); print(f"Lv7  BFS={p}")

# Lv8: 5x5 exitRow=2 par=4
# Three V blockers, c1 covers col3-4, e1 at col2
# c1 left -> r1b up (using egg blocks) actually let's verify
lv, p = build_lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),
    ('c1','c',0,3,2,'H'),('e1','e',0,2,1,'H'),
], names[8], icon_for(1))
ALL.append(lv); print(f"Lv8  BFS={p}")

# Lv9: 5x5 exitRow=2 par=5
lv, p = build_lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),('r2','r',2,3,2,'V'),('r3','r',2,4,2,'V'),
    ('c1','c',1,3,2,'H'),('e1','e',0,2,1,'H'),('e2','e',4,3,1,'H'),
], names[9], icon_for(2))
ALL.append(lv); print(f"Lv9  BFS={p}")

# Lv10: 5x5 exitRow=2 par=5
lv, p = build_lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),
    ('c1','c',0,1,2,'H'),('c2','c',0,3,2,'H'),
], names[10], icon_for(3))
ALL.append(lv); print(f"Lv10 BFS={p}")

# Lv11: 5x5 exitRow=1 par=5
lv, p = build_lv(5,5,1,[
    ('tx','t',1,0,2,'H'),
    ('r1','r',0,2,2,'V'),('r2','r',0,3,2,'V'),('r3','r',0,4,2,'V'),
    ('c1','c',2,2,2,'H'),
], names[11], icon_for(4))
ALL.append(lv); print(f"Lv11 BFS={p}")

# Lv12: 5x5 exitRow=2 par~6
lv, p = build_lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),
    ('c1','c',0,1,2,'H'),('c2','c',0,3,2,'H'),
    ('e1','e',3,4,1,'H'),
], names[12], icon_for(5))
ALL.append(lv); print(f"Lv12 BFS={p}")

# Lv13: 5x5 exitRow=2 par~6
lv, p = build_lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),('c2','c',0,4,2,'V'),
    ('e1','e',3,2,1,'H'),
], names[13], icon_for(6))
ALL.append(lv); print(f"Lv13 BFS={p}")

# Lv14: 5x5 exitRow=2 par~6-7
lv, p = build_lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),('c2','c',3,3,2,'H'),
    ('e1','e',0,4,1,'H'),('e2','e',3,2,1,'H'),
], names[14], icon_for(0))
ALL.append(lv); print(f"Lv14 BFS={p}")

# Lv15: 5x5 exitRow=2 par~7
lv, p = build_lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),('c2','c',3,2,2,'H'),
    ('r4','r',3,4,2,'V'),('e1','e',0,4,1,'H'),
], names[15], icon_for(1))
ALL.append(lv); print(f"Lv15 BFS={p}")

print()
print("=== 6x6 levels (16-50) via random search ===")

# Target par ranges:
# 16-25: par 5-8
# 26-35: par 7-10
# 36-45: par 9-12
# 46-50: par 11-14

level_targets = [
    # (lv_num, exitRow, target_par, seed_offset)
    (16, 2, 5, 0),
    (17, 2, 5, 1),
    (18, 2, 6, 2),
    (19, 2, 6, 3),
    (20, 3, 6, 4),
    (21, 2, 7, 5),
    (22, 2, 7, 6),
    (23, 3, 7, 7),
    (24, 2, 8, 8),
    (25, 3, 8, 9),
    (26, 2, 7, 10),
    (27, 3, 8, 11),
    (28, 2, 8, 12),
    (29, 3, 8, 13),
    (30, 2, 9, 14),
    (31, 3, 9, 15),
    (32, 2, 9, 16),
    (33, 3, 9, 17),
    (34, 2, 10, 18),
    (35, 3, 10, 19),
    (36, 2, 9, 20),
    (37, 3, 10, 21),
    (38, 2, 10, 22),
    (39, 3, 10, 23),
    (40, 2, 11, 24),
    (41, 3, 11, 25),
    (42, 2, 11, 26),
    (43, 3, 12, 27),
    (44, 2, 12, 28),
    (45, 3, 12, 29),
    (46, 2, 11, 30),
    (47, 3, 12, 31),
    (48, 2, 12, 32),
    (49, 3, 13, 33),
    (50, 2, 13, 34),
]

for lv_num, exitRow, target, seed_off in level_targets:
    name = names[lv_num]
    icon = icon_for(lv_num - 7)
    # Try increasing max_tries based on difficulty
    tries = 20000 if target <= 9 else 30000
    pdef, found = random_6x6(target, exitRow, max_tries=tries, seed_offset=seed_off)
    if pdef is not None:
        lv2, p2 = build_lv(6, 6, exitRow, pdef, name, icon)
        ALL.append(lv2)
        print(f"Lv{lv_num:2d} {name}: BFS={p2} pieces={len(pdef)}")
    else:
        # Fallback: search nearby pars
        found_fallback = False
        for alt_par in [target-1, target+1, target-2, target+2]:
            if alt_par < 1: continue
            pdef2, found2 = random_6x6(alt_par, exitRow, max_tries=10000, seed_offset=seed_off+100)
            if pdef2 is not None:
                lv2, p2 = build_lv(6, 6, exitRow, pdef2, name, icon)
                ALL.append(lv2)
                print(f"Lv{lv_num:2d} {name}: BFS={p2} (fallback from {target}) pieces={len(pdef2)}")
                found_fallback = True
                break
        if not found_fallback:
            print(f"Lv{lv_num:2d} {name}: FAILED to find level for target={target}")

print(f"\nTotal levels built: {len(ALL)}")
if len(ALL) == 50:
    print("SUCCESS: All 50 levels built!")
    # Save results
    import json
    with open('/home/user/Dino/levels_data.json', 'w') as f:
        json.dump(ALL, f, ensure_ascii=False, indent=2)
    print("Saved to levels_data.json")
else:
    print(f"WARNING: Only {len(ALL)} levels. Missing {50-len(ALL)}.")
