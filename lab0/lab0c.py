from collections import deque

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up

def reachable_rooms(grid: list[str], s: tuple[int, int]) -> list[tuple[int, int]]:
    # 1st step: convert bordered map size into num of rooms
    num_rows = (len(grid) - 1) // 2
    num_cols = (len(grid[0]) - 1) // 2

    start_row, start_col = s
    if not (0 <= start_row < num_rows and 0 <= start_col < num_cols):
        return []

    # base case: Stanley should spawn in a room
    if grid[2 * start_row + 1][2 * start_col + 1] != ' ':
        return []

    reachable = set([s])
    queue = deque([((start_row, start_col), '')])  # (room, last door color)
    visited = set([((start_row, start_col), '')])

    while len(queue) > 0:
        (room_row, room_col), last_door = queue.popleft()
        map_row, map_col = 2 * room_row + 1, 2 * room_col + 1 # room coords -> map indices

        for d_row, d_col in dirs:
            next_room_row, next_room_col = room_row + d_row, room_col + d_col
            if not (0 <= next_room_row < num_rows and 0 <= next_room_col < num_cols):
                continue

            door_cell = grid[map_row + d_row][map_col + d_col]

            if door_cell == '#': # pader
                continue
            if door_cell in ('R', 'B'):
                if door_cell == last_door:
                    continue
                new_last_door = door_cell
            elif door_cell == '.': # wala
                new_last_door = last_door
            else:
                continue # any other char

            next_map_row, next_map_col = 2 * next_room_row + 1, 2 * next_room_col + 1
            if grid[next_map_row][next_map_col] != ' ':
                continue

            new_state = ((next_room_row, next_room_col), new_last_door)
            if new_state not in visited:
                visited.add(new_state)
                queue.append(new_state)
                reachable.add((next_room_row, next_room_col))

    return sorted(reachable)