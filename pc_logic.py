from collections import deque

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right by 1 tile

def in_plane(tile, size):
    """
    in_plane essentially returns True if both the row and column numbers are between 0 and the board's size limit.
    It will prevent my bfs from looking for paths outside the edges of the grid.
    """
    row, col = tile
    return 0 <= row < size and 0 <= col < size



def rebuild_path(came_from, end):
    """
    Rebuild the path from the start to the end using the came_from dictionary.
    The came_from dictionary is basically a map showing all where we came from.
    Starting at the end tile, the func steps backwards until it reaches the starting point. 
    I reverse so that the result can be a coherent path from x0 to xn rather than the reverse.
    """
    path = []
    tile = end
    while tile is not None:
        path.append(tile)
        tile = came_from[tile]
    path.reverse()
    return path



def get_shortest_path(start, target, walls, size=9):
    """
    First, we check if the target is one or group of tiles (e.g. an entire row), 
    converting it to a set so my bfs can easily check if it has hit a winning spot hhh.
    Using deque to check tiles in a breadth-first manner, 
    starting at the starting tile and explore all possible moves in the four cardinal directions.
    If it returns None, then we're simply boxed in.
    Power-ups are ignored in L1.
    """
    goals = {target} if isinstance(target, tuple) else set(target)
    # If goal's 1 tile (a tuple) -> set(target), else -> convert the whole bunch into a set.

    came_from = {start: None}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current in goals:
            return rebuild_path(came_from, current)

        for d_row, d_col in DIRECTIONS:
            nxt = (current[0] + d_row, current[1] + d_col)
            if in_plane(nxt, size) and nxt not in walls and nxt not in came_from:
                came_from[nxt] = current
                queue.append(nxt)
        # Deque basically works in waves. We add the 4 neighbors to the queue then we visit the first inside (FIFO) 
        # then we add its neighbors at the back of the queuetoo but go back and visit the second in the queue bfr we get to them.
    return None

def get_next_pc_move(current, target, walls, size=9, **options):
    """
    Returns the single tile the player should step to this turn.
    If None -> player is stuck and should surrender? or place a wall.
    If len(path) == 1 -> player is already on the goal yay.
    Otherwise, return the next tile in the path.
    """
    path = get_shortest_path(current, target, walls, size, **options)

    if path is None:
        return None
    if len(path) == 1:
        return current
    return path[1]