def parse_disk_map(disk_map):
    """
    Parse the disk map string into a list of files and free spaces.
    Returns two lists:
    1. file_lengths: list of integers representing file lengths
    2. free_lengths: list of integers representing free space lengths
    """
    # Convert string to list of integers
    numbers = [int(x) for x in disk_map]
    
    # Separate into files (even indices) and free spaces (odd indices)
    file_lengths = numbers[::2]  # Every even index (0, 2, 4, ...)
    free_lengths = numbers[1::2]  # Every odd index (1, 3, 5, ...)
    
    return file_lengths, free_lengths

def create_block_representation(file_lengths, free_lengths):
    """
    Create a list representing individual blocks on the disk.
    Each block contains either a file ID (integer) or None for free space.
    """
    blocks = []
    current_position = 0
    file_id = 0
    
    # Alternate between adding file blocks and free space
    for file_len, free_len in zip(file_lengths, free_lengths):
        # Add file blocks
        for _ in range(file_len):
            blocks.append(file_id)
        current_position += file_len
        file_id += 1
        
        # Add free space blocks
        for _ in range(free_len):
            blocks.append(None)
        current_position += free_len
    
    # Handle the last file if present (when number of files > number of free spaces)
    if len(file_lengths) > len(free_lengths):
        for _ in range(file_lengths[-1]):
            blocks.append(file_id)
    
    return blocks

def compact_disk(blocks):
    """
    Simulate the process of moving file blocks to fill gaps.
    Returns a new list representing the compacted disk.
    """
    # Work with a copy to avoid modifying the original
    compacted = blocks.copy()
    
    # Continue until no more moves are possible
    while True:
        move_made = False
        
        # Find rightmost file block
        rightmost_file_idx = len(compacted) - 1
        while rightmost_file_idx >= 0 and compacted[rightmost_file_idx] is None:
            rightmost_file_idx -= 1
            
        if rightmost_file_idx < 0:
            break
            
        # Find leftmost free space
        leftmost_space_idx = 0
        while leftmost_space_idx < len(compacted) and compacted[leftmost_space_idx] is not None:
            leftmost_space_idx += 1
            
        if leftmost_space_idx >= rightmost_file_idx:
            break
            
        # Move the file block
        compacted[leftmost_space_idx] = compacted[rightmost_file_idx]
        compacted[rightmost_file_idx] = None
        move_made = True
        
        if not move_made:
            break
    
    return compacted

def calculate_checksum(blocks):
    """
    Calculate the filesystem checksum based on block positions and file IDs.
    """
    checksum = 0
    for position, file_id in enumerate(blocks):
        if file_id is not None:  # Skip free space blocks
            checksum += position * file_id
    return checksum

def part1(input_file):
    with open(input_file, 'r') as f:
        disk_map = f.read().strip()
    
    file_lengths, free_lengths = parse_disk_map(disk_map)
    initial_blocks = create_block_representation(file_lengths, free_lengths)
    final_blocks = compact_disk(initial_blocks)
    
    return calculate_checksum(final_blocks)

def find_file_spans(blocks):
    """
    Find the start position and length of each file in the blocks.
    Returns a dictionary mapping file IDs to tuples of (start_position, length).
    """
    file_spans = {}
    current_file = None
    start_pos = 0
    length = 0
    
    for pos, block in enumerate(blocks):
        if block != current_file:
            # Save the previous file's information if we found one
            if current_file is not None and current_file != None:
                file_spans[current_file] = (start_pos, length)
            # Start tracking new file
            current_file = block
            start_pos = pos
            length = 1
        else:
            length += 1
    
    # Don't forget to save the last file's information
    if current_file is not None and current_file != None:
        file_spans[current_file] = (start_pos, length)
    
    return file_spans

def find_free_spaces(blocks):
    """
    Find all continuous spans of free space.
    Returns a list of tuples (start_position, length).
    """
    free_spans = []
    current_length = 0
    start_pos = None
    
    for pos, block in enumerate(blocks):
        if block is None:
            if start_pos is None:
                start_pos = pos
            current_length += 1
        else:
            if current_length > 0:
                free_spans.append((start_pos, current_length))
                start_pos = None
                current_length = 0
    
    # Don't forget to add the last span if it ends with free space
    if current_length > 0:
        free_spans.append((start_pos, current_length))
    
    return free_spans

def compact_disk_whole_files(blocks):
    """
    Simulate the process of moving whole files to fill gaps, working from highest
    to lowest file ID. Each file only moves once if possible.
    Returns a new list representing the compacted disk.
    """
    compacted = blocks.copy()
    file_spans = find_file_spans(compacted)
    
    # Process files in order of decreasing file ID
    for file_id in sorted(file_spans.keys(), reverse=True):
        file_start, file_length = file_spans[file_id]
        
        # Find all free spaces before this file
        free_spans = [(start, length) for start, length in find_free_spaces(compacted)
                     if start < file_start]
        
        # Find the leftmost free space that can fit this file
        target_space = None
        for start, length in free_spans:
            if length >= file_length:
                target_space = start
                break
        
        # If we found a suitable space, move the file
        if target_space is not None:
            # Copy the file to its new location
            for i in range(file_length):
                compacted[target_space + i] = file_id
            
            # Clear the old location
            for i in range(file_start, file_start + file_length):
                compacted[i] = None
    
    return compacted

def part2(input_file):
    with open(input_file, 'r') as f:
        disk_map = f.read().strip()
    
    file_lengths, free_lengths = parse_disk_map(disk_map)
    initial_blocks = create_block_representation(file_lengths, free_lengths)
    final_blocks = compact_disk_whole_files(initial_blocks)
    
    return calculate_checksum(final_blocks)

if __name__ == "__main__":
    input_file = "inputs/day09.txt"
    print(part1(input_file))
    print(part2(input_file))