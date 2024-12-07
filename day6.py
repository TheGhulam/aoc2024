def parse_input(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def find_guard(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '^':
                return (x, y, '^')
    return None

def get_next_position(x, y, direction):
    if direction == '^':
        return (x, y - 1)
    elif direction == '>':
        return (x + 1, y)
    elif direction == 'v':
        return (x, y + 1)
    elif direction == '<':
        return (x - 1, y)

def turn_right(direction):
    directions = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
    return directions[direction]

def is_within_grid(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def part1(filename):
    grid = parse_input(filename)
    
    start = find_guard(grid)
    if not start:
        return 0
        
    x, y, direction = start
    visited = {(x, y)}  # Set to track visited positions
    
    while True:
        next_x, next_y = get_next_position(x, y, direction)
        
        if not is_within_grid(next_x, next_y, grid):
            break
            
        if grid[next_y][next_x] == '#':
            direction = turn_right(direction)
        else:
            x, y = next_x, next_y
            visited.add((x, y))
    
    return len(visited)

def simulate_guard_movement(grid, start_x, start_y, start_dir):
    x, y = start_x, start_y
    direction = start_dir
    visited_states = set()  # Track (position, direction) states
    path = []  # Track the path for loop detection
    
    while True:
        current_state = (x, y, direction)
        
        # If we've seen this state before, we're in a loop
        if current_state in visited_states:
            return True  # Loop detected
            
        visited_states.add(current_state)
        path.append(current_state)
        
        next_x, next_y = get_next_position(x, y, direction)
        
        if not is_within_grid(next_x, next_y, grid):
            return False  # No loop
            
        if grid[next_y][next_x] == '#':
            direction = turn_right(direction)
        else:
            x, y = next_x, next_y

def part2(filename):
    grid = parse_input(filename)
    
    guard_pos = find_guard(grid)
    if not guard_pos:
        return 0
        
    start_x, start_y, start_dir = guard_pos
    valid_positions = []
    
    # Try each empty position
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # Skip positions that are not empty or guard's starting position
            if grid[y][x] != '.' or (x == start_x and y == start_y):
                continue
                
            # Create a copy of the grid with new obstruction
            test_grid = [row[:] for row in grid]
            test_grid[y][x] = '#'
            
            # Simulate guard movement
            if simulate_guard_movement(test_grid, start_x, start_y, start_dir):
                valid_positions.append((x, y))
    
    return len(valid_positions)

result = part1('inputs/day06.txt')
print(f"The guard will visit {result} distinct positions.")

result = part2('inputs/day06.txt')
print(f"There are {result} valid positions to place the obstruction.")