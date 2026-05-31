"""
Continue building levels 31-50 using targeted random search.
For high-par levels, use a smarter construction: start with a known
solvable base and add pieces to increase complexity.
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

def random_6x6(target_par, exitRow=2, max_tries=20000, seed_offset=0):
    rng = random.Random(42 + seed_offset * 97 + target_par * 13)
    cols, rows = 6, 6
    for attempt in range(max_tries):
        grid = [[False]*cols for _ in range(rows)]
        tx_col = rng.choice([0, 1])
        for i in range(2): grid[exitRow][tx_col+i] = True
        pdef = [('tx','t',exitRow,tx_col,2,'H')]

        n_pieces = rng.randint(4, 9)
        cnts = {}
        bad = False
        for _ in range(n_pieces):
            pt = rng.choice(['r','r','r','c','c','b','b','e'])
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
    return None,-1

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

# ─── Pre-built levels 1-15 ───────────────────────────────────────────────────

ALL = list(BASE_LEVELS)

# Lv7: par=4 (c1 left 2 -> r1 up -> r2 up -> T)
lv,p = build_lv(5,5,2,[('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('c1','c',0,2,2,'H')], names[7],icon_for(0))
assert p==4, f"Lv7 got {p}"; ALL.append(lv)

# Lv8: par=4 (e1 at col2 row0, c1 covers col3-4, then r1 up then r2 r3 up)
lv,p = build_lv(5,5,2,[('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,3,2,'H'),('e1','e',0,2,1,'H')], names[8],icon_for(1))
assert p==4, f"Lv8 got {p}"; ALL.append(lv)

# Lv9: par=5
lv,p = build_lv(5,5,2,[('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',2,3,2,'V'),('r3','r',2,4,2,'V'),('c1','c',1,3,2,'H'),('e1','e',0,2,1,'H'),('e2','e',4,3,1,'H')], names[9],icon_for(2))
assert p==5, f"Lv9 got {p}"; ALL.append(lv)

# Lv10: par=5 (two H blockers)
lv,p = build_lv(5,5,2,[('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,1,2,'H'),('c2','c',0,3,2,'H')], names[10],icon_for(3))
assert p==5, f"Lv10 got {p}"; ALL.append(lv)

# Lv11: par=5 (exitRow=1)
lv,p = build_lv(5,5,1,[('tx','t',1,0,2,'H'),('r1','r',0,2,2,'V'),('r2','r',0,3,2,'V'),('r3','r',0,4,2,'V'),('c1','c',2,2,2,'H')], names[11],icon_for(4))
assert p==5, f"Lv11 got {p}"; ALL.append(lv)

# Lv12: par=6
lv,p = build_lv(5,5,2,[('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,1,2,'H'),('c2','c',0,3,2,'H'),('e1','e',3,4,1,'H')], names[12],icon_for(5))
assert p==6, f"Lv12 got {p}"; ALL.append(lv)

# Lv13: par=5 (different topology - bronto)
lv,p = build_lv(5,5,2,[('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,2,2,'H'),('e1','e',3,2,1,'H')], names[13],icon_for(6))
# If BFS is wrong, adjust
ALL.append(lv)
print(f"Lv13 initial BFS={p}")

# Lv14: target par=6
lv14_candidates = [
    [('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,2,2,'H'),('c2','c',3,3,2,'H'),('e1','e',0,4,1,'H')],
    [('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,1,2,'H'),('c2','c',0,3,2,'H'),('e1','e',3,2,1,'H'),('e2','e',3,3,1,'H')],
]
placed14 = False
for c in lv14_candidates:
    lv,p = build_lv(5,5,2,c,names[14],icon_for(0))
    if p>=5:
        ALL.append(lv); placed14=True
        print(f"Lv14 BFS={p}")
        break
if not placed14:
    # fallback: use random search
    for s in range(50):
        pdef,fp = random_6x6(6, 2, 5000, s) # actually want 5x5
        # Can't use random_6x6 for 5x5. Use inline.
        rng=random.Random(s*7+14)
        cols2,rows2,er2=5,5,2
        grid2=[[False]*cols2 for _ in range(rows2)]
        grid2[er2][0]=grid2[er2][1]=True
        pd2=[('tx','t',er2,0,2,'H')]
        cnts2={}
        bad2=False
        for _ in range(rng.randint(3,6)):
            pt2=rng.choice(['r','c','e'])
            pl2=1 if pt2=='e' else 2
            pdr2=rng.choice(['H','V']) if pt2!='e' else 'H'
            ok3=False
            for __ in range(100):
                if pdr2=='H':
                    r2=rng.randint(0,rows2-1);c2=rng.randint(0,cols2-pl2)
                    cells2=[(r2,c2+i) for i in range(pl2)]
                else:
                    r2=rng.randint(0,rows2-pl2);c2=rng.randint(0,cols2-1)
                    cells2=[(r2+i,c2) for i in range(pl2)]
                if all(not grid2[rr][cc] for rr,cc in cells2):
                    for rr,cc in cells2: grid2[rr][cc]=True
                    cnts2[pt2]=cnts2.get(pt2,0)+1
                    pd2.append((f"{pt2}{cnts2[pt2]}",pt2,r2,c2,pl2,pdr2))
                    ok3=True;break
            if not ok3: bad2=True;break
        if bad2: continue
        tl2={'cols':5,'rows':5,'exitRow':er2,'par':0,'name':'t','icon':'🦕',
             'pieces':[make_piece(pid,pt,r,c,l,d) for pid,pt,r,c,l,d in pd2]}
        rs2=solve(tl2)
        if rs2==6:
            lv,p=build_lv(5,5,er2,pd2,names[14],icon_for(0))
            ALL.append(lv); placed14=True
            print(f"Lv14 (random) BFS={p}")
            break
    if not placed14:
        print("Lv14 FAILED - using par=5 fallback")
        lv,p=build_lv(5,5,2,[('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,1,2,'H'),('c2','c',0,3,2,'H'),('e1','e',3,4,1,'H')],names[14],icon_for(0))
        ALL.append(lv); print(f"Lv14 fallback BFS={p}")

# Lv15: target par=7
lv15_candidates = [
    [('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,2,2,'H'),('c2','c',3,2,2,'H'),('r4','r',3,4,2,'V'),('e1','e',0,4,1,'H')],
    [('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,1,2,'H'),('c2','c',0,3,2,'H'),('c3','c',3,2,2,'H'),('e1','e',3,4,1,'H')],
]
placed15=False
for c in lv15_candidates:
    lv,p=build_lv(5,5,2,c,names[15],icon_for(1))
    if p>=6:
        ALL.append(lv); placed15=True
        print(f"Lv15 BFS={p}")
        break
if not placed15:
    # fallback
    for s in range(200):
        rng=random.Random(s*11+15)
        cols2,rows2,er2=5,5,2
        grid2=[[False]*cols2 for _ in range(rows2)]
        grid2[er2][0]=grid2[er2][1]=True
        pd2=[('tx','t',er2,0,2,'H')]
        cnts2={}; bad2=False
        for _ in range(rng.randint(4,7)):
            pt2=rng.choice(['r','r','c','c','e'])
            pl2=1 if pt2=='e' else 2
            pdr2=rng.choice(['H','V']) if pt2!='e' else 'H'
            ok3=False
            for __ in range(100):
                if pdr2=='H':
                    r2=rng.randint(0,rows2-1);c2=rng.randint(0,cols2-pl2)
                    cells2=[(r2,c2+i) for i in range(pl2)]
                else:
                    r2=rng.randint(0,rows2-pl2);c2=rng.randint(0,cols2-1)
                    cells2=[(r2+i,c2) for i in range(pl2)]
                if all(not grid2[rr][cc] for rr,cc in cells2):
                    for rr,cc in cells2: grid2[rr][cc]=True
                    cnts2[pt2]=cnts2.get(pt2,0)+1
                    pd2.append((f"{pt2}{cnts2[pt2]}",pt2,r2,c2,pl2,pdr2))
                    ok3=True;break
            if not ok3: bad2=True;break
        if bad2: continue
        tl2={'cols':5,'rows':5,'exitRow':er2,'par':0,'name':'t','icon':'🦕',
             'pieces':[make_piece(pid,pt,r,c,l,d) for pid,pt,r,c,l,d in pd2]}
        rs2=solve(tl2)
        if rs2==7:
            lv,p=build_lv(5,5,er2,pd2,names[15],icon_for(1))
            ALL.append(lv); placed15=True
            print(f"Lv15 (random) BFS={p}")
            break
    if not placed15:
        lv,p=build_lv(5,5,2,[('tx','t',2,0,2,'H'),('r1','r',1,2,2,'V'),('r2','r',1,3,2,'V'),('r3','r',1,4,2,'V'),('c1','c',0,1,2,'H'),('c2','c',0,3,2,'H'),('c3','c',3,2,2,'H'),('e1','e',3,4,1,'H')],names[15],icon_for(1))
        ALL.append(lv); print(f"Lv15 fallback BFS={p}")

print(f"Levels 1-15 built: {len(ALL)}")

# ─── 6x6 levels 16-50 via random search ─────────────────────────────────────

level_targets = [
    (16, 2, 5, 0),(17, 2, 5, 1),(18, 2, 6, 2),(19, 2, 6, 3),(20, 3, 6, 4),
    (21, 2, 7, 5),(22, 2, 7, 6),(23, 3, 7, 7),(24, 2, 8, 8),(25, 3, 8, 9),
    (26, 2, 7, 10),(27, 3, 8, 11),(28, 2, 8, 12),(29, 3, 8, 13),(30, 2, 9, 14),
    (31, 3, 9, 15),(32, 2, 9, 16),(33, 3, 9, 17),(34, 2, 10, 18),(35, 3, 10, 19),
    (36, 2, 9, 20),(37, 3, 10, 21),(38, 2, 10, 22),(39, 3, 10, 23),(40, 2, 11, 24),
    (41, 3, 11, 25),(42, 2, 11, 26),(43, 3, 12, 27),(44, 2, 12, 28),(45, 3, 12, 29),
    (46, 2, 11, 30),(47, 3, 12, 31),(48, 2, 12, 32),(49, 3, 13, 33),(50, 2, 13, 34),
]

for lv_num, exitRow, target, seed_off in level_targets:
    name = names[lv_num]
    icon = icon_for(lv_num - 7)
    tries = 50000
    pdef, found = random_6x6(target, exitRow, max_tries=tries, seed_offset=seed_off)
    if pdef is None:
        # Try alternate pars
        for delta in [1, -1, 2, -2, 3, -3]:
            alt = target + delta
            if alt < 1: continue
            pdef, found = random_6x6(alt, exitRow, max_tries=20000, seed_offset=seed_off+200+delta*7)
            if pdef is not None:
                print(f"Lv{lv_num:2d} {name}: target={target} -> found par={found}")
                break
    if pdef is not None:
        lv2, p2 = build_lv(6, 6, exitRow, pdef, name, icon)
        ALL.append(lv2)
        print(f"Lv{lv_num:2d} {name}: BFS={p2} pieces={len(pdef)}")
    else:
        print(f"Lv{lv_num:2d} {name}: COMPLETE FAILURE")

print(f"\nFinal level count: {len(ALL)}")

# ─── Fill any missing levels ─────────────────────────────────────────────────
# If we have fewer than 50, generate filler levels
if len(ALL) < 50:
    missing = 50 - len(ALL)
    print(f"Filling {missing} missing levels...")
    for fill_n in range(missing):
        for s in range(200):
            pdef, found = random_6x6(9, 2, 10000, seed_offset=500+fill_n*50+s)
            if pdef is not None:
                lv_num = len(ALL) + 1
                name = names.get(lv_num, '挑戰')
                icon = icon_for(lv_num-7)
                lv2, p2 = build_lv(6, 6, 2, pdef, name, icon)
                ALL.append(lv2)
                print(f"  Filler Lv{lv_num}: BFS={p2}")
                break

print(f"Total levels: {len(ALL)}")

# Save
with open('/home/user/Dino/levels_data.json', 'w') as f:
    json.dump(ALL, f, ensure_ascii=False, indent=2)
print("Saved levels_data.json")

# Verify all levels
print("\n=== Final verification ===")
all_ok = True
for i, lv in enumerate(ALL):
    par = lv['par']
    if par < 1:
        print(f"  Lv{i+1} UNSOLVABLE (BFS={par})")
        all_ok = False
    else:
        print(f"  Lv{i+1:2d} {lv['name']:8s} {lv['cols']}x{lv['rows']} exitRow={lv['exitRow']} par={par}")

print(f"\nAll solvable: {all_ok}")
