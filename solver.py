from collections import deque

def solve(level):
    """BFS solver. Returns (min_moves, solvable). """
    cols = level['cols']
    rows = level['rows']
    exit_row = level['exitRow']
    pieces = level['pieces']

    # Separate fixed eggs from movable pieces
    movable = [p for p in pieces if p['type'] != 'e']
    fixed = [p for p in pieces if p['type'] == 'e']

    # Build fixed occupancy set
    fixed_cells = set()
    for p in fixed:
        fixed_cells.add((p['row'], p['col']))

    # Initial state: tuple of (id, row, col) sorted by id
    def make_state(mpieces):
        return tuple(sorted((p['id'], p['row'], p['col']) for p in mpieces))

    def is_win(state):
        for pid, r, c in state:
            if pid == 'tx':
                # Find tx len (always 2)
                return c + 2 > cols
        return False

    def get_piece_info(pid):
        for p in movable:
            if p['id'] == pid:
                return p
        return None

    # Build lookup: id -> (type, dir, len)
    piece_info = {}
    for p in movable:
        piece_info[p['id']] = (p['type'], p['dir'], p['len'])

    def get_occupancy(state):
        occ = set(fixed_cells)
        for pid, r, c in state:
            ptype, pdir, plen = piece_info[pid]
            for i in range(plen):
                if pdir == 'H':
                    occ.add((r, c + i))
                else:
                    occ.add((r + i, c))
        return occ

    def get_moves(state):
        """Generate all possible next states."""
        # Build dict for quick lookup
        state_dict = {pid: (r, c) for pid, r, c in state}

        for pid, r, c in state:
            ptype, pdir, plen = piece_info[pid]

            # Build occupancy excluding this piece
            occ = set(fixed_cells)
            for pid2, r2, c2 in state:
                if pid2 == pid:
                    continue
                pt2, pd2, pl2 = piece_info[pid2]
                for i in range(pl2):
                    if pd2 == 'H':
                        occ.add((r2, c2 + i))
                    else:
                        occ.add((r2 + i, c2))

            if pdir == 'H':
                # Move left
                steps = 0
                nc = c - 1
                while nc >= 0 and (r, nc) not in occ:
                    steps += 1
                    new_state = tuple(sorted(
                        (pid2, r2, c2) if pid2 != pid else (pid, r, c - steps)
                        for pid2, r2, c2 in state
                    ))
                    yield new_state
                    nc -= 1

                # Move right
                steps = 0
                nc = c + plen
                while True:
                    if ptype == 't':
                        # T-Rex can exit
                        if nc > cols:
                            break
                        if nc == cols:
                            # Exit move - win state
                            steps += 1
                            new_state = tuple(sorted(
                                (pid2, r2, c2) if pid2 != pid else (pid, r, c + steps)
                                for pid2, r2, c2 in state
                            ))
                            yield new_state
                            break
                        if (r, nc) in occ:
                            break
                        steps += 1
                        new_state = tuple(sorted(
                            (pid2, r2, c2) if pid2 != pid else (pid, r, c + steps)
                            for pid2, r2, c2 in state
                        ))
                        yield new_state
                        nc += 1
                    else:
                        if nc >= cols or (r, nc) in occ:
                            break
                        steps += 1
                        new_state = tuple(sorted(
                            (pid2, r2, c2) if pid2 != pid else (pid, r, c + steps)
                            for pid2, r2, c2 in state
                        ))
                        yield new_state
                        nc += 1
            else:  # V
                # Move up
                steps = 0
                nr = r - 1
                while nr >= 0 and (nr, c) not in occ:
                    steps += 1
                    new_state = tuple(sorted(
                        (pid2, r2, c2) if pid2 != pid else (pid, r - steps, c)
                        for pid2, r2, c2 in state
                    ))
                    yield new_state
                    nr -= 1

                # Move down
                steps = 0
                nr = r + plen
                while nr < rows and (nr, c) not in occ:
                    steps += 1
                    new_state = tuple(sorted(
                        (pid2, r2, c2) if pid2 != pid else (pid, r + steps, c)
                        for pid2, r2, c2 in state
                    ))
                    yield new_state
                    nr += 1

    init_state = make_state(movable)

    if is_win(init_state):
        return 0

    visited = {init_state: 0}
    queue = deque([(init_state, 0)])

    while queue:
        state, dist = queue.popleft()

        if dist > 20:  # Safety limit
            continue

        for next_state in get_moves(state):
            if is_win(next_state):
                return dist + 1
            if next_state not in visited:
                visited[next_state] = dist + 1
                queue.append((next_state, dist + 1))

    return -1


def verify_level(level):
    result = solve(level)
    return result


# ── Level definitions ──

def make_piece(pid, ptype, row, col, length, direction):
    type_map = {
        't': ('🦖', '小暴龍', 'pt'),
        'b': ('🦕', '長頸龍', 'pb'),
        'c': ('🐊', '三角龍', 'pc'),
        'r': ('🦎', '迅猛龍', 'pr'),
        'e': ('🥚', '恐龍蛋', 'pe'),
    }
    em, nm, cs = type_map[ptype]
    return {
        'id': pid, 'type': ptype, 'row': row, 'col': col,
        'len': length, 'dir': direction,
        'em': em, 'nm': nm, 'cs': cs
    }


# Existing levels 1-6 (kept as-is from the game)
LEVELS = [
    # Lv1
    {'cols':4,'rows':4,'exitRow':1,'par':2,'name':'小試身手','icon':'🥚',
     'pieces':[
        make_piece('tx','t',1,0,2,'H'),
        make_piece('b1','b',0,2,2,'V'),
        make_piece('e1','e',3,3,1,'H'),
     ]},
    # Lv2
    {'cols':4,'rows':4,'exitRow':1,'par':3,'name':'暖身一下','icon':'🦎',
     'pieces':[
        make_piece('tx','t',1,0,2,'H'),
        make_piece('b1','b',0,2,2,'V'),
        make_piece('c1','c',2,2,2,'H'),
        make_piece('e1','e',3,0,1,'H'),
     ]},
    # Lv3
    {'cols':5,'rows':5,'exitRow':2,'par':3,'name':'加油前進','icon':'🦕',
     'pieces':[
        make_piece('tx','t',2,0,2,'H'),
        make_piece('r1','r',2,2,2,'V'),
        make_piece('c1','c',0,2,2,'H'),
        make_piece('e1','e',4,2,1,'H'),
     ]},
    # Lv4
    {'cols':5,'rows':5,'exitRow':1,'par':4,'name':'勇敢挑戰','icon':'🐊',
     'pieces':[
        make_piece('tx','t',1,0,2,'H'),
        make_piece('r1','r',0,2,2,'V'),
        make_piece('c1','c',2,1,2,'H'),
        make_piece('r2','r',2,3,2,'V'),
        make_piece('e1','e',2,0,1,'H'),
     ]},
    # Lv5
    {'cols':5,'rows':5,'exitRow':2,'par':5,'name':'超級高手','icon':'🦖',
     'pieces':[
        make_piece('tx','t',2,0,2,'H'),
        make_piece('r1','r',1,2,2,'V'),
        make_piece('c1','c',0,1,2,'H'),
        make_piece('r2','r',0,3,2,'V'),
        make_piece('r3','r',0,4,2,'V'),
        make_piece('e1','e',0,0,1,'H'),
        make_piece('e2','e',3,2,1,'H'),
     ]},
    # Lv6
    {'cols':6,'rows':6,'exitRow':2,'par':6,'name':'恐龍勇士','icon':'⭐',
     'pieces':[
        make_piece('tx','t',2,0,2,'H'),
        make_piece('r1','r',1,2,2,'V'),
        make_piece('c1','c',0,1,2,'H'),
        make_piece('r2','r',0,3,2,'V'),
        make_piece('r3','r',0,4,2,'V'),
        make_piece('r4','r',2,5,2,'V'),
        make_piece('e1','e',0,0,1,'H'),
        make_piece('e2','e',3,2,1,'H'),
     ]},
]

# Verify levels 1-6
print("=== Verifying existing levels 1-6 ===")
for i, lv in enumerate(LEVELS):
    result = verify_level(lv)
    print(f"  Lv{i+1} ({lv['cols']}x{lv['rows']}, exitRow={lv['exitRow']}, par={lv['par']}): BFS={result} {'OK' if result > 0 else 'FAIL'}")
