def read_pairs(filename):
    left_nums = []
    right_nums = []
    
    with open(filename, 'r') as file:
        for line in file:
            # Split each line into left and right numbers
            left, right = map(int, line.strip().split())
            left_nums.append(left)
            right_nums.append(right)
    
    return left_nums, right_nums

def calculate_total_distance(left_nums, right_nums):
    # Sort both lists to pair smallest with smallest, etc.
    left_sorted = sorted(left_nums)
    right_sorted = sorted(right_nums)
    
    total_distance = 0
    
    # Calculate distance between each pair
    for left, right in zip(left_sorted, right_sorted):
        distance = abs(left - right)
        total_distance += distance
    
    return total_distance

def main():
    # Read input
    left_nums, right_nums = read_pairs('day1.txt')
    
    # Calculate and print result
    result = calculate_total_distance(left_nums, right_nums)
    print(f"Total distance: {result}")

if __name__ == "__main__":
    main()