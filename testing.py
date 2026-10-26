from draft import get_shortest_path, get_next_enemy_move

# Placeholder for Person 1's get_collapsed_tiles: just hardcode the outer ring
def fake_collapsed_tiles(size, turn):
    return {(r, c) for r in range(size) for c in range(size)
            if min(r, c, size - 1 - r, size - 1 - c) < 1}

path = get_shortest_path((6, 6), (0, 6), set(), 13,
                         avoid_tiles=fake_collapsed_tiles(13, 4))
assert (0, 5) not in path