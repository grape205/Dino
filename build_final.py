"""
Build all 50 levels using optimized BFS solver.
"""
import sys, random, json, time
sys.path.insert(0, '/home/user/Dino')
from solver_fast import solve_fast as solve, make_piece, LEVELS as BASE_LEVELS

t_start = time.time()

def build_lv(cols, rows, exitRow, pieces_def, name, icon):
    pieces = [make_piece(pid, pt, r, c, l, d) for pid,pt,r,c,l,d in pieces_def]
    lv = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,'name':name,'icon':icon,'pieces':pieces}
    result = solve(lv)
    lv['par'] = result
    return lv, result

def random_level(target_par, cols, rows, exitRow=2, max_tries=50000, seed_base=0):
    rng = random.Random(seed_base)
    for attempt in range(max_tries):
        grid = [[False]*cols for _ in range(rows)]
        tx_col = 0 if rng.random() < 0.7 else 1
        # ensure T-Rex fits
        if tx_col + 2 > cols: tx_col = 0
        for i in range(2): grid[exitRow][tx_col+i] = True
        pdef = [('tx','t',exitRow,tx_col,2,'H')]

        n_pieces = rng.randint(3, min(9, cols*rows//3))
        cnts = {}
        bad = False
        for _ in range(n_pieces):
            pt = rng.choice(['r','r','r','c','c','b','e'])
            plen = 3 if pt=='b' else (1 if pt=='e' else 2)
            pdir = rng.choice(['H','V']) if pt!='e' else 'H'
            ok2 = False
            for __ in range(300):
                if pdir=='H':
                    r_=rng.randint(0,rows-1); c_=rng.randint(0,cols-plen)
                    cells=[(r_,c_+i) for i in range(plen)]
                else:
                    r_=rng.randint(0,rows-plen); c_=rng.randint(0,cols-1)
                    cells=[(r_+i,c_) for i in range(plen)]
                if all(not grid[rr][cc] for rr,cc in cells):
                    for rr,cc in cells: grid[rr][cc]=True
                    cnts[pt]=cnts.get(pt,0)+1
                    pdef.append((f"{pt}{cnts[pt]}",pt,r_,c_,plen,pdir))
                    ok2=True; break
            if not ok2: bad=True; break
        if bad: continue
        test={'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,'name':'t','icon':'🦕',
              'pieces':[make_piece(pid,pt,r,c,l,d) for pid,pt,r,c,l,d in pdef]}
        res=solve(test)
        if res==target_par:
            return pdef, res
    return None, -1

icons=['🦕','🦖','🐊','🦎','⭐','🏆','👑']
def icon_for(n): return icons[n%len(icons)]

names={
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

ALL = list(BASE_LEVELS)
print("Levels 1-6 (existing):")
for i, lv in enumerate(ALL):
    print(f"  Lv{i+1}: BFS={lv['par']}")

# Level spec: (lv_num, cols, rows, exitRow, target_par, seed_base)
level_specs = [
    # 5x5 levels (7-15), par 4-7
    (7,  5,5,2, 4,  10007),
    (8,  5,5,1, 4,  10008),
    (9,  5,5,2, 5,  10009),
    (10, 5,5,1, 5,  10010),
    (11, 5,5,2, 5,  10011),
    (12, 5,5,2, 6,  10012),
    (13, 5,5,1, 6,  10013),
    (14, 5,5,2, 6,  10014),
    (15, 5,5,2, 7,  10015),
    # 6x6 levels (16-50)
    (16, 6,6,2, 5,  10016),
    (17, 6,6,2, 5,  10017),
    (18, 6,6,2, 6,  10018),
    (19, 6,6,3, 6,  10019),
    (20, 6,6,2, 6,  10020),
    (21, 6,6,2, 7,  10021),
    (22, 6,6,3, 7,  10022),
    (23, 6,6,2, 7,  10023),
    (24, 6,6,3, 8,  10024),
    (25, 6,6,2, 8,  10025),
    (26, 6,6,3, 7,  10026),
    (27, 6,6,2, 8,  10027),
    (28, 6,6,3, 8,  10028),
    (29, 6,6,2, 8,  10029),
    (30, 6,6,3, 9,  10030),
    (31, 6,6,2, 9,  10031),
    (32, 6,6,3, 9,  10032),
    (33, 6,6,2, 9,  10033),
    (34, 6,6,3,10,  10034),
    (35, 6,6,2,10,  10035),
    (36, 6,6,3, 9,  10036),
    (37, 6,6,2,10,  10037),
    (38, 6,6,3,10,  10038),
    (39, 6,6,2,10,  10039),
    (40, 6,6,3,11,  10040),
    (41, 6,6,2,11,  10041),
    (42, 6,6,3,11,  10042),
    (43, 6,6,2,12,  10043),
    (44, 6,6,3,12,  10044),
    (45, 6,6,2,12,  10045),
    (46, 6,6,3,11,  10046),
    (47, 6,6,2,12,  10047),
    (48, 6,6,3,12,  10048),
    (49, 6,6,2,13,  10049),
    (50, 6,6,3,14,  10050),
]

print("\nBuilding levels 7-50...")
for lv_num, cols, rows, exitRow, target, seed_base in level_specs:
    name = names[lv_num]
    icon = icon_for(lv_num-7)

    pdef = None
    actual_par = -1

    # Try exact target first
    pdef, actual_par = random_level(target, cols, rows, exitRow, max_tries=80000, seed_base=seed_base)

    if pdef is None:
        # Try nearby pars (accept within ±2)
        for delta in [1, -1, 2, -2, 3, -3]:
            alt = target + delta
            if alt < 1: continue
            pdef, actual_par = random_level(alt, cols, rows, exitRow, max_tries=30000, seed_base=seed_base+delta*1000)
            if pdef is not None:
                break

    if pdef is not None:
        lv2, p2 = build_lv(cols, rows, exitRow, pdef, name, icon)
        ALL.append(lv2)
        elapsed = time.time() - t_start
        print(f"  Lv{lv_num:2d} {name}: BFS={p2} pieces={len(pdef)} ({elapsed:.1f}s)")
    else:
        print(f"  Lv{lv_num:2d} {name}: FAILED (target={target})")

print(f"\nTotal levels: {len(ALL)}")

# Verify all
print("\n=== Verification ===")
all_ok = True
for i, lv in enumerate(ALL):
    par = lv.get('par', -1)
    ok = par >= 1
    if not ok:
        all_ok = False
        print(f"  Lv{i+1:2d} FAIL par={par}")

print(f"All {len(ALL)} levels solvable: {all_ok}")

if len(ALL) == 50 and all_ok:
    with open('/home/user/Dino/levels_data.json', 'w') as f:
        json.dump(ALL, f, ensure_ascii=False, indent=2)
    print("Saved to levels_data.json")
else:
    print(f"WARNING: Only {len(ALL)} levels or some unsolvable. Check output.")
    with open('/home/user/Dino/levels_data.json', 'w') as f:
        json.dump(ALL, f, ensure_ascii=False, indent=2)
    print("Partial save to levels_data.json")
