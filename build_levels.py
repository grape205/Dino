import sys
sys.path.insert(0, '/home/user/Dino')
from solver import solve, make_piece, LEVELS as BASE_LEVELS

def lv(cols, rows, exitRow, pieces_def, name='', icon='🦕', par=0):
    pieces = [make_piece(pid, pt, r, c, l, d) for pid,pt,r,c,l,d in pieces_def]
    level = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':par,
             'name':name,'icon':icon,'pieces':pieces}
    result = solve(level)
    level['par'] = result
    return level, result

ALL_LEVELS = list(BASE_LEVELS)  # start with verified levels 1-6

icons = ['🦕','🦖','🐊','🦎','⭐','🏆','👑']
def icon_for(idx):  # idx 0-based from lv7
    return icons[idx % len(icons)]

names = {
    7:'初學者', 8:'恐龍迷', 9:'小探險家', 10:'冒險開始',
    11:'越來越難', 12:'動動腦筋', 13:'挑戰開始', 14:'恐龍博士', 15:'智力測驗',
    16:'進階玩家', 17:'高手之路', 18:'恐龍達人', 19:'頭腦體操', 20:'解謎高手',
    21:'思考訓練', 22:'推理高手', 23:'智慧勇士', 24:'腦力激盪', 25:'謎題挑戰',
    26:'困難模式', 27:'超難挑戰', 28:'恐龍難題', 29:'腦筋急轉', 30:'智力競賽',
    31:'困難關卡', 32:'超級難關', 33:'極限挑戰', 34:'恐龍勇者', 35:'邏輯大師',
    36:'恐龍天才', 37:'超級大腦', 38:'最強挑戰', 39:'傳奇玩家', 40:'恐龍霸主',
    41:'傳說開始', 42:'史詩難題', 43:'頂尖高手', 44:'終極挑戰', 45:'恐龍王者',
    46:'最強大腦', 47:'恐龍傳說', 48:'無敵挑戰', 49:'終極難關', 50:'恐龍冠軍',
}

results = []

print("Building and verifying levels 7-50...")
print()

# ─── Levels 7-15: 5x5, par 4-7 ───────────────────────────────────────────────

# Lv7: 5x5, exitRow=2, target par=4
# r1(V,r1,c2), r2(V,r1,c3) block row2. c1(H,r0,c2) blocks both going up.
# Solution: c1 left 2 -> r1 up -> r2 up -> T  (4 moves)
lv7, p7 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('c1','c',0,2,2,'H'),
], names[7], icon_for(0))
ALL_LEVELS.append(lv7)
print(f"Lv7  {names[7]}: BFS={p7} ({'OK' if p7==4 else 'CHECK'})")

# Lv8: 5x5, exitRow=2, target par=4
# Same as lv7 but c1 must go right (not left), r3 also in play
# r1(V,r1,c3), r2(V,r1,c4), c1(H,r0,c3) blocks r1,r2 going up, e1 at (0,2)
# Solution: c1 right -> r1 up -> r2 up -> T OR c1 right -> r2 up -> r1 up -> T
lv8, p8 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,3,2,'V'),
    ('r2','r',1,4,2,'V'),
    ('r1b','r',1,2,2,'V'),  # extra blocker at col2
    ('c1','c',0,3,2,'H'),   # row0,col3-4
    ('e1','e',0,2,1,'H'),   # blocks r1b going up
], names[8], icon_for(1))
ALL_LEVELS.append(lv8)
print(f"Lv8  {names[8]}: BFS={p8} ({'OK' if p8==4 else 'CHECK'})")

# Lv9: 5x5, exitRow=2, target par=5
# From successful design B
lv9, p9 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('c1','c',1,3,2,'H'),
    ('e1','e',0,2,1,'H'),
    ('e2','e',4,3,1,'H'),
], names[9], icon_for(2))
ALL_LEVELS.append(lv9)
print(f"Lv9  {names[9]}: BFS={p9} ({'OK' if p9==5 else 'CHECK'})")

# Lv10: 5x5, exitRow=2, target par=5
# Design A variant - verified BFS=4, need par=5
# New design: 3 V blockers + c1 blocks 2 + e blocks 1, r3 needs 2-step chain
# r1(V,r1,c2), r2(V,r1,c3), r3(V,r1,c4)
# c1(H,r0,c2,2): row0,col2-3 blocks r1,r2 going up
# e1(egg) at (0,4): blocks r3 going up
# c2(H,r3,c3,2): row3,col3-4 blocks r2,r3 going down
# Solution: c1 right to col3-4(1) - wait col3-4 with c2 at row3 doesn't affect.
# c1 right: col3-4. Row0,col2 free. r1 up(1). Row2,col2 free.
# r2: row0,col3 has c1! Can't go up. Row3,col3 has c2. Can't go down. STUCK.
# Need c1 to fully clear col3 too.
# c1 right 1 = col3-4. Col3,row0 occupied. Bad for r2.
# c1 left 2 = col0-1. Row0,col2,col3 free. r1 up(1). r2 up(1).
# r3: row0,col4 has e1! Can't go up. Row3,col4 has c2. Can't go down. r3 STUCK. Bad.
# Change: c2 at row3,col3 only (not col4). Use e2 at row3,col4 to block r3 down.
# Then r3 has e1(row0,col4) above and e2(row3,col4) below. r3 length=2: rows1-2. Up: row0 blocked. Down: row3 blocked. r3 STUCK. Bad.
# Need r3 to be able to move. Remove one egg.
# e1 only (row0,col4 blocks r3 up). r3 can go down to rows3-4 (if row3,col4 free - c2 at col3 not col4).
# But we want r3 to need 2 steps. c2(H,r3,c3,2) doesn't block col4.
# So r3 goes down freely. We're back to 4 moves for r3 path.
# Alternative: put c1 large enough to block all three.
# b1(H,r0,c2,3): row0,col2-4. Blocks r1,r2,r3 going up. b1 must move.
# b1 right: col3-5 OOB. b1 left: col1-3(1), col0-2(2). After left 2: col0-2, col3,col4 free.
# r1(col2): row0,col2 has b1 left end. Still blocked!
# After left 1: col1-3, col4 free (r3 can go up). col2,col3 still in b1. r1,r2 still blocked.
# b1 can't free col2. Same issue as before.
#
# The 5-move design that works (Design B lv9e):
# r1 at rows1-2,col2. r2 at rows2-3,col3. r3 at rows2-3,col4.
# c1(H,r1,c3,2) blocks r2 going up. e1(row0,col2) blocks r1 going up. e2(row4,col3) blocks r2 going down.
# Solution: r1 down 2(1) + c1 left 2(1) + r2 up(1) + r3 down 1(1) + T(1) = 5
# Let me use this verified design for lv10 with slight variation.

lv10, p10 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),   # rows1-2,col2
    ('r2','r',2,3,2,'V'),   # rows2-3,col3
    ('r3','r',2,4,2,'V'),   # rows2-3,col4
    ('c1','c',1,3,2,'H'),   # row1,col3-4
    ('e1','e',0,2,1,'H'),
    ('e2','e',4,3,1,'H'),
    ('e3','e',4,4,1,'H'),   # also blocks r3 going down - forces r3 up? No col4 r3 down 1=rows3-4, row4,col4=e3. Blocked. r3 up: row1,col4 - c1 at row1,col3-4! Blocked initially. After c1 left 2 (c1 at row1,col1-2): row1,col3,col4 free. r3 up 1=rows1-2. Row2,col4 free.
    # Solution: r1 down 2(1) + c1 left 2(1) + r2 up(1) + r3 up(1) + T(1) = 5. Same.
    # But does e3 at (4,4) overlap with anything? r3 at rows2-3,col4: (2,4),(3,4). e3 at (4,4). No overlap. Good.
    # BFS should still be 5.
], names[10], icon_for(3))
ALL_LEVELS.append(lv10)
print(f"Lv10 {names[10]}: BFS={p10} ({'OK' if p10==5 else 'CHECK'})")

# Lv11: 5x5, exitRow=2, target par=5
# Different topology - use brontosaurus
# b1(V,r0,c3,3): rows0-2,col3. Blocks T at (2,3). b1 down: row3,col3 free -> down 1=rows1-3, down 2=rows2-4. Neither clears row2.
# b1 can't clear exitRow if len=3 and only 5 rows and exitRow=2. Skip.
# b1(H,r3,c2,3): row3,col2-4. Doesn't directly block T.
# Use it to block other pieces from going down, creating longer chains.

# Lv11: 5x5, exitRow=2, target par=5
# Different from lv9/10:
# r1(V,r0,c2,2), c1(H,r2,c2,2): r1 at rows0-1,col2. c1 at row2,col2-3.
# Wait c1(H) is horizontal and T-Rex is H too - c1 blocks T's path (row2,col2-3).
# T needs col2,col3,col4 clear. c1 blocks col2,col3.
# r2(V,r2,c4,2): rows2-3,col4 blocks col4.
# c1 can go right: col3-4 (1 move). Row2,col2 free. But col3 has c1 right end still. T at col2 blocked by col3.
# c1 right 2: col4-5 OOB. c1 right 1 only. Not enough.
# c1 can go left: col0-1 (but T at col0-1 row2!). Overlap. Can't.
# c1 is a bad blocker for T in 5x5 (same issue as before).
# Must use V pieces for direct blocking.

# Lv11: exitRow=1, 5x5, target par=5
# T at row1,col0. Needs cols2,3,4 clear in row1.
# r1(V,r0,c2,2): rows0-1,col2. Blocks (1,2).
# c1(H,r2,c2,2): row2,col2-3. c1 blocks r1 from going down (row2,col2 occ).
# r2(V,r0,c3,2): rows0-1,col3. Blocks (1,3).
# e1(egg,r2,c3): row2,col3 blocks r2 from going down.
# r3(V,r0,c4,2): rows0-1,col4. Blocks (1,4).
# r3 down: row2,col4 free -> down 1=rows1-2. Still in row1! down 2=rows2-3. Row1,col4 free.
# r3 down 2 = 1 move.
# r1 down: row2,col2 has c1. Blocked. c1 must move first.
# c1 right 1=col3-4. Row2,col2 free. But row2,col3 has e1! c1 at col3-4... c1 right 1: col3,row2 = e1. Blocked.
# c1 left: col0-1,row2 free. c1 left 1=col1-2. col2,row2 occupied (c1 left end). Still blocked for r1?
# After c1 left 1: c1 at col1-2. r1 at rows0-1,col2. r1 wants to go down: row2,col2 has c1. Still blocked!
# c1 left 2=col0-1. Row2,col2 free. r1 down 2=rows2-3 (1 move). Row1,col2 free.
# r2: row2,col3 has e1. r2 up: row-1 OOB. r2 down: row2,col3 has e1. r2 STUCK. Bad!
# Remove e1. r2 down: row2,col3 free. r2 down 2=rows2-3. Row1,col3 free.
# Now: c1 left 2(1) + r1 down 2(1) + r2 down 2(1) + r3 down 2(1) + T(1) = 5 moves.
# Can we do it in 4? All 4 pieces (c1,r1,r2,r3,T) need to move. c1 unblocks r1.
# Can r2 and r3 move independently (without waiting for c1)?
# r2: row2,col3 free initially (no e1). r2 down 2 = rows2-3 (row2,col3 still has r2 bottom? rows2-3 means (2,3),(3,3), so row2,col3 still occupied!). r2 down 2 means r2 moves 2 steps: new pos = rows0+2=rows2-3. Still in row1? No: r2 started at rows0-1. After down 2: rows2-3. Row1,col3 free! Good.
# r2 can move independently of c1 (since c1 only blocks r1 going down, not r2).
# r3 can also move independently: down 2 = rows2-3. Row1,col4 free.
# So: r2 down 2(1) + r3 down 2(1) + c1 left 2(1) + r1 down 2(1) + T(1) = 5 moves.
# Shorter: can r2 and r3 move in parallel (same count)? Each is 1 move. c1+r1+T = 3. Total = 5.
# Is there a 4-move solution? Need to eliminate one step.
# If r1 could move down without c1: row2,col2 initially free? c1 is there. Can't.
# If c1 weren't needed (e.g., r1 can go up instead): row-1 OOB. Can't.
# So minimum is 5 moves. BFS should confirm.

lv11, p11 = lv(5,5,1,[
    ('tx','t',1,0,2,'H'),
    ('r1','r',0,2,2,'V'),   # rows0-1,col2
    ('r2','r',0,3,2,'V'),   # rows0-1,col3
    ('r3','r',0,4,2,'V'),   # rows0-1,col4
    ('c1','c',2,2,2,'H'),   # row2,col2-3 blocks r1 going down
], names[11], icon_for(4))
ALL_LEVELS.append(lv11)
print(f"Lv11 {names[11]}: BFS={p11} ({'OK' if p11>=4 else 'CHECK'})")

# Lv12: 5x5, exitRow=2, target par=5 (different design)
# exitRow=2. T at col0.
# r1(V,r1,c2), c1(H,r0,c1,2) blocks r1 going up (row0,col2? c1 at col1-2 row0 - col2 has c1!).
# r1 up: row0,col2 has c1. Blocked. r1 down: rows3-4. Row2,col2 free. But need more steps.
# Add r2(V,r1,c3), r3(V,r1,c4). Also need to block them.
# c1(H,r0,c1,2) only covers col1-2. r2,r3 can go up freely.
# Add c2(H,r0,c3,2) row0,col3-4. Blocks r2,r3 going up.
# c1 right: col2-3. Row0,col1 free. col2 still has c1 right end. r1 still blocked.
# c1 left: col0-1. Row0,col2 free. r1 up: rows0-1. Row2,col2 free.
# c2 left: col2-3. Row0,col3 free (c2 moved but its left end at col2). r2 can go up: row0,col3 free (c2 now at col2-3, not col3). r2 up: rows0-1. c2 at col2,row0 and r2 at rows0-1,col3 - no overlap.
# Total: c1 left(1) + c2 left(1) + r1 up(1) + r2 up(1) + r3 up(1) + T(1) = 6 moves.
# Is there a 5-move shortcut?
# c1 and c2 must both move before r1,r2 can go up. r3 can go up independently (row0,col4 - c2 was at col3-4 initially! row0,col4 has c2 right end). r3 blocked.
# After c2 left 1 (col2-3): row0,col4 free. r3 up (1). So c1 + c2 must move = 2 moves, then r1,r2,r3 up = 3 moves, T = 1. Total = 6.
# BFS would be 6.

lv12, p12 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('c1','c',0,1,2,'H'),   # row0,col1-2
    ('c2','c',0,3,2,'H'),   # row0,col3-4
], names[12], icon_for(5))
ALL_LEVELS.append(lv12)
print(f"Lv12 {names[12]}: BFS={p12} ({'OK' if p12>=5 else 'CHECK'})")

# Lv13: 5x5, exitRow=2, target par=6
lv13, p13 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('c1','c',0,1,2,'H'),   # row0,col1-2
    ('c2','c',0,3,2,'H'),   # row0,col3-4
    ('e1','e',3,2,1,'H'),   # blocks r1 going down
], names[13], icon_for(6))
ALL_LEVELS.append(lv13)
print(f"Lv13 {names[13]}: BFS={p13} ({'OK' if p13>=5 else 'CHECK'})")

# Lv14: 5x5, target par=6
lv14, p14 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),   # row0,col2-3
    ('c2','c',3,3,2,'H'),   # row3,col3-4 blocks r2,r3 going down
    ('e1','e',0,4,1,'H'),   # blocks r3 going up
    ('e2','e',3,2,1,'H'),   # blocks r1 going down
], names[14], icon_for(0))
ALL_LEVELS.append(lv14)
print(f"Lv14 {names[14]}: BFS={p14} ({'OK' if p14>=6 else 'CHECK'})")

# Lv15: 5x5, target par=7
lv15, p15 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),   # row0,col2-3
    ('c2','c',3,2,2,'H'),   # row3,col2-3 blocks r1,r2 down
    ('c3','c',0,4,2,'V'),   # wait c3 can be H or V. Let's use r4(V,r3,c4,2) rows3-4,col4 blocks r3 down
    ('e1','e',0,4,1,'H'),   # blocks r3 up
], names[15], icon_for(1))
# Remove c3 from above - I put it wrong. Let me redo lv15.
ALL_LEVELS.pop()  # remove bad lv15

lv15, p15 = lv(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),   # row0,col2-3 blocks r1,r2 up
    ('c2','c',3,2,2,'H'),   # row3,col2-3 blocks r1,r2 down
    ('r4','r',3,4,2,'V'),   # rows3-4,col4 blocks r3 down
    ('e1','e',0,4,1,'H'),   # blocks r3 up
], names[15], icon_for(1))
ALL_LEVELS.append(lv15)
print(f"Lv15 {names[15]}: BFS={p15} ({'OK' if p15>=6 else 'CHECK'})")

print()
print("=== Levels 16-25: 6x6, par 5-8 ===")

# For 6x6 we have more room and can create richer puzzles.
# T-Rex at exitRow, len=2. Need cols 2-5 (or subset) in exitRow to be clear.
# T exits when col+2 > 6, i.e., col >= 5.

# Lv16: 6x6, exitRow=2, par=5
lv16, p16 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),   # rows1-2,col2
    ('r2','r',1,3,2,'V'),   # rows1-2,col3
    ('c1','c',0,2,2,'H'),   # row0,col2-3 blocks r1,r2 up
    ('r3','r',2,5,2,'V'),   # rows2-3,col5 blocks T at (2,5) - wait T needs to reach col>=5 (col+2>6 -> col>4 -> col>=5). T at col5 occupies col5-6 (6 OOB) -> win. So T needs col2-4 clear (to slide from col0 to col5).
    # Actually T exit condition: col+2>6 means col>=5. So T at col5: col5+2=7>6. Win.
    # But T slides right: first needs col2,col3,col4 clear (to reach col5), then col5... wait:
    # T at col0: needs col2 free (occupied by r1). After r1 moves, T at col2: needs col4 free. T at col4: needs... col6 OOB, so T exits.
    # Actually T just needs a clear path to slide: T slides in one move multiple steps.
    # T can slide from col0 to wherever the first obstacle is minus 1.
    # For T to exit (col+2>6), T needs to reach col>=5, so cells (2,2),(2,3),(2,4) must all be clear (no piece there).
    # r3(V,rows2-3,col5): (2,5) is col5. Does T need col5? T at col4: occupies col4,col5. col5 has r3! T can't be at col4. T at col3: occupies col3,col4. col4 free. T at col4: col4,col5 - col5 has r3. Wait, to exit T must reach col5: T at col5 occupies col5,col6 (col6 OOB -> exit). r3 at col5,rows2-3: cell (2,5) occupied. T at col4: occupies (2,4),(2,5). (2,5) has r3! T can't reach col4 if (2,5) is occupied.
    # Hmm. For T to reach col5 (exit), it needs (2,5) to be free too. r3 at rows2-3,col5 blocks T at its final move.
    # So r3 must also be moved. 6 pieces to move: c1(1) + r1(1) + r2(1) + r3(1) + T(1) = 5.
], names[16], icon_for(0))
ALL_LEVELS.append(lv16)
print(f"Lv16 {names[16]}: BFS={p16} ({'OK' if p16==5 else 'CHECK'})")

# Lv17: 6x6, exitRow=2, par=6
lv17, p17 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),   # row0,col2-3
    ('r4','r',2,5,2,'V'),   # rows2-3,col5
], names[17], icon_for(1))
ALL_LEVELS.append(lv17)
print(f"Lv17 {names[17]}: BFS={p17} ({'OK' if p17>=5 else 'CHECK'})")

# Lv18: 6x6, exitRow=2, par=6
lv18, p18 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),   # row0,col4-5 blocks r3 up
    ('r4','r',2,5,2,'V'),
], names[18], icon_for(2))
ALL_LEVELS.append(lv18)
print(f"Lv18 {names[18]}: BFS={p18} ({'OK' if p18>=6 else 'CHECK'})")

# Lv19: 6x6, exitRow=2, par=7
lv19, p19 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('r4','r',2,5,2,'V'),
    ('e1','e',3,5,1,'H'),   # blocks r4 down
], names[19], icon_for(3))
ALL_LEVELS.append(lv19)
print(f"Lv19 {names[19]}: BFS={p19} ({'OK' if p19>=6 else 'CHECK'})")

# Lv20: 6x6, exitRow=3, par=7
lv20, p20 = lv(6,6,3,[
    ('tx','t',3,0,2,'H'),
    ('r1','r',2,2,2,'V'),   # rows2-3,col2
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('r4','r',2,5,2,'V'),
    ('c1','c',1,2,2,'H'),   # row1,col2-3 blocks r1,r2 going up
    ('c2','c',1,4,2,'H'),   # row1,col4-5 blocks r3,r4 going up
], names[20], icon_for(4))
ALL_LEVELS.append(lv20)
print(f"Lv20 {names[20]}: BFS={p20} ({'OK' if p20>=6 else 'CHECK'})")

# Lv21: 6x6, exitRow=2, par=7
lv21, p21 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),   # row0,col2-3
    ('c2','c',0,4,2,'H'),   # row0,col4-5
], names[21], icon_for(5))
ALL_LEVELS.append(lv21)
print(f"Lv21 {names[21]}: BFS={p21} ({'OK' if p21>=6 else 'CHECK'})")

# Lv22: 6x6, exitRow=2, par=7
lv22, p22 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('e1','e',3,2,1,'H'),   # blocks r1 going down
], names[22], icon_for(6))
ALL_LEVELS.append(lv22)
print(f"Lv22 {names[22]}: BFS={p22} ({'OK' if p22>=6 else 'CHECK'})")

# Lv23: 6x6, exitRow=2, par=7-8
lv23, p23 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('e1','e',3,2,1,'H'),
    ('e2','e',3,5,1,'H'),   # blocks r4 going down
], names[23], icon_for(0))
ALL_LEVELS.append(lv23)
print(f"Lv23 {names[23]}: BFS={p23} ({'OK' if p23>=7 else 'CHECK'})")

# Lv24: 6x6, exitRow=2, par=8
lv24, p24 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('e1','e',3,2,1,'H'),
    ('e2','e',3,5,1,'H'),
    ('b1','b',3,3,3,'H'),   # row3,col3-5. Blocks r2,r3,r4 going down (row3,col3,col4,col5 occupied)
    # But e2 at row3,col5 and b1 at row3,col3-5 overlap at (3,5)! Bad.
], names[24], icon_for(1))
# Fix: remove e2, use b1 for that blocking
ALL_LEVELS.pop()
lv24, p24 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('e1','e',3,2,1,'H'),
    ('b1','b',3,3,3,'H'),   # row3,col3-5 blocks r2,r3,r4 going down
], names[24], icon_for(1))
ALL_LEVELS.append(lv24)
print(f"Lv24 {names[24]}: BFS={p24} ({'OK' if p24>=7 else 'CHECK'})")

# Lv25: 6x6, exitRow=2, par=8
lv25, p25 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('e1','e',3,2,1,'H'),
    ('b1','b',3,3,3,'H'),
    ('r5','r',4,1,2,'V'),   # extra piece to add complexity
], names[25], icon_for(2))
ALL_LEVELS.append(lv25)
print(f"Lv25 {names[25]}: BFS={p25} ({'OK' if p25>=7 else 'CHECK'})")

print()
print("=== Levels 26-35: 6x6, par 7-10 ===")

# Lv26: 6x6, exitRow=3, par=7
lv26, p26 = lv(6,6,3,[
    ('tx','t',3,0,2,'H'),
    ('r1','r',2,2,2,'V'),   # rows2-3,col2
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('r4','r',2,5,2,'V'),
    ('c1','c',1,2,2,'H'),   # row1,col2-3
    ('c2','c',1,4,2,'H'),   # row1,col4-5
], names[26], icon_for(3))
ALL_LEVELS.append(lv26)
print(f"Lv26 {names[26]}: BFS={p26} ({'OK' if p26>=7 else 'CHECK'})")

# Lv27: 6x6, exitRow=3, par=8
lv27, p27 = lv(6,6,3,[
    ('tx','t',3,0,2,'H'),
    ('r1','r',2,2,2,'V'),
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('r4','r',2,5,2,'V'),
    ('c1','c',1,2,2,'H'),
    ('c2','c',1,4,2,'H'),
    ('e1','e',0,3,1,'H'),   # blocks c1 going up? c1 is H. Blocks r2(col3) going up to row0.
    # r2(V,rows2-3,col3). c1 blocks r2 going up (row1,col3 occ). For r2 to go up past row1, c1 must move.
    # After c1 moves, r2 can go up. But e1 at row0,col3 blocks r2 from going to row0.
    # So r2 up max = row1 (1 step: rows1-2). row2 still occupied. r2 up 2: row0,col3 has e1. Blocked.
    # r2 up 1 = rows1-2. (2,3) still has r2 top? rows1-2 means (1,3),(2,3). Yes, row2 still occupied!
    # r2 needs to go to rows0-1 to clear row2. But row0,col3 has e1. r2 STUCK after c1 moves!
    # Remove e1, use different blocker.
], names[27], icon_for(4))
ALL_LEVELS.pop()
lv27, p27 = lv(6,6,3,[
    ('tx','t',3,0,2,'H'),
    ('r1','r',2,2,2,'V'),
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('r4','r',2,5,2,'V'),
    ('c1','c',1,2,2,'H'),
    ('c2','c',1,4,2,'H'),
    ('b1','b',4,2,3,'H'),   # row4,col2-4 blocks r1,r2,r3 going down
], names[27], icon_for(4))
ALL_LEVELS.append(lv27)
print(f"Lv27 {names[27]}: BFS={p27} ({'OK' if p27>=7 else 'CHECK'})")

# Lv28: 6x6, exitRow=2, par=8
lv28, p28 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('b1','b',0,2,3,'H'),   # row0,col2-4 blocks r1,r2,r3 going up
    ('c1','c',0,5,2,'V'),   # wait c1 V at col5 rows0-1: blocks r4(rows1-2,col5) going up? r4 up: row0,col5 - c1(V,r0,c5) occupies rows0-1,col5! r4 top going up hits c1 bottom at row0,col5. Blocked. Yes.
    # c1 must move. c1(V,r0,c5): left/right? c1 is V, moves up/down. Up: row-1 OOB. Down: row2,col5 free -> down 1 = rows1-2. row0,col5 free. r4 up 1 = rows0-1. row2,col5 free... wait r4 at rows1-2,col5. After down 1, r4 up 1: rows0-1. row2,col5 free? r4 originally at rows1-2. After up 1: rows0-1. (2,5) free.
    # Hmm but c1(V) moved down to rows1-2 and r4 is also at rows1-2,col5. OVERLAP!
    # c1 down goes to rows1-2, but r4 is at rows1-2,col5. Can't.
    # c1 STUCK. Bad.
], names[28], icon_for(5))
ALL_LEVELS.pop()
lv28, p28 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('b1','b',0,2,3,'H'),   # row0,col2-4 blocks r1,r2,r3 going up
    ('e1','e',0,5,1,'H'),   # blocks r4 going up
    ('b2','b',3,2,3,'H'),   # row3,col2-4 blocks r1,r2,r3 going down
], names[28], icon_for(5))
ALL_LEVELS.append(lv28)
print(f"Lv28 {names[28]}: BFS={p28} ({'OK' if p28>=7 else 'CHECK'})")

# Lv29: 6x6, exitRow=2, par=8
lv29, p29 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('b1','b',0,2,3,'H'),
    ('e1','e',0,5,1,'H'),
    ('b2','b',3,3,3,'H'),   # row3,col3-5 blocks r2,r3,r4 going down
    ('e2','e',3,2,1,'H'),   # blocks r1 going down
], names[29], icon_for(6))
ALL_LEVELS.append(lv29)
print(f"Lv29 {names[29]}: BFS={p29} ({'OK' if p29>=7 else 'CHECK'})")

# Lv30: 6x6, exitRow=3, par=9
lv30, p30 = lv(6,6,3,[
    ('tx','t',3,0,2,'H'),
    ('r1','r',2,2,2,'V'),
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('r4','r',2,5,2,'V'),
    ('c1','c',1,2,2,'H'),
    ('c2','c',1,4,2,'H'),
    ('b1','b',4,2,3,'H'),   # row4,col2-4 blocks r1,r2,r3 down
    ('e1','e',4,5,1,'H'),   # blocks r4 down
], names[30], icon_for(0))
ALL_LEVELS.append(lv30)
print(f"Lv30 {names[30]}: BFS={p30} ({'OK' if p30>=8 else 'CHECK'})")

# Lv31: 6x6, exitRow=2, par=9
lv31, p31 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('b1','b',0,2,3,'H'),   # row0,col2-4
    ('e1','e',0,5,1,'H'),
    ('b2','b',3,2,3,'H'),   # row3,col2-4
    ('e2','e',3,5,1,'H'),
    ('r5','r',4,0,2,'V'),   # extra piece rows4-5,col0
], names[31], icon_for(1))
ALL_LEVELS.append(lv31)
print(f"Lv31 {names[31]}: BFS={p31} ({'OK' if p31>=8 else 'CHECK'})")

# Lv32: 6x6, exitRow=2, par=9
lv32, p32 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('b1','b',3,2,3,'H'),
    ('e1','e',3,5,1,'H'),
    ('c3','c',4,3,2,'H'),   # row4,col3-4
], names[32], icon_for(2))
ALL_LEVELS.append(lv32)
print(f"Lv32 {names[32]}: BFS={p32} ({'OK' if p32>=8 else 'CHECK'})")

# Lv33: 6x6, exitRow=3, par=9-10
lv33, p33 = lv(6,6,3,[
    ('tx','t',3,0,2,'H'),
    ('r1','r',2,2,2,'V'),
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('r4','r',2,5,2,'V'),
    ('c1','c',1,2,2,'H'),
    ('c2','c',1,4,2,'H'),
    ('b1','b',4,2,3,'H'),
    ('e1','e',4,5,1,'H'),
    ('c3','c',0,2,2,'H'),   # row0,col2-3 blocks r1,r2 going further up
], names[33], icon_for(3))
ALL_LEVELS.append(lv33)
print(f"Lv33 {names[33]}: BFS={p33} ({'OK' if p33>=9 else 'CHECK'})")

# Lv34: 6x6, par=10
lv34, p34 = lv(6,6,3,[
    ('tx','t',3,0,2,'H'),
    ('r1','r',2,2,2,'V'),
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('r4','r',2,5,2,'V'),
    ('c1','c',1,2,2,'H'),
    ('c2','c',1,4,2,'H'),
    ('b1','b',4,2,3,'H'),
    ('e1','e',4,5,1,'H'),
    ('c3','c',0,2,2,'H'),
    ('e2','e',0,4,1,'H'),   # blocks r3 going further up
], names[34], icon_for(4))
ALL_LEVELS.append(lv34)
print(f"Lv34 {names[34]}: BFS={p34} ({'OK' if p34>=9 else 'CHECK'})")

# Lv35: 6x6, par=10
lv35, p35 = lv(6,6,3,[
    ('tx','t',3,0,2,'H'),
    ('r1','r',2,2,2,'V'),
    ('r2','r',2,3,2,'V'),
    ('r3','r',2,4,2,'V'),
    ('r4','r',2,5,2,'V'),
    ('c1','c',1,2,2,'H'),
    ('c2','c',1,4,2,'H'),
    ('b1','b',4,2,3,'H'),
    ('e1','e',4,5,1,'H'),
    ('c3','c',0,2,2,'H'),
    ('e2','e',0,4,1,'H'),
    ('r5','r',0,1,2,'V'),   # rows0-1,col1 extra piece
], names[35], icon_for(5))
ALL_LEVELS.append(lv35)
print(f"Lv35 {names[35]}: BFS={p35} ({'OK' if p35>=9 else 'CHECK'})")

print()
print("=== Levels 36-45: 6x6, par 9-12 ===")

# For higher par levels, need deeper chains.
# Strategy: use a "lock" piece that needs 3+ supporting moves to clear.

# Lv36: 6x6, exitRow=2, par=9
lv36, p36 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('b1','b',0,2,3,'H'),   # row0,col2-4
    ('c1','c',0,5,2,'V'),   # Wait col5, V len2 rows0-1: (0,5),(1,5). r4 at (1,5) - OVERLAP!
], names[36], icon_for(6))
ALL_LEVELS.pop()

# Build lv36 carefully
# 4 V blockers in row: r1..r4 at col2-5, rows1-2 (in exitRow=2).
# b1(H,r0,c2,3): row0,col2-4 blocks r1,r2,r3 going up. row0,col5 free for r4.
# r4 up: row0,col5 free -> up 1 = rows0-1. Row2,col5 free.
# b1 must move for r1,r2,r3 to go up.
# b1 right: col3-5(1), col4-6 OOB(can't). left: col1-3(1), col0-2(2).
# b1 left 2: col0-2. Row0,col3,col4 free. r2 up(1), r3 up(1). Still r1 blocked (col2 in b1).
# b1 left 1: col1-3. col2 still in b1. r1 still blocked.
# b1 right 1: col3-5. col2 free! r1 up(1). col4 still in b1. r3 still blocked. r3 down free.
# Let's check: r3 down: row3,col4 free -> r3 down 1 = rows2-3. (2,4) still r3 top. Down 2 = rows3-4. Row2,col4 free.
# After r4 up(1): row2,col5 free.
# After b1 right 1(1) + r1 up(1): row2,col2 free. r2: row0,col3 has b1 (col3-5 range). Can't go up.
# r2 down: row3,col3 free. r2 down 2 = rows3-4. Row2,col3 free. r3 down 2 = rows3-4. Row2,col4 free.
# Sequence: r4 up(1) + b1 right 1(1) + r1 up(1) + r2 down 2(1) + r3 down 2(1) + T(1) = 6 moves.
# Not 9. Need more constraints.

# For high par levels, I need more intricate designs. Let me use a more systematic approach.
# Create "double-locked" pieces where unlocking requires 2 moves each.

# Pattern for par~10:
# exitRow pieces need 3 supporting chains.
# Example: r1 blocked by c1, c1 blocked by r5, r5 blocked by c3, c3 blocked by b2...

# Let me try building a specific known puzzle topology.
# Reference: Rush Hour levels typically use interlocked pieces.

# Lv36: 6x6, par=9
# exitRow=2. T at col0.
# Block 1: r1(V,r1,c2) at rows1-2,col2. Chain: c1(H,r1,c3) row1,col3-4 blocks... r1 is V, not affected by c1 H.
# I need c1 to block something V that blocks r1.
# c1(H,r0,c2,2) row0,col2-3 blocks r1(V) going up. For c1 to move:
#   c1 right: col3-4(1), col4-5(2).
#   c1 left: col0-1(1 if free), col-1 OOB.
# Let r5(V,r0,c1,2) rows0-1,col1 block c1 going left (col1,row0 occupied):
#   c1 can only go right.
#   c1 right 1: col3-4. Row0,col2 free. r1 up(1). Row2,col2 free.
# r5: rows0-1,col1. T at row2,col0-1: no overlap (different rows). r5 can go down: row2,col1 free. r5 down 1=rows1-2. Still at row0? No: r5 started rows0-1, down 1 = rows1-2, row0 free. Doesn't affect c1 going right.
# With r5, c1 going right is still easy. Need to block c1 going right too.
# r6(V,r0,c4,2): rows0-1,col4 blocks c1 going right (col4,row0 occupied). c1 at col2-3, right 1: col3-4, col4 occupied. Can't. c1 stuck! Bad.
# r6(V,r0,c3,2): col3,row0 occupied. c1 at col2-3, right: col3,row0 has r6. Can't go right. c1 left: col0-1, row0 - r5 at col1. col1 occupied. c1 can't move! Bad.

# Hmm. Let me think differently.
# To get par=9 in 6x6, use a layout where there are 3 independent "locks":
# Lock A: needs 2 moves to open (A1 + A2)
# Lock B: needs 2 moves to open (B1 + B2)
# Lock C: needs 2 moves to open (C1 + C2)
# Plus direct blockers: 2 blockers + T = 3 more
# Total: 2+2+2+2+1 = 9

# Concrete design:
# T at row2,col0.
# r1(V,rows1-2,col2): direct blocker A. To move r1, c1(H,row1,col3-4) must move. To move c1, r2(V,rows0-1,col3) must move.
# So: r2 up/down(1) + c1 right(1) [or left] + r1 up(1) ... = 3 moves for chain A.
# r3(V,rows1-2,col3): direct blocker B. To move r3, same chain? But if r2 moves to free c1, and c1 moves to free r1, then r3 at col3 is now blocked by c1 position...
# This gets complicated quickly. Let me just test designs and use BFS.

# Strategy: use exitRow=2, T at col1 (not col0) to add one more T-Rex move.
# Actually T always starts at col=0 per game rules. Let me check: "T-Rex always starts at col=0 or col=1".
# OK, T can be at col=1. That means T only needs to slide from col1 to col5+ (exit).
# Path: T needs cells (2,3),(2,4),(2,5) clear when T is at col3,col4,col5 respectively.

# Let me just write more diverse puzzles and check BFS for each.

lv36, p36 = lv(6,6,2,[
    ('tx','t',2,1,2,'H'),   # T at col1
    ('r1','r',1,3,2,'V'),   # rows1-2,col3
    ('r2','r',1,4,2,'V'),
    ('r3','r',1,5,2,'V'),
    ('c1','c',0,3,2,'H'),   # row0,col3-4
    ('c2','c',3,3,2,'H'),   # row3,col3-4
    ('e1','e',0,5,1,'H'),
    ('e2','e',3,5,1,'H'),
    ('r4','r',2,0,2,'V'),   # rows2-3,col0 - blocks T going left? T is H, col0-1 initially. r4 at col0,rows2-3: (2,0) has T! Overlap.
], names[36], icon_for(6))
ALL_LEVELS.pop()

lv36, p36 = lv(6,6,2,[
    ('tx','t',2,1,2,'H'),   # T at col1
    ('r1','r',1,3,2,'V'),   # blocks (2,3)
    ('r2','r',1,4,2,'V'),   # blocks (2,4)
    ('r3','r',1,5,2,'V'),   # blocks (2,5)
    ('c1','c',0,3,2,'H'),   # row0,col3-4 blocks r1,r2 up
    ('e1','e',0,5,1,'H'),   # blocks r3 up
    ('c2','c',3,3,2,'H'),   # row3,col3-4 blocks r1,r2 down
    ('e2','e',3,5,1,'H'),   # blocks r3 down
    ('b1','b',0,0,3,'V'),   # col0,rows0-2: (0,0),(1,0),(2,0). (2,0) has... T is at (2,1),(2,2). Col0,row2 is (2,0) free. OK.
    # b1(V,r0,c0,3): occupies col0,rows0-2. Doesn't directly affect T path.
], names[36], icon_for(6))
ALL_LEVELS.append(lv36)
print(f"Lv36 {names[36]}: BFS={p36} ({'OK' if p36>=8 else 'CHECK'})")

# Lv37: 6x6, par=9-10
lv37, p37 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('b1','b',3,2,3,'H'),
    ('b2','b',3,5,3,'V'),   # col5,rows3-5 blocks r4 going down more. r4 at rows1-2,col5: down 1=rows2-3. (3,5) has b2. Blocked at down 1. r4 down 1=rows2-3: row2 still has r4! Down 2=rows3-4: (3,5) has b2. Blocked. r4 can only go down 1 (rows2-3), which doesn't clear row2. r4 UP: row0,col5 - c2 at row0,col4-5. (0,5) occupied. r4 STUCK!
    # Remove b2. Use e for that.
], names[37], icon_for(0))
ALL_LEVELS.pop()

lv37, p37 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),
    ('c2','c',0,4,2,'H'),
    ('b1','b',3,2,3,'H'),   # row3,col2-4
    ('e1','e',3,5,1,'H'),   # blocks r4 down
    ('e2','e',0,5,1,'H'),   # Hmm c2 is at col4-5, (0,5) would overlap with c2 right end! Bad.
], names[37], icon_for(0))
ALL_LEVELS.pop()

lv37, p37 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('c1','c',0,2,2,'H'),   # col2-3
    ('c2','c',0,4,2,'H'),   # col4-5
    ('b1','b',3,2,3,'H'),   # row3,col2-4
    ('e1','e',3,5,1,'H'),   # blocks r4 down (row3,col5)
    # c2 at (0,4),(0,5). e1 at (3,5). No overlap. c2 blocks r3(col4) and r4(col5) going up.
    # r4: row0,col5 has c2 right end. Blocked up. row3,col5 has e1. Blocked down. r4 STUCK!
    # c2 must move to allow r4 to move. c2 right: col5-6 OOB. c2 left 1: col3-4. col4 free. But col3,row0 - c1 is at col2-3! (0,3) has c1 right end. c2 left 1: col3-4, (0,3) occupied. Blocked.
    # c2 left 2: col2-3. (0,2) has c1. Blocked. c2 stuck!
    # Different: c1 at col2-3 and c2 at col4-5. For c2 to move, c1 must move first.
    # c1 left: col0-1 free. c1 left 2(1). Row0,col2,col3 free. c2 left: col3-4? (0,3) free. c2 left 1=col3-4(1). Row0,col4 free. r3 up 1 = rows0-1 (row0,col4 free now). (2,4) free.
    # c2 (now at col3-4) left 1 more = col2-3. (0,2) free (c1 moved away). c2 left 1 from col3-4 = col2-3(1). Row0,col4 still has c2? No: c2 moved to col2-3. Row0,col5 free. r4 up 1 = rows0-1. (2,5) free.
    # But sequence has c2 needing 2 moves. And e1 still blocks r4 down. r4 must go up.
    # After c1 left 2 + c2 left 1 (col3-4): r3 up free. But c2 still at col3-4, row0,col5 free. r4 up 1.
    # Wait after c2 left 1 (from col4-5 to col3-4): row0,col4 has c2 new left end, col5 free. r4(col5) up: row0,col5 free. r4 up 1 = rows0-1. (2,5) free.
    # Check r3: row0,col4 has c2. r3(col4) up 1: row0,col4 occupied. r3 can't go up. r3 down: row3,col4 - b1 at col2-4. (3,4) occupied. r3 down blocked. r3 STUCK!
    # Hmm. c2 at col3-4 blocks r3 up, and b1 blocks r3 down. r3 STUCK.
    # This topology is a dead end.
], names[37], icon_for(0))
ALL_LEVELS.pop()

# Let me use a fundamentally different approach for high-par levels.
# Use exitRow=2 with 3 V blockers and deep chains, each requiring 3 moves.

# Lv36-45 strategy: use known good patterns from lower levels + extra "locks"
# A "lock" = piece A blocked by piece B blocked by piece C
# Each chain of length 3 adds 3 moves.

# Simple reliable high-par design:
# T at row2, col0. Need cols 2,3,4,5 clear.
# r1(V,r1,c2,2): blocker at col2. Chain: c1(H,r0,c2,2) blocks r1 up, r5(V,r0,c1,2) blocks c1 left.
# When r5 moves down, c1 can move left, then r1 can move up. 3 moves for chain A.
# r2(V,r1,c3,2): blocker at col3. Chain: c1 also blocks r2 up (c1 covers col2-3). After c1 moves, r2 up. No extra chain.
# r3(V,r1,c4,2): blocker at col4. Chain: c2(H,r0,c4,2) blocks r3,r4 up. r6(V,r0,c3,2) blocks c2 left.
#   When r6 moves down, c2 can move left, then r3 up. 3 moves for chain B.
# r4(V,r1,c5,2): blocker at col5. After c2 moves, r4 up. 1 extra move.
# Total: r5 down(1) + c1 left(1) + r1 up(1) + r2 up(1) + r6 down(1) + c2 left(1) + r3 up(1) + r4 up(1) + T(1) = 9 moves.
# Check for conflicts:
# r5(V,r0,c1,2): rows0-1,col1. c1(H,r0,c2,2): row0,col2-3. No overlap.
# r6(V,r0,c3,2): rows0-1,col3. c1 at row0,col2-3: (0,3) has c1 right end AND r6 at (0,3)! OVERLAP! Bad.
# Fix: use c3(H,r0,c4,2) instead of c2, and use different chain for r3,r4.
# Or: shift r6 to col4: r6(V,r0,c4,2). c2(H,r0,c4,2) would overlap with r6 at (0,4). Still bad.
# Key insight: chains need V pieces at row0 (to block H pieces going left), but H pieces at row0 block V pieces going up.
# They can't occupy the same cell.
# Solution: use row-1 as buffer... but row-1 doesn't exist.
# Alternative: use brontosaurus (len=3) so it can move from row0 to row2+, freeing the H blocker path.
# b1(V,r0,c1,3): rows0-2,col1. Blocks c1 going left (col1,row0 occ). b1 can go down: row3,col1 free -> down 1=rows1-3. row0,col1 free. c1 can now go left.
# c1(H,r0,c2,2): row0,col2-3. Blocks r1,r2 up. After b1 down 1, c1 left 1=col1-2 (col1,row0 free). row0,col2,col3 now free (c1 at col1-2, col2 occupied). Hmm c1 left: new pos col1-2, col2 still in c1. r1 up blocked.
# c1 left 2=col0-1. col2,col3 free. r1,r2 up.
# But can c1 go left 2? col-1 OOB. c1 at col2-3: left 2 = col0-1. col0,col1 free? b1 at col1: if b1 moved to rows1-3, row0,col1 free. col0 free. OK.
# Sequence for chain A: b1 down 1(1) + c1 left 2(1) + r1 up(1) + r2 up(1) = 4 moves for 2 blockers.
# Chain B for r3,r4: similar setup. b2(V,r0,c4,3) blocks c2(H,r0,c4,2)? b2 at rows0-2,col4, c2 at row0,col4-5 - overlap at (0,4). Bad.
# Use b2(V,r0,c5,3): rows0-2,col5. c2(H,r0,c4,2): row0,col4-5 - (0,5) overlap with b2. Bad.
# b2(V,r3,c4,3): rows3-5,col4. Blocks r3(rows1-2,col4) from going down (row3,col4 occ). c2 blocks r3 up.
# c2(H,r0,c4,2): row0,col4-5. r3(rows1-2,col4) up: row0,col4 occ. Blocked. r3 down: row3,col4 has b2. Blocked. r3 STUCK unless c2 moves.
# c2 left: col3-4(1), col2-3(2)... (0,3) has c1 after c1 moved. This is getting very complicated.

# Let me take a practical approach: just put together levels that I know work from BFS tests.
# I'll use variations of working patterns.

# For levels 36-45 and 46-50, use BFS-driven design:
# Design a level, check BFS, if wrong par, adjust.

# Key insight from tests: the lv28-style design (b1 blocking multiple V pieces) works well.
# Let me use consistent reliable patterns:

def make_high_par_6x6_A(extra_pieces=[]):
    """Base: 4 V blockers, b1 blocks 3 up, e blocks 1 up, b2 blocks 3 down. ~8 moves."""
    base = [
        ('tx','t',2,0,2,'H'),
        ('r1','r',1,2,2,'V'),
        ('r2','r',1,3,2,'V'),
        ('r3','r',1,4,2,'V'),
        ('r4','r',1,5,2,'V'),
        ('b1','b',0,2,3,'H'),   # row0,col2-4 blocks r1,r2,r3 up
        ('e1','e',0,5,1,'H'),   # blocks r4 up
        ('b2','b',3,2,3,'H'),   # row3,col2-4 blocks r1,r2,r3 down
        ('e2','e',3,5,1,'H'),   # blocks r4 down
    ] + extra_pieces
    return base

# Base gives BFS=? Let's test first.
base_test, bp = lv(6,6,2, make_high_par_6x6_A(), 'test', '🦕')
print(f"  Base A: BFS={bp}")

# Now add extra pieces to increase par:
# If we block b1 from moving easily, that adds moves.
# b1(H,r0,c2,3): can go left (col0-1,1 step; col-1,OOB - max left=2 to col0-1) or right (col3-5:col5 is OOB since len3+start? col3+3=col6 OOB. max right to col3,len: col3-5,col5=5 is valid in 6-wide. col3+3-1=col5. OK!).
# Actually b1(H,r0,c2,3) right 1 = col3-5. col2 freed! r1 up. col3,col4 occupied by b1. r2 blocked.
# b1 right 2 = col4-6. col6 OOB. Can't.
# b1 left 1 = col1-3. col2 still in b1.
# b1 left 2 = col0-2. col3 freed. r2 up. col2 still in b1. r1 blocked.
# Hmm. b1 can free col3 (left 1) or col2 (right 1) but not both at once.
# If b1 right 1: r1 up(col2 free). b1 left: can it now go left? b1 at col3-5. left 1=col2-4 (col2 might have r1 in rows0-1 after r1 moved up). If r1 moved to rows0-1 (up 1), then row0,col2 has r1. b1 can't go to col2.
# This topology requires b1 to move multiple times or separate.

# Let me just test directly:
lv36, p36 = lv(6,6,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),
    ('r4','r',1,5,2,'V'),
    ('b1','b',0,2,3,'H'),
    ('e1','e',0,5,1,'H'),
    ('b2','b',3,2,3,'H'),
    ('e2','e',3,5,1,'H'),
    ('c1','c',4,1,2,'H'),   # extra piece in row4 (irrelevant?)
], names[36], icon_for(6))
ALL_LEVELS.append(lv36)
print(f"Lv36 {names[36]}: BFS={p36}")

# Let me pivot to a completely different approach: use an automated search.
# I'll randomize piece placement and check BFS until I get desired par.
import random
random.seed(42)

def random_level_5x5(target_par, exitRow=2, max_tries=5000):
    """Try random 5x5 levels until BFS matches target_par."""
    cols, rows = 5, 5
    for _ in range(max_tries):
        grid = [[False]*cols for _ in range(rows)]
        # Place T-Rex
        grid[exitRow][0] = grid[exitRow][1] = True
        pieces_def = [('tx','t',exitRow,0,2,'H')]

        # Add 2-5 random pieces
        n_pieces = random.randint(2, 5)
        piece_ids = {'r':0,'c':0,'b':0,'e':0}
        ok = True
        for _ in range(n_pieces):
            ptype = random.choice(['r','r','r','c','c','b','e'])
            if ptype == 'b':
                plen = 3
            elif ptype == 'e':
                plen = 1
            else:
                plen = 2
            pdir = random.choice(['H','V']) if ptype not in ('e','t') else 'H'
            # Pick random position
            attempts = 0
            placed = False
            while attempts < 100:
                attempts += 1
                if pdir == 'H':
                    r = random.randint(0, rows-1)
                    c = random.randint(0, cols-plen)
                    cells = [(r, c+i) for i in range(plen)]
                else:
                    r = random.randint(0, rows-plen)
                    c = random.randint(0, cols-1)
                    cells = [(r+i, c) for i in range(plen)]
                if all(not grid[rr][cc] for rr,cc in cells):
                    for rr,cc in cells:
                        grid[rr][cc] = True
                    piece_ids[ptype] += 1
                    pid = f"{ptype}{piece_ids[ptype]}"
                    pieces_def.append((pid, ptype, r, c, plen, pdir))
                    placed = True
                    break
            if not placed:
                ok = False
                break
        if not ok:
            continue

        test_lv = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,
                   'name':'test','icon':'🦕',
                   'pieces':[make_piece(pid,pt,r,c,l,d) for pid,pt,r,c,l,d in pieces_def]}
        result = solve(test_lv)
        if result == target_par:
            return pieces_def, result
    return None, -1

def random_level_6x6(target_par, exitRow=2, max_tries=10000):
    """Try random 6x6 levels until BFS matches target_par."""
    cols, rows = 6, 6
    for _ in range(max_tries):
        grid = [[False]*cols for _ in range(rows)]
        tx_col = random.choice([0, 1])
        for i in range(2):
            grid[exitRow][tx_col+i] = True
        pieces_def = [('tx','t',exitRow,tx_col,2,'H')]

        n_pieces = random.randint(3, 7)
        piece_ids = {'r':0,'c':0,'b':0,'e':0}
        ok = True
        for _ in range(n_pieces):
            ptype = random.choice(['r','r','r','c','c','b','e'])
            if ptype == 'b':
                plen = 3
            elif ptype == 'e':
                plen = 1
            else:
                plen = 2
            pdir = random.choice(['H','V']) if ptype not in ('e','t') else 'H'
            attempts = 0
            placed = False
            while attempts < 100:
                attempts += 1
                if pdir == 'H':
                    r = random.randint(0, rows-1)
                    c = random.randint(0, cols-plen)
                    cells = [(r, c+i) for i in range(plen)]
                else:
                    r = random.randint(0, rows-plen)
                    c = random.randint(0, cols-1)
                    cells = [(r+i, c) for i in range(plen)]
                if all(not grid[rr][cc] for rr,cc in cells):
                    for rr,cc in cells:
                        grid[rr][cc] = True
                    piece_ids[ptype] += 1
                    pid = f"{ptype}{piece_ids[ptype]}"
                    pieces_def.append((pid, ptype, r, c, plen, pdir))
                    placed = True
                    break
            if not placed:
                ok = False
                break
        if not ok:
            continue

        test_lv = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,
                   'name':'test','icon':'🦕',
                   'pieces':[make_piece(pid,pt,r,c,l,d) for pid,pt,r,c,l,d in pieces_def]}
        result = solve(test_lv)
        if result == target_par:
            return pieces_def, result
    return None, -1

print("\nSearching for random levels...")
# Search for levels 37-50 using random search
targets = {
    37: (6,6,2,9),
    38: (6,6,3,9),
    39: (6,6,2,10),
    40: (6,6,3,10),
    41: (6,6,2,10),
    42: (6,6,3,11),
    43: (6,6,2,11),
    44: (6,6,3,12),
    45: (6,6,2,12),
    46: (6,6,3,11),
    47: (6,6,2,12),
    48: (6,6,3,12),
    49: (6,6,2,13),
    50: (6,6,3,14),
}

random_results = {}
for lv_num, (cols, rows, exitRow, target) in targets.items():
    pieces_def, found_par = random_level_6x6(target, exitRow, max_tries=20000)
    if pieces_def is not None:
        random_results[lv_num] = (pieces_def, found_par, cols, rows, exitRow)
        print(f"  Lv{lv_num}: Found par={found_par} with {len(pieces_def)} pieces")
    else:
        print(f"  Lv{lv_num}: NOT FOUND for target={target}")

# Print summary so far
print(f"\nManually designed levels: {len(ALL_LEVELS)}")
print(f"Random levels found: {len(random_results)}")
