"""
Build all 50 levels using random search for all of levels 7-50.
This avoids hand-crafting errors.
"""
import sys, random, json
sys.path.insert(0, '/home/user/Dino')
from solver import solve, make_piece, LEVELS as BASE_LEVELS

# ─── helpers ─────────────────────────────────────────────────────────────────

def build_lv(cols, rows, exitRow, pieces_def, name, icon):
    pieces = [make_piece(pid, pt, r, c, l, d) for pid,pt,r,c,l,d in pieces_def]
    lv = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,'name':name,'icon':icon,'pieces':pieces}
    result = solve(lv)
    lv['par'] = result
    return lv, result

def random_nxn(target_par, cols, rows, exitRow=2, max_tries=30000, seed_base=0):
    rng = random.Random(seed_base + target_par * 31 + exitRow * 7)
    for attempt in range(max_tries):
        grid = [[False]*cols for _ in range(rows)]
        tx_col = rng.choice([0, 0, 1])
        for i in range(2): grid[exitRow][tx_col+i] = True
        pdef = [('tx','t',exitRow,tx_col,2,'H')]

        n_pieces = rng.randint(3, 9 if cols==6 else 6)
        cnts = {}
        bad = False
        for _ in range(n_pieces):
            pt = rng.choice(['r','r','r','c','c','b','e'])
            plen = 3 if pt=='b' else (1 if pt=='e' else 2)
            pdir = rng.choice(['H','V']) if pt!='e' else 'H'
            ok2 = False
            for __ in range(200):
                if pdir=='H':
                    r=rng.randint(0,rows-1); c=rng.randint(0,cols-plen)
                    cells=[(r,c+i) for i in range(plen)]
                else:
                    r=rng.randint(0,rows-plen); c=rng.randint(0,cols-1)
                    cells=[(r+i,c) for i in range(plen)]
                if all(not grid[rr][cc] for rr,cc in cells):
                    for rr,cc in cells: grid[rr][cc]=True
                    cnts[pt]=cnts.get(pt,0)+1
                    pdef.append((f"{pt}{cnts[pt]}",pt,r,c,plen,pdir))
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

ALL = list(BASE_LEVELS)  # lv1-6

# ─── Levels 7-15: 5x5, par 4-7 ────────────────────────────────────────────
print("Building 5x5 levels 7-15...")

# Target pars: 7->4, 8->4, 9->5, 10->5, 11->5, 12->6, 13->6, 14->6, 15->7
targets_5x5 = [
    (7,  5,5,2, 4,  0),
    (8,  5,5,1, 4,  100),
    (9,  5,5,2, 5,  200),
    (10, 5,5,1, 5,  300),
    (11, 5,5,2, 5,  400),
    (12, 5,5,2, 6,  500),
    (13, 5,5,1, 6,  600),
    (14, 5,5,2, 6,  700),
    (15, 5,5,2, 7,  800),
]

for lv_num, cols, rows, exitRow, target, seed_base in targets_5x5:
    name = names[lv_num]
    icon = icon_for(lv_num-7)
    found = False
    for seed_off in range(50):
        pdef, res = random_nxn(target, cols, rows, exitRow, max_tries=15000, seed_base=seed_base+seed_off*37)
        if pdef is not None:
            lv2, p2 = build_lv(cols, rows, exitRow, pdef, name, icon)
            ALL.append(lv2)
            print(f"  Lv{lv_num} {name}: BFS={p2} pieces={len(pdef)}")
            found = True
            break
    if not found:
        # Accept nearby par
        for delta in [1, -1, 2, -2]:
            alt = target + delta
            if alt < 1: continue
            for seed_off in range(20):
                pdef, res = random_nxn(alt, cols, rows, exitRow, max_tries=10000, seed_base=seed_base+seed_off*19+1000)
                if pdef is not None:
                    lv2, p2 = build_lv(cols, rows, exitRow, pdef, name, icon)
                    ALL.append(lv2)
                    print(f"  Lv{lv_num} {name}: BFS={p2} (target was {target})")
                    found = True
                    break
            if found: break
        if not found:
            print(f"  Lv{lv_num} {name}: FAILED")

print(f"Built {len(ALL)} levels so far")

# ─── Levels 16-50: 6x6 ────────────────────────────────────────────────────
print("\nBuilding 6x6 levels 16-50...")

targets_6x6 = [
    (16, 6,6,2, 5,  1000),
    (17, 6,6,2, 5,  1100),
    (18, 6,6,2, 6,  1200),
    (19, 6,6,3, 6,  1300),
    (20, 6,6,2, 6,  1400),
    (21, 6,6,2, 7,  1500),
    (22, 6,6,3, 7,  1600),
    (23, 6,6,2, 7,  1700),
    (24, 6,6,3, 8,  1800),
    (25, 6,6,2, 8,  1900),
    (26, 6,6,3, 7,  2000),
    (27, 6,6,2, 8,  2100),
    (28, 6,6,3, 8,  2200),
    (29, 6,6,2, 8,  2300),
    (30, 6,6,3, 9,  2400),
    (31, 6,6,2, 9,  2500),
    (32, 6,6,3, 9,  2600),
    (33, 6,6,2, 9,  2700),
    (34, 6,6,3, 10, 2800),
    (35, 6,6,2, 10, 2900),
    (36, 6,6,3, 9,  3000),
    (37, 6,6,2, 10, 3100),
    (38, 6,6,3, 10, 3200),
    (39, 6,6,2, 10, 3300),
    (40, 6,6,3, 11, 3400),
    (41, 6,6,2, 11, 3500),
    (42, 6,6,3, 11, 3600),
    (43, 6,6,2, 12, 3700),
    (44, 6,6,3, 12, 3800),
    (45, 6,6,2, 12, 3900),
    (46, 6,6,3, 11, 4000),
    (47, 6,6,2, 12, 4100),
    (48, 6,6,3, 12, 4200),
    (49, 6,6,2, 13, 4300),
    (50, 6,6,3, 14, 4400),
]

for lv_num, cols, rows, exitRow, target, seed_base in targets_6x6:
    name = names[lv_num]
    icon = icon_for(lv_num-7)
    found = False
    for seed_off in range(30):
        pdef, res = random_nxn(target, cols, rows, exitRow, max_tries=30000, seed_base=seed_base+seed_off*41)
        if pdef is not None:
            lv2, p2 = build_lv(cols, rows, exitRow, pdef, name, icon)
            ALL.append(lv2)
            print(f"  Lv{lv_num} {name}: BFS={p2} pieces={len(pdef)}")
            found = True
            break
    if not found:
        for delta in [1, -1, 2, -2, 3, -3]:
            alt = target + delta
            if alt < 1: continue
            for seed_off in range(15):
                pdef, res = random_nxn(alt, cols, rows, exitRow, max_tries=15000, seed_base=seed_base+seed_off*23+5000)
                if pdef is not None:
                    lv2, p2 = build_lv(cols, rows, exitRow, pdef, name, icon)
                    ALL.append(lv2)
                    print(f"  Lv{lv_num} {name}: BFS={p2} (target was {target})")
                    found = True
                    break
            if found: break
        if not found:
            print(f"  Lv{lv_num} {name}: FAILED")

print(f"\nFinal count: {len(ALL)} levels")

# Verify
print("\n=== Verification ===")
all_ok = True
for i, lv in enumerate(ALL):
    par = lv.get('par', -1)
    ok = par >= 1
    if not ok: all_ok = False
    print(f"  Lv{i+1:2d} {lv.get('name','?'):10s} {lv['cols']}x{lv['rows']} exitRow={lv['exitRow']} par={par} {'OK' if ok else 'FAIL'}")
print(f"\nAll solvable: {all_ok}, Total: {len(ALL)}")

# Save
with open('/home/user/Dino/levels_data.json', 'w') as f:
    json.dump(ALL, f, ensure_ascii=False, indent=2)
print("Saved to /home/user/Dino/levels_data.json")
