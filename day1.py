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
    left_sorted = sorted(left_nums)
    right_sorted = sorted(right_nums)
    
    total_distance = 0
    
    # Calculate distance between each pair
    for left, right in zip(left_sorted, right_sorted):
        distance = abs(left - right)
        total_distance += distance
    
    return total_distance

def calculate_similarity_score(left_nums, right_nums):
    total_score = 0
    
    for left_num in left_nums:
        appearances = right_nums.count(left_num)
        score = left_num * appearances
        total_score += score
    
    return total_score

def main():
    left_nums, right_nums = read_pairs('day1.txt')
    
    print(f"Total distance: {calculate_total_distance(left_nums, right_nums)}")
    print(f"Similarity score: {calculate_similarity_score(left_nums, right_nums)}")

if __name__ == "__main__":
    main()