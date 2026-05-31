"""
Optimized BFS solver using integer state encoding.
"""
from collections import deque

def solve_fast(level):
    cols = level['cols']
    rows = level['rows']
    pieces = level['pieces']

    movable = [p for p in pieces if p['type'] != 'e']
    fixed_cells = frozenset((p['row'], p['col']) for p in pieces if p['type'] == 'e')

    # Sort movable pieces by id for consistent state encoding
    movable_sorted = sorted(movable, key=lambda p: p['id'])
    n = len(movable_sorted)

    # Find T-Rex index
    tx_idx = next(i for i, p in enumerate(movable_sorted) if p['id'] == 'tx')
    tx_len = movable_sorted[tx_idx]['len']  # always 2

    # Encode piece info
    piece_dirs = [p['dir'] for p in movable_sorted]
    piece_lens = [p['len'] for p in movable_sorted]
    piece_types = [p['type'] for p in movable_sorted]

    # Initial state: tuple of (row, col) for each movable piece in sorted order
    init_state = tuple((p['row'], p['col']) for p in movable_sorted)

    def is_win(state):
        r, c = state[tx_idx]
        return c + tx_len > cols

    def get_moves(state):
        # Build occupancy grid
        grid = [bytearray(cols) for _ in range(rows)]
        for r, c in fixed_cells:
            grid[r][c] = 1
        for idx, (r, c) in enumerate(state):
            l = piece_lens[idx]
            d = piece_dirs[idx]
            if d == 'H':
                for i in range(l): grid[r][c+i] = 1
            else:
                for i in range(l): grid[r+i][c] = 1

        results = []
        for idx, (r, c) in enumerate(state):
            l = piece_lens[idx]
            d = piece_dirs[idx]
            ptype = piece_types[idx]

            # Unmark this piece
            if d == 'H':
                for i in range(l): grid[r][c+i] = 0
            else:
                for i in range(l): grid[r+i][c] = 0

            if d == 'H':
                # Left
                nc = c - 1
                steps = 0
                while nc >= 0 and not grid[r][nc]:
                    steps += 1
                    new_state = state[:idx] + ((r, c-steps),) + state[idx+1:]
                    results.append(new_state)
                    nc -= 1
                # Right
                nc = c + l
                steps = 0
                if ptype == 't':
                    # T-Rex can exit
                    while nc < cols and not grid[r][nc]:
                        steps += 1
                        new_state = state[:idx] + ((r, c+steps),) + state[idx+1:]
                        results.append(new_state)
                        nc += 1
                    # Exit move
                    if nc >= cols or not grid[r][nc]:
                        # Actually just check: can T-Rex exit?
                        # T exits if it can slide to col where c+l > cols
                        # The exit cell is beyond cols, so we just check if path is clear up to cols-1
                        can_exit_steps = steps + 1  # one more step exits
                        new_state = state[:idx] + ((r, c+can_exit_steps),) + state[idx+1:]
                        results.append(new_state)
                else:
                    while nc < cols and not grid[r][nc]:
                        steps += 1
                        new_state = state[:idx] + ((r, c+steps),) + state[idx+1:]
                        results.append(new_state)
                        nc += 1
            else:  # V
                # Up
                nr = r - 1
                steps = 0
                while nr >= 0 and not grid[nr][c]:
                    steps += 1
                    new_state = state[:idx] + ((r-steps, c),) + state[idx+1:]
                    results.append(new_state)
                    nr -= 1
                # Down
                nr = r + l
                steps = 0
                while nr < rows and not grid[nr][c]:
                    steps += 1
                    new_state = state[:idx] + ((r+steps, c),) + state[idx+1:]
                    results.append(new_state)
                    nr += 1

            # Re-mark
            if d == 'H':
                for i in range(l): grid[r][c+i] = 1
            else:
                for i in range(l): grid[r+i][c] = 1

        return results

    if is_win(init_state):
        return 0

    visited = {init_state}
    queue = deque([(init_state, 0)])

    while queue:
        state, dist = queue.popleft()
        if dist >= 20:
            continue

        for next_state in get_moves(state):
            if is_win(next_state):
                return dist + 1
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, dist + 1))

    return -1


def make_piece(pid, ptype, row, col, length, direction):
    type_map = {
        't': ('🦖', '小暴龍', 'pt'),
        'b': ('🦕', '長頸龍', 'pb'),
        'c': ('🐊', '三角龍', 'pc'),
        'r': ('🦎', '迅猛龍', 'pr'),
        'e': ('🥚', '恐龍蛋', 'pe'),
    }
    em, nm, cs = type_map[ptype]
    return {'id': pid, 'type': ptype, 'row': row, 'col': col,
            'len': length, 'dir': direction, 'em': em, 'nm': nm, 'cs': cs}


def solve(level):
    return solve_fast(level)


# Original levels for import compatibility
LEVELS = [
    {'cols':4,'rows':4,'exitRow':1,'par':2,'name':'小試身手','icon':'🥚','pieces':[
        make_piece('tx','t',1,0,2,'H'), make_piece('b1','b',0,2,2,'V'), make_piece('e1','e',3,3,1,'H')]},
    {'cols':4,'rows':4,'exitRow':1,'par':3,'name':'暖身一下','icon':'🦎','pieces':[
        make_piece('tx','t',1,0,2,'H'), make_piece('b1','b',0,2,2,'V'), make_piece('c1','c',2,2,2,'H'), make_piece('e1','e',3,0,1,'H')]},
    {'cols':5,'rows':5,'exitRow':2,'par':3,'name':'加油前進','icon':'🦕','pieces':[
        make_piece('tx','t',2,0,2,'H'), make_piece('r1','r',2,2,2,'V'), make_piece('c1','c',0,2,2,'H'), make_piece('e1','e',4,2,1,'H')]},
    {'cols':5,'rows':5,'exitRow':1,'par':4,'name':'勇敢挑戰','icon':'🐊','pieces':[
        make_piece('tx','t',1,0,2,'H'), make_piece('r1','r',0,2,2,'V'), make_piece('c1','c',2,1,2,'H'), make_piece('r2','r',2,3,2,'V'), make_piece('e1','e',2,0,1,'H')]},
    {'cols':5,'rows':5,'exitRow':2,'par':5,'name':'超級高手','icon':'🦖','pieces':[
        make_piece('tx','t',2,0,2,'H'), make_piece('r1','r',1,2,2,'V'), make_piece('c1','c',0,1,2,'H'), make_piece('r2','r',0,3,2,'V'), make_piece('r3','r',0,4,2,'V'), make_piece('e1','e',0,0,1,'H'), make_piece('e2','e',3,2,1,'H')]},
    {'cols':6,'rows':6,'exitRow':2,'par':6,'name':'恐龍勇士','icon':'⭐','pieces':[
        make_piece('tx','t',2,0,2,'H'), make_piece('r1','r',1,2,2,'V'), make_piece('c1','c',0,1,2,'H'), make_piece('r2','r',0,3,2,'V'), make_piece('r3','r',0,4,2,'V'), make_piece('r4','r',2,5,2,'V'), make_piece('e1','e',0,0,1,'H'), make_piece('e2','e',3,2,1,'H')]},
]


if __name__ == '__main__':
    print("Testing solver speed...")
    import time
    t0 = time.time()
    for _ in range(5):
        for lv in LEVELS:
            r = solve_fast(lv)
    elapsed = time.time() - t0
    print(f"  6 levels x 5 = 30 solves in {elapsed:.3f}s")
    for i, lv in enumerate(LEVELS):
        print(f"  Lv{i+1}: BFS={solve_fast(lv)}")
