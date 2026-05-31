"""Build levels 48-50."""
import sys, random, json, time
sys.path.insert(0, '/home/user/Dino')
from solver_fast import solve_fast as solve, make_piece

t_start = time.time()

def build_lv(cols, rows, exitRow, pieces_def, name, icon):
    pieces = [make_piece(pid, pt, r, c, l, d) for pid,pt,r,c,l,d in pieces_def]
    lv = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,'name':name,'icon':icon,'pieces':pieces}
    result = solve(lv)
    lv['par'] = result
    return lv, result

def random_level(target_par, cols, rows, exitRow=2, max_tries=100000, seed_base=0):
    rng = random.Random(seed_base)
    for attempt in range(max_tries):
        grid = [[False]*cols for _ in range(rows)]
        tx_col = 0 if rng.random() < 0.7 else 1
        if tx_col + 2 > cols: tx_col = 0
        for i in range(2): grid[exitRow][tx_col+i] = True
        pdef = [('tx','t',exitRow,tx_col,2,'H')]

        n_pieces = rng.randint(5, 10)
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
names={48:'無敵挑戰',49:'終極難關',50:'恐龍冠軍'}

specs = [
    (48, 6,6,2,12, 20048),
    (49, 6,6,3,13, 20049),
    (50, 6,6,2,13, 20050),
]

results = {}
for lv_num, cols, rows, exitRow, target, seed_base in specs:
    name = names[lv_num]
    icon = icons[(lv_num-7)%len(icons)]
    pdef, ap = random_level(target, cols, rows, exitRow, max_tries=200000, seed_base=seed_base)
    if pdef is None:
        for delta in [1,-1,2,-2,3,-3,4,-4]:
            alt = target+delta
            if alt<1: continue
            pdef,ap = random_level(alt, cols, rows, exitRow, max_tries=80000, seed_base=seed_base+delta*3000)
            if pdef: break
    if pdef:
        lv2,p2 = build_lv(cols,rows,exitRow,pdef,name,icon)
        results[lv_num] = lv2
        print(f"Lv{lv_num} {name}: BFS={p2} pieces={len(pdef)} ({time.time()-t_start:.1f}s)")
    else:
        print(f"Lv{lv_num} FAILED")

with open('/home/user/Dino/levels_48_50.json','w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"Done: {len(results)} levels saved")
