# Divide & Conquer 😄

1. **Core BFS:** `get_shortest_path(start, target, walls, ...)`
   - Grid navigation on an N×N board (9, 11, or 13), moving in 4 directions and blocked by walls and board edges.
   - Return the full list of coordinates, not just the length, so the Survey display can draw the path.
   - Ignore pickups (power-ups) as obstacles, so they can be stepped over (Level 1), and ignore Echoes entirely.
   - Return `None` if no path exists. This is also what the game can use to reject illegal wall placements that fully block a player.

2. **Next-move wrapper:** `get_next_enemy_move(current, target, walls)`
   - Call the BFS and return only the first step of the path, which main uses to move the enemy.
   - Handle "already at the goal" and "no path" cases safely.

3. **Phase Step support (Level 2)**
   - Add `has_phase_step` and `walls_passed` to the BFS. The path may cross exactly one wall tile, and the flag is toggled off after that tile is used.
   - Exclude the Glyph Door from this, since Phase Step doesn't work on it.

4. **Opportunist behavior (Level 2)**
   - Compare the path length of "go straight to the goal" against "detour to the Phase Step pickup, then go to the goal".
   - If the detour is acceptable and the pickup is still there, set the pickup as the temporary target. Once it's collected, set `has_phase_step = True` for the enemy.

5. **Patrol walls:** `update_patrol_walls(patrol_state, player_walls)` (Level 2)
   - Move each 2-square patrol wall one step along its track per round.
   - If the next step is blocked by a player wall, don't move and increment that wall's stall counter. Reset the counter when it moves again.
   - At a stall count of 2, spawn the Anchor shard and return it so the display code can draw it.

6. **Collapse-aware routing (Level 3), Survivalist behavior**
   - Pass `turn_counter` into the BFS.
   - If the round ends in 4 or 9 (collapse next turn), temporarily treat the outer ring as `#` walls so the enemy routes inward.
   - Make the ring depth grow with each collapse (rounds 5, 10, 15), since the board shrinks 13 → 11 → 9 → 7, and stop collapsing after the 7×7 remains.
   - Use a temporary copy of the wall set so the real board data isn't modified.

7. **Target switching**
   - Make the target a parameter: the goal row for Levels 1–2, and `lockdown_node` (the true exit/Keystone) for Level 3, since the original goal edge collapses at round 5.

8. **Level 3 extras (if the AI needs them)**
   - Account for decaying walls (remove walls older than 8 rounds before pathing).
   - Overclock lets the enemy take 2 steps, so call the move function twice with the board updated in between.
   - After round 20 (Sudden Death), skip any wall-placement logic.

9. **Testing**
   - Unit-test each function on small hand-made grids: open board, fully blocked board, a single wall crossed with Phase Step, patrol stall at 1 vs 2 rounds, and collapse routing at rounds 4, 9, and 14.