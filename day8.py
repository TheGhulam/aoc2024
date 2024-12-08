def read_input(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def find_antennas(grid):
    # Find positions of all antennas grouped by frequency
    antennas = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != '.':
                freq = grid[y][x]
                if freq not in antennas:
                    antennas[freq] = []
                antennas[freq].append((x, y))
    return antennas

def is_valid_antinode(x1, y1, x2, y2, check_x, check_y):
    # Calculate distances from the check point to both antennas
    dist1 = ((check_x - x1) ** 2 + (check_y - y1) ** 2) ** 0.5
    dist2 = ((check_x - x2) ** 2 + (check_y - y2) ** 2) ** 0.5
    
    # Check if one distance is twice the other (in either direction)
    # Use floating point comparison with small epsilon for rounding errors
    epsilon = 1e-10
    return abs(dist1 - 2 * dist2) < epsilon or abs(dist2 - 2 * dist1) < epsilon

def find_antinodes(antenna_positions, grid_width, grid_height):
    antinodes = set()
    
    # For each pair of antennas
    for i, (x1, y1) in enumerate(antenna_positions):
        for j, (x2, y2) in enumerate(antenna_positions):
            if i >= j:  # Skip duplicate pairs and self-pairs
                continue
            
            # Check every point in the grid
            for check_y in range(grid_height):
                for check_x in range(grid_width):
                    if is_valid_antinode(x1, y1, x2, y2, check_x, check_y):
                        # Verify the point is collinear with the antennas
                        # Using cross product = 0 for collinearity
                        vec1_x = x2 - x1
                        vec1_y = y2 - y1
                        vec2_x = check_x - x1
                        vec2_y = check_y - y1
                        cross_product = vec1_x * vec2_y - vec1_y * vec2_x
                        
                        if abs(cross_product) < 1e-10:  # Account for floating point errors
                            antinodes.add((check_x, check_y))
    
    return antinodes

def part1(grid):
    height = len(grid)
    width = len(grid[0])
    
    # Get all antennas grouped by frequency
    antennas = find_antennas(grid)
    
    # Find all antinodes for each frequency
    all_antinodes = set()
    for freq, positions in antennas.items():
        if len(positions) >= 2:  # Need at least 2 antennas of same frequency
            antinodes = find_antinodes(positions, width, height)
            all_antinodes.update(antinodes)
    
    return len(all_antinodes)

def is_collinear(x1, y1, x2, y2, x3, y3):
    # Calculate the area of the triangle formed by three points
    # If area is 0, points are collinear
    area = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
    return area == 0

def find_antinodes_2(antenna_positions, grid_width, grid_height):
    antinodes = set()
    
    # For each pair of antennas
    for i, (x1, y1) in enumerate(antenna_positions):
        for j, (x2, y2) in enumerate(antenna_positions):
            if i >= j:  # Skip duplicate pairs and self-pairs
                continue
            
            # Always add antenna positions themselves as antinodes
            # (since they're collinear with at least two antennas)
            antinodes.add((x1, y1))
            antinodes.add((x2, y2))
            
            # Check every point in the grid
            for check_y in range(grid_height):
                for check_x in range(grid_width):
                    if is_collinear(x1, y1, x2, y2, check_x, check_y):
                        antinodes.add((check_x, check_y))
    
    return antinodes

def part2(grid):
    height = len(grid)
    width = len(grid[0])
    
    # Get all antennas grouped by frequency
    antennas = find_antennas(grid)
    
    # Find all antinodes for each frequency
    all_antinodes = set()
    for freq, positions in antennas.items():
        if len(positions) >= 2:  # Need at least 2 antennas of same frequency
            antinodes = find_antinodes_2(positions, width, height)
            all_antinodes.update(antinodes)
    
    return len(all_antinodes)

grid = read_input('inputs/day08.txt')
print(part1(grid),  part2(grid))
