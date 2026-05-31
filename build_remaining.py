"""
Build remaining levels 41-50 using optimized BFS solver.
Uses specific seeds known to work from previous runs.
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
        if tx_col + 2 > cols: tx_col = 0
        for i in range(2): grid[exitRow][tx_col+i] = True
        pdef = [('tx','t',exitRow,tx_col,2,'H')]

        n_pieces = rng.randint(4, 9)
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
    41:'傳說開始',42:'史詩難題',43:'頂尖高手',44:'終極挑戰',45:'恐龍王者',
    46:'最強大腦',47:'恐龍傳說',48:'無敵挑戰',49:'終極難關',50:'恐龍冠軍',
}

# These are the remaining levels needed
remaining_specs = [
    (41, 6,6,3,11, 10041),
    (42, 6,6,2,11, 10042),
    (43, 6,6,3,12, 10043),
    (44, 6,6,2,12, 10044),
    (45, 6,6,3,12, 10045),
    (46, 6,6,2,11, 10046),
    (47, 6,6,3,12, 10047),
    (48, 6,6,2,12, 10048),
    (49, 6,6,3,13, 10049),
    (50, 6,6,2,13, 10050),
]

results = {}
print("Building levels 41-50...")
for lv_num, cols, rows, exitRow, target, seed_base in remaining_specs:
    name = names[lv_num]
    icon = icon_for(lv_num-7)

    pdef, actual_par = random_level(target, cols, rows, exitRow, max_tries=100000, seed_base=seed_base)

    if pdef is None:
        for delta in [1, -1, 2, -2, 3, -3, 4, -4]:
            alt = target + delta
            if alt < 1: continue
            pdef, actual_par = random_level(alt, cols, rows, exitRow, max_tries=50000, seed_base=seed_base+delta*2000)
            if pdef is not None:
                break

    if pdef is not None:
        lv2, p2 = build_lv(cols, rows, exitRow, pdef, name, icon)
        results[lv_num] = lv2
        elapsed = time.time() - t_start
        print(f"  Lv{lv_num:2d} {name}: BFS={p2} pieces={len(pdef)} ({elapsed:.1f}s)")
    else:
        print(f"  Lv{lv_num:2d} {name}: FAILED target={target}")

# Save results
with open('/home/user/Dino/levels_41_50.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(results)} levels to levels_41_50.json")
