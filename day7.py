def evaluate_expression(nums, operators):
    """
    Evaluate expression from left to right, ignoring operator precedence.
    """
    result = nums[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            result += nums[i + 1]
        elif operators[i] == '*':
            result *= nums[i + 1]
        else:  # '||' concatenation
            result = int(str(result) + str(nums[i + 1]))
    return result


def part1(test_value, numbers):
    """
    Try all possible combinations of + and * operators between the numbers.
    Return True if any combination equals the test value.
    """
    n = len(numbers) - 1  # number of operators needed
    for i in range(2 ** n):  # each bit represents + (0) or * (1)
        operators = []
        for j in range(n):
            # Convert bit to operator: 0 -> '+', 1 -> '*'
            operators.append('+' if (i & (1 << j)) == 0 else '*')
        
        result = evaluate_expression(numbers, operators)
        if result == test_value:
            return True
    
    return False


def part2(test_value, numbers):
    """
    Try all possible combinations of + and * operators between the numbers.
    Return True if any combination equals the test value.
    """
    n = len(numbers) - 1  # number of operators needed
    operators = ['+', '*', '||']
    
    for combo in range(3 ** n):  # each position can be +, *, or ||
        current_operators = []
        temp = combo
        
        # Convert number to base-3 representation for operator selection
        for _ in range(n):
            current_operators.append(operators[temp % 3])
            temp //= 3
        
        result = evaluate_expression(numbers, current_operators)
        if result == test_value:
            return True
    
    return False

def main(input_text):
    res1, res2 = 0, 0
    
    for line in input_text.strip().split('\n'):
        test_part, nums_part = line.split(':')
        test_value = int(test_part.strip())
        numbers = [int(x) for x in nums_part.strip().split()]
        
        if part1(test_value, numbers):
            res1 += test_value
    
    for line in input_text.strip().split('\n'):
        test_part, nums_part = line.split(':')
        test_value = int(test_part.strip())
        numbers = [int(x) for x in nums_part.strip().split()]
        
        if part2(test_value, numbers):
            res2 += test_value
    
    return res1, res2

with open('inputs/day07.txt', 'r') as f:
    input_text = f.read()

print(main(input_text)) 