import sys
sys.path.insert(0, '/home/user/Dino')
from solver import solve, make_piece, LEVELS

def check(lv):
    return solve(lv)

# Levels 7-15: 5x5, par 4-7
# Levels 16-25: 6x6, par 5-8
# Levels 26-35: 6x6, par 7-10
# Levels 36-45: 6x6, par 9-12
# Levels 46-50: 6x6, par 11-14

new_levels = []

# ── Lv7: 5x5, exitRow=2, ~4 moves ──
# Grid:
#  . . r1 . .
#  . . r1 c1 c1
#  T T .  .  .  -> exit
#  . . .  .  .
#  . . .  .  .
# r1(V,r0,c2,len2) blocks col2 rows 0-1, but exit row is clear
# Actually need something blocking T-Rex path
# T-Rex at row2, blocking: need piece at (2, col>=2)
# r1(V,r0,c2,len2): rows0-1,col2 - doesn't block row2
# Let's put c1(H,r2,c2,len2) blocking T-Rex exit path
# Then r1(V,r1,c2,len2) blocking c1 from moving up
# c2(H,r0,c0,len2) blocking r1 from moving up
# Solution: c2 right -> r1 up -> c1 up -> T-Rex exit (4 moves)
lv7 = {'cols':5,'rows':5,'exitRow':2,'par':4,'name':'初學者','icon':'🦕',
 'pieces':[
    make_piece('tx','t',2,0,2,'H'),
    make_piece('c1','c',2,2,2,'H'),   # blocks exit row
    make_piece('r1','r',0,2,2,'V'),   # blocks c1 from going up (at rows 0-1, col2)
    make_piece('c2','c',0,0,2,'H'),   # blocks r1 from going further up? No, r1 at row0 can't go up
    # Actually r1(V,r0,c2) occupies rows0,1 col2. c1(H,r2,c2) occupies row2,col2-3
    # c1 can move up to row1? No, r1 is at row1,col2 blocking. c1 can move down.
    # c1 down 1 -> row3,col2-3. Then T-Rex can exit. That's 2 moves.
    # Need to block c1 from going down directly.
    make_piece('e1','e',3,2,1,'H'),   # egg at row3,col2 blocks c1 going down
    # Now c1 must go up. But r1(V,r0,c2) is at rows0-1,col2. c1 needs col2 row1 clear.
    # r1 at row0-1,col2 blocks c1 at row2 from moving up to row1.
    # So: r1 must move first. r1(V) can move down: row2 col2 has c1, blocked. Up: row-1, can't.
    # r1 is stuck! Need to unblock r1.
    # Let's restructure completely.
 ]}

# Restart lv7 with cleaner design
# 5x5, exitRow=2, ~4 moves
# Layout:
#  . c1 c1 . .
#  . .  r1 . .
#  T T  r1 . .  -> exit
#  . .  .  . .
#  . .  e1 . .
# r1(V,r1,c2,len2): rows1-2,col2. Blocks T-Rex.
# c1(H,r0,c1,len2): rows0,col1-2. Blocks r1 from going up (col2,row0 occupied).
# e1 at row4,col2 blocks r1 from going down.
# Solution: c1 left 1 (to c0-1? no, col can't be -1). c1 right 2 (to col3-4).
# Then r1 up 1 -> rows0-1. Then T-Rex exits. = 3 moves. Need 4.
# Add one more blocker.
# Add r2(V,r3,c3,len2) to block something...
# Or: c1(H,r0,c1,len2), r1(V,r0,c2,len2) - r1 occupies rows0-1
# If c1 is at row0,col1-2, and r1 at row0-1,col2: they overlap at (0,2)! Bad.

# Clean approach for lv7:
# 5x5 exitRow=2, par=4
#  . . . r1 .
#  . . . r1 .
#  T T c1 c1 .  -> exit
#  . . . .  .
#  . . . .  .
# c1(H,r2,c2,len2) blocks T-Rex. r1(V,r0,c3,len2) blocks c1 from going right (col3,row2).
# Wait c1 occupies col2-3. r1 occupies col3,row0-1. c1 wants to go right to col3 - blocked by r1.
# c1 can go left: col0-1,row2. But tx occupies col0-1,row2! Blocked.
# So c1 can't move. Add space: tx at col0, c1 at col2-3, tx len=2 so col0-1. c1 at col2-3.
# c1 left would go to col1-2 or col0-1? Moving left 1 = col1-2. col1,row2 free. So c1 can go left 1.
# But then T-Rex can only advance to col2 (c1 now at col1-2, col2 blocked). Hmm.
#
# Better: block c1 from moving left too.
# e1(egg) at row2,col1 would block c1 from moving left. But T-Rex is at col0-1,row2, so col1 is T-Rex!
#
# Let me use a different structure:
# 5x5 exitRow=1, par=4
#  . . r1 . .
#  T T r1 . .  -> exit  (r1 V at rows0-1,col2)
#  . c1 c1 . .  (c1 H at row2,col1-2)
#  . . r2 . .
#  . . r2 . .   (r2 V at rows3-4,col2)
# r1 is blocked from going down by c1(row2,col2). Blocked from going up (row-1 invalid).
# c1 can go left (col0-1? col0,row2 free -> c1 left 1 = col0-1).
# Then r1 down 2 -> rows2-3. But r2 at rows3-4,col2 blocks (row3,col2 occupied). r1 down 1 = rows1-2.
# After c1 moves left 1: r1 down 1 -> rows1-2. Now row0,col2 free.
# Wait r1 was at rows0-1. After r1 down 1 -> rows1-2. T-Rex at row1, col0-1. col2,row1 now has r1. Still blocked!
# r1 down 2: rows2-3. But row3,col2 has r2. Blocked. r1 down 1 only.
# Hmm. Let's try:
# Solution: c1 left 1 -> r1 up? Can't (row-1). r1 down: row2 free (c1 moved to col0-1). r1 down 1->rows1-2, still blocks.
# r1 down 2: row2 free (c1 gone), row3 has r2 - blocked.
# This is getting complicated. Let me just try specific designs and verify with BFS.

# LV7: Simple 5x5, exitRow=2, par=4
# T-Rex row2. Two pieces blocking, need chain of 3+1=4 moves.
lv7 = {'cols':5,'rows':5,'exitRow':2,'par':4,'name':'初學者','icon':'🦕',
 'pieces':[
    make_piece('tx','t',2,0,2,'H'),
    make_piece('r1','r',1,2,2,'V'),   # V, rows1-2, col2 - blocks T-Rex at (2,2)
    make_piece('c1','c',1,3,2,'H'),   # H, row1, col3-4 - blocks r1 from going right? No r1 is V.
    # r1(V) moves up/down. Up: row0,col2 free -> r1 up 1 = rows0-1. Then col2,row2 free. T-Rex exits.
    # That's only 2 moves. Need to block r1 from going up.
    make_piece('e1','e',0,2,1,'H'),   # egg at row0,col2 blocks r1 going up
    # Now r1 must go down. Row3,col2 free -> r1 down 1 = rows2-3. Still at row2!
    # r1 down 2 = rows3-4. Then T-Rex exits. 3 moves total (r1 down 2 = 1 move, T-Rex = 1 move? No, r1 down 2 is 1 move)
    # r1 down 2 is a SINGLE move (slide 2 cells = 1 move). Then T-Rex exits = 1 move. Total = 2. Not 4.
    # Need multiple pieces in the chain.
 ]}

# Let me think more carefully about 4-move puzzles.
# 4-move chain: A blocks T, B blocks A, C blocks B, D blocks C (or similar)

# LV7: 5x5, exitRow=2, par=4
# r1(V, row0,col2,len2): rows0-1,col2
# c1(H, row2,col2,len2): rows2,col2-3 - BLOCKS T-Rex
# r2(V, row2,col4,len2): rows2-3,col4
# e1: row2,col1 - wait T-Rex at col0-1 row2. col1 is T-Rex body.
#
# Cleaner:
# c1(H,row2,c3,len2) blocks cols3-4 of exit row - but T-Rex needs to pass col2,3,4
# T-Rex len=2, starts col0. Exits when col+2>5, so col>=4. T-Rex must slide to col4 (occupies 4-5, exit).
# Actually T-Rex exits when col+len > cols, i.e., col+2>5, col>3, col>=4.
# So T-Rex needs cells 2,3,4 in exit row to be clear (it needs to slide right).
# Any piece at (exitRow, col>=2) blocks T-Rex.

# Simple 4-move:
# r1(V,r0,c2,len2) at rows0-1,col2 blocks T-Rex at (2,2)
# c1(H,r0,c3,len2) at row0,col3-4 blocks r1 from moving up (row0,col2 is... wait c1 is at col3-4, not col2)
# r1 can move up: row-1 invalid (can't). r1 can move down: row2,col2 = ? T-Rex occupies row2,col0-1. col2 row2 is free.
# r1 down 1 = rows1-2. Still blocking row2! r1 down 2 = rows2-3. row2,col2 - occupied by r1 itself as it moves...
# Actually moving r1 down means its top goes to row1+1=row2 for 1 step, rows2-3. Row2,col2 is now r1's top. Still blocks T-Rex!
# r1 down 3 = rows3-4. Now rows1-2 free. But row3-4 must be clear. T-Rex can exit (row2,col2 now free). That's 2 moves.

# The issue is T-Rex only needs col2 to be free in row2 (then it slides all the way out).
# For 4 moves we need at least 3 pieces to move.

# LV7: 5x5, exitRow=2, par=4
# Layout:
#  e1  .  .  .  .
#  .   .  r1 c1 c1
#  T   T  r1 .  .   -> exit
#  .   .  r2 .  .
#  .   .  r2 .  .
# r1(V,r1,c2,len2): rows1-2,col2. Blocks T-Rex.
# c1(H,r1,c3,len2): row1,col3-4. Blocks r1 from going right? r1 is V, moves up/down.
# r1 up: row0,col2 free -> up 1 = rows0-1. T-Rex can exit. 2 moves.
# Block r1 going up: put e1 at row0,col2. Now r1 must go down.
# r2(V,r3,c2,len2): rows3-4,col2. Blocks r1 going down past row3.
# r1 down: row3,col2 has r2 - blocked. r1 can't move! Puzzle unsolvable.
#
# Need r2 to be movable first. r2 can go left or... r2 is V, moves up/down.
# r2 up: row2,col2 free (T-Rex at col0-1, col2 row2 free). r2 up 1 = rows2-3. Still blocks r1.
# r2 up blocked by r1 at row2? No, r1 is at rows1-2. row2,col2 has r1. So r2 can't go up.
#
# This is getting complex. Let me try a fresh approach - use c pieces (H) to create simpler chains.

# LV7: 5x5, exitRow=1, par=4
#  .  r1  .  .  .
#  T  T   r1 .  .   -> exit  (r1 V rows0-1 col2, blocks T-Rex at row1,col2)
#  .  c1  c1 .  .   (c1 H row2 col1-2, blocks r1 from going down)
#  .  .   .  r2 .
#  .  .   .  r2 .   (r2 V rows3-4 col3)
# r1 can go up (row-1 invalid). r1 down: row2,col2 has c1 - blocked.
# c1 can go left: col0-1? col0,row2 free, col1,row2 free. c1 left 1 = col0-1. (1 move)
# Now r1 down: row2,col2 free. r1 down 1 = rows1-2. row1,col2 still occupied by r1! Still blocks T.
# r1 down 2 = rows2-3. row1,col2 free. T-Rex exits. Total: 3 moves. Need 4.
# Add one more blocker: c2(H,r2,c3,len2) row2,col3-4. Now c1 going left is fine (col2,row2 now has c2? no c2 is col3-4).
# c1(col1-2) going left 1 = col0-1. r1 down: row2 col2 free (c1 moved). rows2-3. But c2 at row2,col3-4 - doesn't affect col2.
# Still 3 moves.
# Let me add: c2 blocks r1 from going all the way down. r2 at rows3,col2 (egg) blocks r1 from going to rows3-4.
# e1(egg) at row3,col2. r1 can only go down 1 (to rows1-2 from rows0-1). Still blocks. Down 2 = rows2-3, row3,col2=egg. Down 1 = rows1-2 still blocks.
# Hmm. For r1 to unblock row1, it needs to go to rows2-3 minimum (down 2 from rows0-1).
# If e1 at row3,col2: r1 max down = 2 (rows2-3), with row2,col2 free and row3,col2 = egg blocked. So down 1 only (rows1-2).
# Still blocked.
#
# Different approach: T-Rex at col1 (not col0).
# LV7: 5x5, exitRow=2, par=4
#  .  .  .  .  .
#  .  .  r1 .  .
#  .  T  T  r1 .   -> exit  tx at row2,col1
#  .  .  c1 c1 .   c1 H row3,col2-3
#  .  .  .  e1 .   e1 egg row4,col3
# r1(V,r1,c2,len2) rows1-2,col2. Blocks T-Rex (tx at col1-2, row2).
# Wait tx occupies col1-2. r1 at col2,row2 - they OVERLAP. Bad.
#
# OK let me just carefully design and test with BFS. I'll write several candidates.

def lv_candidate(cols, rows, exitRow, pieces_def):
    """pieces_def: list of (id, type, row, col, len, dir)"""
    pieces = [make_piece(pid, pt, r, c, l, d) for pid,pt,r,c,l,d in pieces_def]
    lv = {'cols':cols,'rows':rows,'exitRow':exitRow,'par':0,'name':'test','icon':'🦕','pieces':pieces}
    result = solve(lv)
    return result

# Test candidates for lv7 (5x5, exitRow=2, want ~4)
print("Testing lv7 candidates...")

# Candidate A:
# r1(V,r0,c2,2): rows0-1,col2. Blocks T at (2,2) - wait T is at row2, r1 at rows0-1, doesn't block row2!
# c1(H,r2,c2,2): rows2,col2-3. Blocks T-Rex.
# r1(V,r1,c2,2): rows1-2,col2. Overlaps with c1 at (2,2)! Bad.

# Let's be systematic. T-Rex at row2,col0,len2. Needs col2,3,4 (in row2) to be clear eventually.
# Direct blocker: piece at (2, 2) or (2,3) or (2,4).
# If piece at (2,2):
#   - V piece: rows a to a+len-1 containing row2. It needs to move up or down to clear row2.
#   - H piece: row2, must move left (but T-Rex is at col0-1) or right.

# r1(V,r1,c3,2): rows1-2,col3. Blocks T at (2,3).
# c1(H,r2,c2,2): row2,col2-3. Blocks T at (2,2) AND (2,3) overlap with r1 at (2,3)! Bad.

# Let's keep it simple: one direct blocker + chain.

# c1(H,r2,c3,2): row2,col3-4. Blocks T-Rex (needs to reach col3+).
# r1(V,r0,c3,2): rows0-1,col3. Blocks c1 from going... c1 is H, moves left/right.
#   c1 left: col2-3. row2,col2 free? Yes (T at col0-1). c1 can go left 1.
#   Then T-Rex exits? T at col0, needs col2,3 clear. After c1 moves to col2-3, col3 free but col2 blocked! No.
#   T needs its path: slides right from col0. At col2, c1 now at col2-3 - still blocked.
#   c1 must go right: col4-5, out of bounds (cols=5, max col is 4, c1 at col3+1=4 ok, col3+2=5 out of bounds for len2, actually col4 would make it occupy col4-5, col5 out of bounds). So c1 can go right at most to col3 (stays). max right for c1 at col3: col3+2=5 >= cols=5, so c1 can go right 0. col3+2=5=cols, so c1 occupies col3,col4 which is fine but moving right 1 would put it at col4,col5 - col5 out of bounds. So c1 can't go right.
#   Hmm. Let's put c1 at col2-3 originally.
# c1(H,r2,c2,2): row2,col2-3. T needs these clear.
# c1 can go right: col3-4, then col4-5 (out of bounds), so max right = 1 (to col3-4).
#   After c1 right 1: col2,row2 free. T slides right through col2, col3(c1),- blocked at col3.
#   T needs col2,col3,col4 clear (actually T at col0, slides right: col2 free, col3 has c1). Still blocked.
#   c1 needs to move further. c1 at col3-4: col4+1=5=cols, can't go more right.
# c1 left: col0-1(row2). T at col0-1. Overlap! Can't.
#   c1 left 1: col1-2. T at col0-1, row2. col1,row2 has T. Blocked.
# So c1(H,r2,c2,2) can ONLY go right 1 step (to col3-4), which doesn't fully clear path.
# Conclusion: for 5x5, the direct blocker should be a V piece in the exit row.

# V piece in exit row: r1(V,r1,c2,2) occupies rows1-2,col2.
# r1 can go up: row0,col2 must be free.
# r1 can go down: row3,col2 must be free.
# If r1 up 1 -> rows0-1: row2,col2 free. T exits. 2 moves total.
# Need to block r1 going up AND going down initially, requiring chain.

# Block r1 going up: piece at row0,col2.
# Block r1 going down: piece at row3,col2.
# If both are movable, we need to move one of them first.

# Piece at row0,col2: c2(H,r0,c2,2) occupies row0,col2-3.
#   c2 can go left: col0-1,row0. col0 row0 free, col1 row0 free. c2 left 1 = col1-2. col2 still occupied! Left 2 = col0-1. Then row0,col2 free.
#   c2 left 2: col0-1. (1 move). Then r1 up 1: rows0-1. (1 move). T exits. 3 moves.
# Piece at row3,col2: not needed if we can get 4 moves another way.

# For 4 moves, add another blocker for c2 going left.
# e1(egg) at row0,col1: blocks c2 from going left 2.
#   c2 can only go left 1 (to col1-2, but col1,row0 has egg! can't).
#   Wait c2 moving left: left edge moves from col2 to col2-steps. If e1 at col1,row0: c2 can go left 0 (col1 blocked). c2 can go right: col3-4 (row0,col3 free, col4 free). c2 right 1 = col3-4. row0,col2 free.
#   Then r1 up 1. T exits. 3 moves.

# Still 3. Need one more step.
# Add piece blocking r1 going up even after c2 moves.
# r2(V,r0,c2,2) at rows0-1,col2 - but r1 is at rows1-2,col2. Overlap at row1,col2! Bad.

# Let me try: two pieces blocking T-Rex.
# r1(V,r1,c2,2): rows1-2,col2.
# r2(V,r1,c3,2): rows1-2,col3.
# Both block T-Rex (col2 and col3 in row2).
# c1(H,r0,c2,2): row0,col2-3. Blocks both r1 and r2 from going up.
# Solution: c1 left 2 (to col0-1) -> r1 up 1 -> r2 up 1 -> T exits. 4 moves!
# Check c1 left 2: col0,row0 free? Yes. col1,row0 free? Yes. OK.
# After c1 left: row0,col2 and row0,col3 free.
# r1 up 1: rows0-1,col2. Row2,col2 free.
# r2 up 1: rows0-1,col3. But row0,col2 has r1 (after r1 moves up)! r2 is at col3, row0,col3 - that's different from r1 at col2. OK no overlap.
# After r2 up 1: row2,col3 free. T-Rex can now exit (col2,col3 free, col4 also free). T exits. 4 moves!
# Let's verify: are there shorter solutions?
# Can we do it in 3?
#   c1 right: c1 at col2-3, right 1 = col3-4. row0,col2 free (for r1 up). row0,col3 occupied by c1.
#   r1 up 1: rows0-1. row2,col2 free.
#   T-Rex: col2 free, col3 still has r2 rows1-2. Blocked at col3.
#   r2 up 1: rows0-1,col3. But c1 at col3-4,row0! row0,col3 occupied. r2 can't go up.
#   r2 down: rows2-3,col3. row2,col3 still occupied by r2's top? No: r2 moves down 1 = rows2-3. row2 still has r2 top. Still blocks T.
#   r2 down 2 = rows3-4. row2,col3 free. T exits. But that's c1 right, r1 up, r2 down 2, T = 4 moves. Same count.
#
# Minimum is 4? Let's check: can T exit in fewer with this layout?
# T needs row2,col2 and col3 clear (min: slide to col3+, then exit when col+2>5 means col>=4, so needs col4 too?
# T-Rex len=2. T at col0. Slides right. Can exit when col+2>5 i.e. col>=4.
# But T can't skip over pieces. T needs all cols from 2 to 3 free (to reach col4). Actually:
# T at col2: occupies col2-3. col3 must be free when T is at col2.
# T at col3: occupies col3-4. col4 must be free.
# T at col4: occupies col4-5. col5 out of bounds -> EXIT. Win!
# So T needs cols 2,3,4 free in row2.
# r1 at col2 and r2 at col3 both block. Both must move. c1 blocks both from going up.
# Minimum moves: c1 (1) + r1 (1) + r2 (1) + T (1) = 4. Correct.

r_lv7 = lv_candidate(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),   # rows1-2,col2
    ('r2','r',1,3,2,'V'),   # rows1-2,col3
    ('c1','c',0,2,2,'H'),   # row0,col2-3, blocks r1,r2 going up
])
print(f"  Lv7 candidate: BFS={r_lv7}")

# Lv8: 5x5, exitRow=2, par=5
# Extend lv7 by adding one more blocker for c1.
# c1(H,r0,c2,2) blocked from going left by e1(egg) at row0,col1.
# Then c1 must go right (to col3-4). row0,col2 free. r1 up. row2,col2 free.
# But r2 still blocks col3. r2 up: row0,col3 free (c1 moved to col3-4... wait col3 has c1!).
# c1 at col3-4: row0,col3 occupied. r2 can't go up. r2 must go down.
# r2 down 1: rows2-3. row2,col3 still occupied (r2 top).
# r2 down 2: rows3-4. row2,col3 free. T exits.
# Total: c1 right(1) + r1 up(1) + r2 down 2(1) + T exit(1) = 4 moves. Still 4!
#
# Let me add r3(V,r3,c3,2) rows3-4,col3 to block r2 from going down.
# Then: c1 right -> r1 up -> r2: can't go up (c1 there) can't go down (r3 there) - STUCK. Unsolvable.
#
# Need a different chain for 5 moves.

# Lv8: 5x5, exitRow=2, par=5
# Three blockers in exit row:
# r1(V,r1,c2,2), r2(V,r1,c3,2), r3(V,r1,c4,2) all block cols2-4 in row2.
# c1(H,r0,c2,2) blocks r1,r2 up. r3 can go up freely (row0,col4 free).
# Solution: r3 up(1) -> c1 right 2(1) [to col4-5? no col5 OOB. col4+1=5=cols, c1 right max=1 to col3-4. But r3 moved to rows0-1,col4... row0,col4 now r3. c1 at col2-3, right 1 = col3-4. row0,col3 free,col4 has r3. c1 right 1 ok (col3-4, row0,col3 free, row0,col4 no r3 doesn't matter for row0,col4 - wait r3(V) after up 1 is at rows0-1,col4. row0,col4 occupied. c1 right 1 = col3-4: occupies row0,col3,col4. col4,row0 has r3. OVERLAP! Bad.
# c1 can only go left: col0-1,row0 free. c1 left 1 = col1-2 (col2 still occupied by c1). left 2 = col0-1. Row0,col2,col3 free.
# Then r1 up(1) + r2 up(1) + T exit(1). Total: r3 up + c1 left 2 + r1 up + r2 up + T = 5 moves!
# Check for shorter: can we skip r3 up? Without r3 up, r3 at rows1-2,col4 blocks T.
# c1 left 2: row0,col2,col3 free. r1 up + r2 up: col2,col3 free in row2. r3 still at row2,col4. T blocked.
# r3 up: row0,col4 free (c1 moved). r3 up 1 = rows0-1. row2,col4 free. T exits.
# So: c1 left 2(1) + r1 up(1) + r2 up(1) + r3 up(1) + T(1) = 5 moves.
# Or: r3 up(1) + c1 left 2(1) + r1 up(1) + r2 up(1) + T(1) = 5 moves.
# Is there a 4-move solution?
# r1,r2,r3 all block row2. Need all 3 to move + T = 4 pieces, but c1 blocks r1,r2.
# If c1 moves to unblock both r1 and r2 in 1 move, and r3 moves independently:
# c1 left 2(1) unblocks r1,r2. r1 up(1). r2 up(1). r3 up(1). T(1). = 5 minimum.
# BFS will confirm.

r_lv8 = lv_candidate(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),
    ('r2','r',1,3,2,'V'),
    ('r3','r',1,4,2,'V'),   # rows1-2,col4
    ('c1','c',0,2,2,'H'),   # row0,col2-3
])
print(f"  Lv8 candidate: BFS={r_lv8}")

# Lv9: 5x5, exitRow=2, par=5 or 6
# Different topology.
# b1(V,r0,c2,3): rows0-2,col2. Blocks T-Rex at (2,2).
# c1(H,r2,c3,2): row2,col3-4. Blocks b1 from going down (row3,col2 not blocked actually; col3 has c1 but col2 doesn't).
# Actually b1 at rows0-2,col2. b1 down: row3,col2 free -> down 1=rows1-3. Still at row2! down 2=rows2-4. row2,col2 still has b1. b1 would need to go down 3 to rows3-5 but row5 OOB. b1 down max = rows2-4? No, b1 len=3. rows0-2: down 1=rows1-3, down 2=rows2-4. Neither clears row2. b1 up: row-1 OOB. b1 CANNOT MOVE to clear row2! The bottom of b1 (len3) is always at row2 when it's as far down as possible in 5 rows (rows2-4). To clear row2, b1 must be at rows3+. But rows3+len-1=rows5 OOB. Impossible in 5 rows.
# So b1(V,len3) in a 5-row grid cannot be used as a direct blocker of the exit row if exitRow=2 (middle row).
# b1 up: if b1 at rows0-2, up is impossible (row-1). If b1 at rows1-3, up 1 = rows0-2. Still at row2 top if exitRow is row1.
# For exitRow=1: b1(V,r1,c2,3) rows1-3. b1 up 1 = rows0-2, still at row1. b1 up impossible (row0-2 is up 0, currently rows1-3). Going up 1 = rows0-2, still occupies row1. Hmm.
# Actually for exitRow=1, b1(V,r2,c2,3) rows2-4. b1 up 1 = rows1-3. row1,col2 occupied. Still blocks. b1 up 2 = rows0-2. row1,col2 still occupied!
# Brontosaurus V len3 can only clear a row if it can move far enough. In 5-row grid, b1 must start at rows2-4 and move to rows0-2 (up 2) to clear row3. But row3 with exitRow=3 would work. Or exitRow=0 with b1 starting at rows1-3 going up 1 to rows0-2, clearing rows1-3... still occupies row1 if row1 is exit. Actually going up 1: rows0-2. Row1 still in b1!
# Brontosaurus V can only clear exitRow if it moves at least (exitRow - start_row + len) or something.
# Conclusion: Don't use brontosaurus V as direct blocker for 5x5. Use it elsewhere.

# Lv9: 5x5, exitRow=1, par=5
# b1(V,r2,c2,3) rows2-4,col2. Doesn't block row1.
# r1(V,r0,c2,2) rows0-1,col2. Blocks T at (1,2). T at row1,col0.
# c1(H,r2,c1,2) row2,col1-2. Blocks r1 going down (row2,col2 occupied by c1 and b1!). Overlap c1 col2 and b1 col2 row2! Bad.

# Lv9: 5x5, exitRow=1, par=5
# r1(V,r0,c2,2) rows0-1,col2. Direct blocker.
# c1(H,r0,c3,2) row0,col3-4. Doesn't block r1 going up (row-1 OOB) or down.
# Let r1 be blocked going down: r2(V,r2,c2,2) rows2-3. r1 down: row2,col2 has r2. Blocked.
# r2 can go down: row4,col2 free -> r2 down 1=rows3-4. (1 move). Then r1 down 2 = rows2-3. row1 free. T exits. 3 moves.
# Add blocker for r2: e1(egg) at row4,col2. r2 can't go down. r2 up: row1,col2 has r1. Blocked. r2 stuck! Bad.
# Instead: c2(H,r2,c2,2) row2,col2-3. Blocks r1 down and r2 from... wait no r2 doesn't exist here.
#
# c2(H,r2,c2,2): row2,col2-3. Blocks r1 from going down (row2,col2 occupied).
# c2 can go left: col0-1,row2 free. c2 left 1 = col1-2. col2 still occupied. left 2 = col0-1. row2,col2 free.
# Then r1 down 2 = rows2-3. row0-1,col2 free. T exits. 4 moves total (c2 left 2, r1 down 2, T).
# Wait: c2 left 2 = 1 move, r1 down 2 = 1 move, T = 1 move. 3 moves total.
# For 5 moves need more chain.

# Let me just write a bunch of candidates and pick the ones BFS gives the right par for.

print("\nTesting more candidates...")

# Lv9: 5x5, exitRow=2, par=5 - use brontosaurus H
r_lv9a = lv_candidate(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),   # rows1-2,col2
    ('b1','b',0,2,3,'H'),   # row0,col2-4 (len3) - blocks r1 going up (row0,col2 occupied)
    ('r2','r',1,3,2,'V'),   # rows1-2,col3
    ('c1','c',3,2,2,'H'),   # row3,col2-3 - blocks r1,r2 going down
])
print(f"  Lv9a: BFS={r_lv9a}")

# Lv9b: simpler 5-mover
r_lv9b = lv_candidate(5,5,1,[
    ('tx','t',1,0,2,'H'),
    ('r1','r',0,2,2,'V'),   # rows0-1,col2 - blocks T at (1,2)
    ('c1','c',2,0,2,'H'),   # row2,col0-1
    ('r2','r',2,2,2,'V'),   # rows2-3,col2 - blocks r1 going down
    ('c2','c',2,3,2,'H'),   # row2,col3-4 - blocks r2 going right? r2 is V.
    # r2(V) blocked going down by e1 below?
    ('e1','e',4,2,1,'H'),   # egg row4,col2 blocks r2 going down more than 1
    # r2 down 1: rows3-4. row2,col2 free. r1 down: rows1-2. still in row1. r1 down 3: rows3-4. But row3,col2 has r2(after down1)... Actually r2 at rows3-4, r1 needs to go to rows2-3 or further. r1 can go down 2 from rows0-1 to rows2-3 (row2,col2 free after r2 moved, row3 has r2 top). r1 down 1=rows1-2 still blocks. r1 down 2=rows2-3: row2,col2 free, row3,col2 has r2 bottom. Blocked. r1 can only go down 1. Still blocks row1.
    # This topology doesn't work for exitRow=1.
])
print(f"  Lv9b: BFS={r_lv9b}")

# Let me try exitRow=2 for all 5x5 remaining and use known-good patterns.

# For 5 moves, use this pattern (extends lv7 4-move):
# Add one more layer: c2 blocks c1 from moving.

# Pattern: c2(H) blocks c1(H) by occupying the destination.
# c1 at row0,col2-3. If c2 at row0,col0-1, then c1 can't go left (col0-1 occupied). c1 must go right.
# c1 right: col3-4. row0,col3,col4 free. OK.
# After c1 right: row0,col2,col3 free. r1 up(1), r2 up(1), T(1). Total: c2 doesn't help here since c1 can go right.
# What if c2 is at row0,col4-5? col5 OOB. Hmm.

# Better: add e1(egg) at row0,col1 to block c1 going left, and add c2 at row0,col4 (H,len1? eggs only len1).
# e1 at row0,col1: c1(col2-3) can't go left (col1 occupied). c1 right 1 = col3-4. row0,col3,col4 free. OK.
# Now r1 up: row0,col2 free. r2 up: row0,col3 - c1 is at col3! r2 can't go up.
# r2 must go down. rows3-4,col3. row2,col3 free. T exits (col2 free after r1 up, col3 free after r2 down, col4 free).
# Total: e1 is fixed, so moves: c1 right(1) + r1 up(1) + r2 down(1) + T(1) = 4 moves. Same as before without e1!

# Hmm the egg doesn't add moves if c1 can still go right.
# Need to also block c1 going right: piece at row0,col4 (e2 egg? or r3).

# e2(egg) at row0,col4: c1(col2-3) can't go right to col3-4 (col4 occupied). c1 can't go left (e1 at col1). c1 STUCK.
# Puzzle unsolvable!

# OK different approach: use brontosaurus to create longer chains.
# b1(H,r0,c0,3): row0,col0-2. Blocks r1(V,r0,c2) from going up? b1 at col0-2 row0, r1 at col2 row0 - overlap! Bad.
# b1(H,r0,c2,3): row0,col2-4. Blocks r1(col2) and r2(col3) from going up. b1 must move left to free them.
# b1 left: col0-1(row0). col-1 OOB. left 1 = col1-3. col2 still occupied. left 2 = col0-2. col3,col4 free but col2 still has b1.
# For b1 to free col2: b1 must move right or very far left. b1 right: col3-5 (col5 OOB).
# b1 is at col2-4 (len3). right 1 = col3-5, col5 OOB. Can't go right.
# b1 left: col1-3 (still col2 blocked). left 2 = col0-2 (still col2 blocked!).
# b1 can never free col2 - col2 is always in b1 (positions col0-2, col1-3, col2-4). Hmm.
# Actually if b1 moves to col0-2 (left 2): col2 still has b1's rightmost cell.
# b1 can free col2 only if its rightmost cell < col2. That means b1 at col0-1 at max (len3, so col-1 needed). Impossible.
# b1(H,len3) starting at col2: cannot free col2. Bad choice.

# b1(H,r0,c1,3): row0,col1-3. Can go left: col0 free? col-1 OOB. left 0 only if col0 free...
# b1 at col1-3, left 1 = col0-2. Still col2 occupied.
# b1 right 1 = col2-4. Col4 is right edge. Col1 freed. Doesn't help col2.
# b1 right 2 = col3-5. col5 OOB. Can't.

# Conclusion: brontosaurus H can't free col2 in a 5-wide grid easily.
# Let me try brontosaurus V (len3) to block something else.

# For 5+ moves in 5x5, I'll use a different exit row pattern.

# Lv9: 5x5, exitRow=0, par=5
# T-Rex at row0. Exit at top... wait the game has T-Rex exit to the RIGHT (H direction). exitRow is the row, T always exits right.
# T at row0,col0. exitRow=0. Pieces blocking col2-4 in row0.

r_lv9c = lv_candidate(5,5,0,[
    ('tx','t',0,0,2,'H'),
    ('r1','r',0,2,2,'V'),   # rows0-1,col2 - blocks T at (0,2)
    ('r2','r',0,3,2,'V'),   # rows0-1,col3
    ('c1','c',2,2,2,'H'),   # row2,col2-3 - blocks r1,r2 going down (row2,col2 and col3)
    ('r3','r',2,4,2,'V'),   # rows2-3,col4 - extra piece
    ('c2','c',4,1,2,'H'),   # row4,col1-2
])
print(f"  Lv9c (exitRow=0): BFS={r_lv9c}")

# Try a more carefully designed 5-mover
r_lv9d = lv_candidate(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('c1','c',2,2,2,'H'),   # row2,col2-3 - direct blocker
    ('r1','r',0,2,2,'V'),   # rows0-1,col2 - blocks c1 going up? c1 is H, not V.
    # c1(H) can go left: col0-1 (T at col0-1! Overlap) or right: col3-4.
    # c1 right 1 = col3-4. row2,col2 free but col3 still has c1 top... wait c1 is H len2, at col3-4 after move. row2,col3 occupied. T at col0 slides to col1(free),col2(free),col3(c1)-blocked.
    # c1 right 2 = col4-5. col5 OOB (cols=5, max index=4). Can't.
    # So c1 can only go right 1, which doesn't clear path. Need c1 to go left.
    # c1 left: col0-1 overlaps with T at col0-1! Blocked.
    # c1 is STUCK (can't go left past T, can't go right enough). Bad design.
])
# Skip, known bad

# The key insight: for 5x5 exitRow=2, T at col0-1.
# Blocker in exit row must be a V piece (can move up/down), not H (H pieces can't fully clear).
# So all direct blockers should be V pieces in the exit row.

# For par=5: need 4 V blockers that need to be moved sequentially.
# But 4 V pieces in cols2-4 of a 5x5 = only 3 possible positions (col2,col3,col4).
# 3 V blockers + chain = 5 moves: 3 V pieces + 2 supporting moves.

# Let me try the pattern that worked for lv8 but make the support piece need 2 moves.
# lv8 had c1(H,r0,c2,2) blocking 2 V pieces. c1 went left 2 (1 move) to free both.
# For 1 more move: add c2(H,r0,c0,2) that blocks c1 going left.
# c1 can't go left (c2 at col0-1 blocks). c1 must go right 2 = col4-5 OOB.
# c1 right 1 = col3-4. Frees col2. But col3 still occupied by c1. r2 at col3 can't go up.
# After c1 right 1: r1 up (col2 free in row0). r2: row0,col3 has c1. Can't go up. r2 down.
# Row3,col3 free: r2 down 1 = rows2-3. row2,col3 still occupied. r2 down 2 = rows3-4. row2,col3 free. T exits.
# Total: c2 right? c2 must move to allow c1 to go somewhere.
# c2(H,r0,c0,2) right 1 = col1-2. row0,col0 free. But col2 occupied by c1! c2 can only go right to col1-2 if col1,col2 are free. col2 has c1. Blocked.
# c2 right 0. c2 left: col-1 OOB. c2 STUCK if c1 is at col2-3. Bad.

# Different: c2(H,r0,c0,2) -> needs c1 to first move, but c1 is blocked by c2. Deadlock.

# Try: c2(H,r0,c0,2) at col0-1. c1(H,r0,c3,2) at col3-4. These don't interfere.
# c1 at col3-4: c1 can't go right (col5 OOB). c1 left 1=col2-3, left 2=col1-2, left 3=col0-1 (occupied by c2).
# c1 left: col2-3(1), col1-2(2, but col1 has c2 right end!). left 2: col1 occupied by c2. c1 left 1 = col2-3 (col2,col3 occupied).
# This blocks r1(V,col2) and r2(V,col3) from going up (row0 has c2 at col0-1 and c1 at col3-4, but row0,col2 and col3 are free! - no wait c1 moved to col2-3).
# Initial: c1 at col3-4, row0. r1(V,r1,c2) rows1-2 (row0,col2 free), r2(V,r1,c3) rows1-2 (row0,col3 free? c1 at col3,row0! overlap if c1 is at col3-4). Bad: r2(V,r1,c3) and c1(H,r0,c3) overlap at row0,col3 if c1 is initial at col3-4!
# Let me reconsider: r2(V,r1,c4,2): rows1-2,col4. Uses col4 instead.
# Then: r1(V,r1,c2), r2(V,r1,c3), r3(V,r1,c4) - 3 blockers.
# c1(H,r0,c3,2): row0,col3-4. Blocks r2(col3) and r3(col4) going up.
# row0,col2 free: r1 can go up directly.
# r1 up(1). row2,col2 free. r2: row0,col3 has c1. Can't go up. r2 down: rows3-4. row2,col3 free. r3: row0,col4 has c1. Can't go up. r3 down: rows3-4,col4. But r2 now at col3,rows3-4 - different col. r3 down 1=rows2-3. row2,col4 free but row2 needs col4 for T. r3 down 2=rows3-4. row2,col4 free. T exits (col2 free[r1 up], col3 free[r2 down], col4 free[r3 down]).
# Total: r1 up(1) + r2 down 2(1) + r3 down 2(1) + T(1) = 4. Not 5.
# Wait, why doesn't c1 need to move? c1 blocks r2 and r3 from going up, but they can go down instead.
# So 4 moves.

# Hmm. Let me try a different topology to get 5 moves.

# 5-mover: need a piece that can only move after another piece moves, creating a longer chain.

# Pattern for 5 moves on 5x5:
#  e  .  r1  r2  .
#  .  .  r1  r2  r3
#  T  T  .   .   r3  -> exit
#  .  .  c1  c1  .
#  .  .  .   .   .
# r1(V,r0,c2,2): rows0-1,col2. Blocks T? No, T at row2. r1 at col2 rows0-1 doesn't block row2.
# I keep confusing myself. Let me be very explicit.
# T-Rex at row=2, col=0, len=2, dir=H. Occupies (2,0),(2,1).
# For T to exit, it needs to slide right. It needs (2,2),(2,3),(2,4) to be free.
# So blockers are pieces occupying (2,2), (2,3), or (2,4).

# Simple 5-mover attempt:
# r1(V,r1,c2,2): occupies (1,2),(2,2). Blocks (2,2).
# r2(V,r2,c3,2): occupies (2,3),(3,3). Blocks (2,3). [r2 starts at row2, so occupies rows2-3]
# r3(V,r1,c4,2): occupies (1,4),(2,4). Blocks (2,4).
# Now r1 can go up (if row0,col2 free) or down (if row3,col2 free).
# r2 can go up (if row1,col3 free, yes) or down (if row4,col3 free, yes).
# r3 can go up (if row0,col4 free) or down (if row3,col4 free).
# Each of r1,r2,r3 can move independently. Min moves = 3+1 = 4.
# To make it 5, one of them must need 2 supporting moves, or add another step.

# Block r1 going up: e1(egg) at (0,2). Then r1 must go down.
# r1 down: row3,col2 free -> r1 down 1 = rows2-3. Still at (2,2)! r1 down 2 = rows3-4. (2,2) free.
# r1 down 2 = 1 move.
# Block r2 going anywhere: e2 at (1,3) blocks r2 going up. e3 at (4,3) blocks r2 going down.
# r2 from rows2-3: up 1=rows1-2 (row1,col3 has e2!). Can't. Down 1=rows3-4 (row4,col3 has e3!). Can't. r2 STUCK. Bad.
# Instead block with movable piece: c1(H,r1,c3,2) at (1,c3-4). Blocks r2 going up (row1,col3 occupied by c1).
# c1 must move right: col4-5 (col5 OOB), or left: col2-3. col2,row1 - has r1(rows1-2). Blocked.
# c1 left 1 = col2-3: col2,row1 has r1. Blocked. c1 can't move?
# c1(H,r1,c3,2): right 1 = col4-5 OOB. left 1 = col2-3: col2,row1 has r1. STUCK if r1 hasn't moved.
# If r1 moves first (down 2): rows3-4, row1,col2 free. Then c1 left 1 = col2-3. Row1,col3 free. Then r2 up 1 = rows1-2. Row2,col3 free. Then... T still needs col4 (r3 at rows1-2,col4). r3 up: row0,col4 free -> r3 up 1 = rows0-1. Row2,col4 free. T exits.
# Total: r1 down 2(1) + c1 left(1) + r2 up(1) + r3 up(1) + T(1) = 5 moves!
# Check overlaps: r1(V,r1,c2), c1(H,r1,c3-4), r2(V,r2,c3), r3(V,r1,c4).
# r1 at (1,2),(2,2). c1 at (1,3),(1,4). r2 at (2,3),(3,3). r3 at (1,4),(2,4).
# c1(1,4) and r3(1,4) OVERLAP! Bad.
# Fix: r3(V,r2,c4,2) rows2-3,col4. r3 at (2,4),(3,4). c1(H,r1,c3,2) at (1,3),(1,4). No overlap now.
# r3 up: row1,col4 free -> r3 up 1=rows1-2. row2,col4 free.
# r3 up: row1,col4 - c1 is at (1,3),(1,4). row1,col4 has c1! r3 can't go up.
# r3 down: row4,col4 free -> down 1=rows3-4. row2,col4 free.
# Solution: r1 down 2(1) + c1 left(1) [to col2-3] + r2 up(1) + r3 down(1) [rows3-4] + T(1) = 5!
# Let's verify no overlaps initially:
# r1(V,r1,c2,2): (1,2),(2,2)
# r2(V,r2,c3,2): (2,3),(3,3)
# r3(V,r2,c4,2): (2,4),(3,4)
# c1(H,r1,c3,2): (1,3),(1,4)
# T-Rex(H,r2,c0,2): (2,0),(2,1)
# e1(egg,r0,c2): (0,2)
# Check all: no overlaps. All within 5x5.

# But wait: r2 at (2,3). c1 at (1,3). No overlap. r3 at (2,4). c1 at (1,4). No overlap.
# c1 going left 1 requires: we said r1 must move first. After r1 down 2, row1,col2 free. c1 left 1 = col2-3. OK.
# r2 going up: need row1,col3 free. c1 moved to col2-3, so (1,3) still has c1! r2 going up to row1,col3 - blocked by c1.
# Hmm. c1 moved left to col2-3: now (1,2),(1,3). col3,row1 still has c1. r2 at (2,3),(3,3) going up: needs row1,col3 free. But c1 is there after c1 left 1 = col2-3. Still blocked!
# c1 must move further: c1 left 2 = col1-2. (1,1),(1,2). row1,col3 free! But does col1,row1 have anything?
# Initial: nothing at (1,1). c1 left 2: (1,1),(1,2). row1,col2 has r1 initially, but r1 already moved to rows3-4. So (1,2) is free. OK!
# After c1 left 2: r2 up 1 = rows1-2. row2,col3 free. r3 down 1 = rows3-4. row2,col4 free. T exits.
# Moves: r1 down 2(1) + c1 left 2(1) + r2 up(1) + r3 down(1) + T(1) = 5.

# But is there a shorter path? Can we do in 4?
# We need col2,col3,col4 in row2 all clear. r1 clears col2 (needs 1 move). r2 clears col3 (needs 1 move). r3 clears col4 (needs 1 move). Plus T = 4 moves minimum IF all can move independently.
# r2 going up: row1,col3 has c1! Can't go up directly. r2 going down: row4,col3 free. r2 down 2 = rows4... wait r2 len=2 at rows2-3. Down 1=rows3-4. Row2,col3 free. But row3,col3 still has r2 bottom -> row4,col3 = r2 bottom. row4 in bounds(0-4).
# r2 down 1 = rows3-4. row2,col3 free. This doesn't need c1 to move!
# So: r1 down 2(1) + r2 down 1(1) + r3 down 1(1) + T(1) = 4 moves. BFS would find this. :(
# The e1 egg at row0,col2 blocks r1 from going up (up from rows1-2: row0,col2 has egg). But r1 can go down.
# So BFS = 4 for this layout. Not 5.

# Need to also block r2 from going down directly.
# e2(egg) at row4,col3: blocks r2 down (row4,col3 occupied). r2 can only go up (needs row1,col3 free).
# Initial: row1,col3 has c1. r2 can't go up. r2 STUCK.
# So c1 must move first: c1 left 2 (or right): c1(H,r1,c3,2) right: col4-5 OOB. left 1=col2-3 (row1,col2 has r1 initially). left 2: col1-2 (row1,col2 has r1). BLOCKED.
# r1 must move first: r1 down 2 -> then c1 left 2 -> then r2 up (row1,col3 free) -> r3 ...
# r3 at rows2-3,col4. r3 up: row1,col4 - c1 after left 2 is at col1-2, so row1,col4 free. r3 up 1=rows1-2. row2,col4 free. T exits.
# Moves: r1 down 2(1) + c1 left 2(1) + r2 up(1) + r3 up(1) + T(1) = 5.
# Shorter? r1 must go first (to allow c1 to move). c1 must go before r2. r3 independent.
# r3 up first (1): rows1-2, row2,col4 free. Then r1 down 2(1), c1 left 2(1), r2 up(1), T(1) = 5. Same.
# Can we skip c1? r2 blocked up by c1, blocked down by e2. r2 STUCK unless c1 moves. Can't skip c1.
# So minimum is 5.

r_lv9e = lv_candidate(5,5,2,[
    ('tx','t',2,0,2,'H'),
    ('r1','r',1,2,2,'V'),   # rows1-2,col2
    ('r2','r',2,3,2,'V'),   # rows2-3,col3
    ('r3','r',2,4,2,'V'),   # rows2-3,col4
    ('c1','c',1,3,2,'H'),   # row1,col3-4 - blocks r2 going up
    ('e1','e',0,2,1,'H'),   # egg row0,col2 - blocks r1 going up
    ('e2','e',4,3,1,'H'),   # egg row4,col3 - blocks r2 going down
])
print(f"  Lv9e (target 5): BFS={r_lv9e}")

# Lv10: 5x5, exitRow=2, par=6
# Extend: also block r3 going up (with c1 covering col4 too? c1 len=2 covers col3-4).
# Use b1(H,r1,c3,3): row1,col3-4-5? col5 OOB. b1(H,r1,c2,3): row1,col2-4. Blocks r1,r2,r3(if at col2-4) from going up.
# Wait r1 at col2,rows1-2: (1,2) has r1. b1 at row1,col2 overlaps (1,2)! Bad.
# b1(H,r0,c2,3): row0,col2-4. Blocks r1(col2), r2(col3), r3(col4) from going up.
# b1 must move left: col0-1(row0). col-1 OOB. left 0 = col2 still blocked. Can't free col2 going left.
# b1 right: col3-5. col5 OOB. Can't.
# b1 STUCK. Bad if blocking col2.
# b1(H,r0,c1,3): row0,col1-3. Blocks r2(col2? no, col2 not in col1-3)... col1,2,3. So blocks r1(col2) going up (row0,col2=b1). r3 at col4: row0,col4 free.
# b1 right 1=col2-4: row0,col1 free. col2,3,4 occupied.
# b1 right 2=col3-5: col5 OOB.
# b1 left 1=col0-2: col0 free,col1 free,col2 occupied. Still col2 blocked.
# b1 can't free col2.
# Conclusion: brontosaurus H in row0 can never free col2 in a 5-wide grid (its middle cell always covers col2 if it starts at col1-3).

# New strategy for 6 moves: use the 5-move design + 1 more blocker.
# From lv9e (5 moves): add c2(H,r3,c4,2) to block r3 going down.
# r3(V,r2,c4,2) rows2-3,col4. c2(H,r3,c4,2) row3,col4-5 - col5 OOB! Bad.
# c2(H,r3,c3,2) row3,col3-4: r3 down blocked (row3,col4 has c2). Also blocks r2 down? r2(V,r2,c3) row3,col3 has c2. r2 down 1=rows3-4: row3,col3 has c2. Blocked.
# With e2 at row4,col3 and c2 at row3,col3: r2 down blocked by c2 (row3,col3). r2 up blocked by c1 (row1,col3).
# r2 STUCK. Unless c2 can move or c1 can move.
# This creates a longer chain: to solve r2, need to clear above (c1) or below (c2).
# c2 left: col2-3. row3,col2 free (r1 moved away)? Initially r1 at rows1-2 so row3,col2 free. c2 left 1=col2-3. row3,col4 free.
# Then r3 down 1=rows3-4. row2,col4 free. And c2 moved to free row3,col3. r2 can now go down 1=rows3-4. row2,col3 free.
# Sequence: r1 down 2 + c1 left 2 + r2 down(or up after c1 moves - if c2 blocks down, r2 still needs up? c1 left 2 frees row1,col3. r2 up 1=rows1-2. row2,col3 free. c2 doesn't affect up direction.)
# With c2(H,r3,c3,2): r2(V,r2,c3) down 1=rows3-4: row3,col3 has c2. Blocked. r2 up: row1,col3 has c1 initially.
# After r1 down 2 + c1 left 2: row1,col3 free. r2 up 1=rows1-2. row2,col3 free. c2 irrelevant for this path.
# So: r1(1)+c1(1)+r2(1)+r3 down(1)+T(1)=5. c2 doesn't add a move!
# r3: (rows2-3,col4). r3 up: row1,col4 free (c1 now at col1-2 after left 2). r3 up 1=rows1-2. row2,col4 free. T exits.
# If c2(H,r1,c4,2) blocks r3 going up: c2 at row1,col4-5 OOB.
# c2(H,r1,c3,2) row1,col3-4: overlaps c1(H,r1,c3,2)! Can't have two H pieces at same row overlapping.

# Ugh. Let me just try various 5x5 designs and use BFS to find ones with the right par.
# I'll generate a bunch and report BFS results.

print("\n=== Batch testing 5x5 designs for par 5-6 ===")

# Design A: classic Rush Hour inspired
# Row:  0: .  .  c1 c1 .
#       1: .  .  r1 .  r2
#       2: T  T  r1 .  r2  -> exit
#       3: .  .  .  b1 b1 b1  <- b1 len3 OOB for col=3, col4=len3 would need col3-5 (col5 OOB)
# Let me try b1(H,r3,c2,3): row3,col2-4.
# r1(V,r1,c2): rows1-2. c1(H,r0,c2,2): row0,col2-3.
# r2(V,r1,c4): rows1-2.
# b1(H,r3,c2,3): row3,col2-4. Doesn't affect row2 directly.
# T blocked by r1(rows1-2,col2) and r2(rows1-2,col4)? T needs col2,col3,col4 clear in row2.
# r2 at row2,col4: blocks (2,4). r1 at row2,col2: blocks (2,2). col3 row2 free.
# r1 up: row0,col2 has c1. Blocked. r1 down: row3,col2 has b1. Blocked. r1 STUCK.
# Unless c1 or b1 moves.
# c1(H,r0,c2,2) right 1=col3-4. row0,col2 free. r1 up 1=rows0-1. row2,col2 free.
# r2 up: row0,col4 free (c1 moved to col3-4? col4,row0 has c1 right end!). r2 can't go up.
# r2 down: row3,col4 - b1 at col2-4, so row3,col4 has b1! Blocked.
# b1 right: col3-5 OOB. b1 left 1=col1-3. row3,col4 free. r2 down 1=rows2-3. Still at (2,4)! r2 down 2=rows3-4. Row3,col4 - b1 moved to col1-3, row3,col4 free. r2 down 2.  row2,col4 free. T exits.
# Sequence: c1 right(1) + b1 left(1) + r1 up(1) + r2 down 2(1) + T(1) = 5 moves.
# Shorter? Can we do 4?
# r1 up needs c1 to move. r2 down needs b1 to move. So c1 and b1 both must move = 2 extra moves. 2+2(r1,r2)+1(T)=5. Can't do less.
# BFS should give 5.

designs_5x5 = {
    'A': (5,5,2,[
        ('tx','t',2,0,2,'H'),
        ('r1','r',1,2,2,'V'),   # rows1-2,col2
        ('r2','r',1,4,2,'V'),   # rows1-2,col4
        ('c1','c',0,2,2,'H'),   # row0,col2-3
        ('b1','b',3,2,3,'H'),   # row3,col2-4
    ]),
    'B': (5,5,2,[  # from lv9e
        ('tx','t',2,0,2,'H'),
        ('r1','r',1,2,2,'V'),
        ('r2','r',2,3,2,'V'),
        ('r3','r',2,4,2,'V'),
        ('c1','c',1,3,2,'H'),
        ('e1','e',0,2,1,'H'),
        ('e2','e',4,3,1,'H'),
    ]),
    'C': (5,5,2,[  # 3 V blockers + 1 support
        ('tx','t',2,0,2,'H'),
        ('r1','r',1,2,2,'V'),
        ('r2','r',1,3,2,'V'),
        ('r3','r',1,4,2,'V'),
        ('c1','c',0,3,2,'H'),   # row0,col3-4 blocks r2,r3 going up
        ('e1','e',0,2,1,'H'),   # blocks r1 going up
    ]),
    'D': (5,5,2,[  # variation
        ('tx','t',2,0,2,'H'),
        ('r1','r',1,2,2,'V'),
        ('r2','r',1,3,2,'V'),
        ('c1','c',0,2,2,'H'),   # row0,col2-3
        ('c2','c',3,2,2,'H'),   # row3,col2-3 blocks r1,r2 going down
        ('e1','e',4,3,1,'H'),
    ]),
    'E_6moves': (5,5,2,[
        ('tx','t',2,0,2,'H'),
        ('r1','r',1,2,2,'V'),
        ('r2','r',1,3,2,'V'),
        ('r3','r',1,4,2,'V'),
        ('c1','c',0,2,2,'H'),   # row0,col2-3 blocks r1,r2
        ('e1','e',0,4,1,'H'),   # blocks r3 going up
        ('c2','c',3,3,2,'H'),   # row3,col3-4 blocks r2,r3 going down
    ]),
}

for name, (cols,rows,er,pieces) in designs_5x5.items():
    r = lv_candidate(cols,rows,er,pieces)
    print(f"  Design {name}: BFS={r}")
