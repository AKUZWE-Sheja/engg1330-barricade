from pc_logic import (
    get_shortest_path,
    get_next_pc_move,
    update_patrol_walls,
    get_collapsed_tiles,
    get_active_walls,
    path_length,
    decide_pc_target,
    get_overclock_moves,
    should_use_overclock,
    is_wall_placement_legal,
    choose_wall,
)

def run_tests():
    # 1. Open board
    path = get_shortest_path((0, 0), (0, 4), set(), size=5)
    assert path[0] == (0, 0) and path[-1] == (0, 4) and len(path) == 5

    # 2. Blocked path vs Phase Step
    wall_row = {(1, c) for c in range(5)}
    assert get_shortest_path((0, 0), (2, 0), wall_row, size=5) is None
    phase_path = get_shortest_path((0, 0), (2, 0), wall_row, size=5, has_phase_step=True)
    assert len(phase_path) == 3

    # 3. Glyph Door overrides Phase Step
    assert get_shortest_path(
        (0, 0), (2, 0), wall_row, size=5, has_phase_step=True, door_tiles=wall_row
    ) is None

    # 4. Patrol Wall: stall round 1 -> crystallize round 2
    patrols = [{"tiles": [(2, 2), (2, 3)], "direction": (1, 0), "stall": 0}]
    assert update_patrol_walls(patrols, {(3, 2)}, size=5) is None
    assert update_patrol_walls(patrols, {(3, 2)}, size=5) == (2, 2)
    assert len(patrols) == 0  # wall shattered and removed

    # 5. Ring collapse timing (13x13)
    assert get_collapsed_tiles(13, turn_counter=3) == set()
    assert (0, 0) in get_collapsed_tiles(13, turn_counter=4) and (1, 1) not in get_collapsed_tiles(13, turn_counter=4)
    assert (1, 1) in get_collapsed_tiles(13, turn_counter=9) and (2, 2) not in get_collapsed_tiles(13, turn_counter=9)
    assert (2, 2) in get_collapsed_tiles(13, turn_counter=14) and (3, 3) not in get_collapsed_tiles(13, turn_counter=14)

    # 6. Collapse avoidance & goal priority (passes avoid_tiles, NOT turn_counter)
    danger = get_collapsed_tiles(13, turn_counter=4)
    path = get_shortest_path((6, 6), (0, 6), set(), size=13, avoid_tiles=danger)
    assert path[-1] == (0, 6)
    # The intermediate path stays off outer ring (0, c) except the goal (0, 6)
    assert all(r != 0 for r, c in path[:-1])

    # 7. Fallback when boxed by collapse
    # FIXED: Added a physical wall at (1,0). Without this, the AI wasn't boxed, 
    # it would just walk to (1,0) to avoid (0,1). Now it is forced to test the fallback.
    trapped_pos = (0, 0)
    move = get_next_pc_move(trapped_pos, (0, 2), walls={(1, 0)}, size=5, avoid_tiles={(0, 1)})
    assert move == (0, 1)  # took danger tile rather than freezing

    # 8. Decaying walls lifetime (8 turns)
    assert get_active_walls({(1, 1): 3}, turn_counter=10) == {(1, 1)}
    assert get_active_walls({(1, 1): 3}, turn_counter=11) == set()

    # 9. Overclock mechanics
    p1_path = [(0, 0), (0, 1), (0, 2)]
    pc_path = [(4, 0), (4, 1), (4, 2), (4, 3)]
    assert should_use_overclock(pc_path, p1_path) is True  # behind -> burn it
    moves = get_overclock_moves((0, 0), (0, 4), set(), size=5)
    assert moves == [(0, 1), (0, 2)]

    # 10. Wall legality & fair play
    # FIXED: The original test started the player with walls at (0,1) and (1,0), 
    # meaning the player at (0,0) was ALREADY trapped before the test even ran.
    starting_walls = {(0, 1)} 
    assert is_wall_placement_legal((2, 2), starting_walls, (0, 0), (4, 4), (0, 4), (4, 0), size=5) is True
    assert is_wall_placement_legal((1, 0), starting_walls, (0, 0), (4, 4), (0, 4), (4, 0), size=5) is False

    # 11. Offensive wall selection
    # FIXED: Depending on deque execution order, BFS might prefer routing through (0,1) or (1,0) equally.
    chosen = choose_wall((0, 0), (4, 4), (2, 0), (0, 4), set(), size=5, min_gain=1)
    assert chosen in [(1, 0), (0, 1)]

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()