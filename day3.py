import re
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Instruction:
    type: str  # 'mul', 'do', or 'dont'
    position: int
    nums: Tuple[int, int] = None  # Only for mul instructions

def part1(filename):
    # Read the input file
    with open(filename, 'r') as f:
        text = f.read()
    
    # Regular expression to match valid mul(X,Y) instructions
    # Must be exactly "mul(" followed by 1-3 digits, comma, 1-3 digits, and closing parenthesis
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    
    total_sum = 0
    count = 0
    
    # Find all matches and calculate sum
    for match in re.finditer(pattern, text):
        num1 = int(match.group(1))
        num2 = int(match.group(2))
        product = num1 * num2
        total_sum += product
        count += 1
    
    print(f"Found {count} valid multiplication instructions")
    print(f"Total sum of all multiplications: {total_sum}")
    return total_sum

def part2(filename: str) -> int:
    with open(filename, 'r') as f:
        text = f.read()
    
    instructions = []
    
    # Find multiplication instructions
    for match in re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', text):
        instructions.append(Instruction(
            type='mul',
            position=match.start(),
            nums=(int(match.group(1)), int(match.group(2)))
        ))
    
    # Find do() instructions
    for match in re.finditer(r'do\(\)', text):
        instructions.append(Instruction(
            type='do',
            position=match.start()
        ))
    
    # Find don't() instructions
    for match in re.finditer(r'don\'t\(\)', text):
        instructions.append(Instruction(
            type='dont',
            position=match.start()
        ))
    
    # Sort instructions by position
    instructions.sort(key=lambda x: x.position)
    
    # Process instructions
    enabled = True  # Multiplications start enabled
    total_sum = 0
    enabled_count = 0
    disabled_count = 0
    
    for inst in instructions:
        if inst.type == 'do':
            enabled = True
        elif inst.type == 'dont':
            enabled = False
        elif inst.type == 'mul' and enabled:
            product = inst.nums[0] * inst.nums[1]
            total_sum += product
            enabled_count += 1
        elif inst.type == 'mul':
            disabled_count += 1
    
    print(f"Processed {len(instructions)} total instructions")
    print(f"Enabled multiplications: {enabled_count}")
    print(f"Disabled multiplications: {disabled_count}")
    print(f"Sum of enabled multiplications: {total_sum}")
    
    return total_sum

if __name__ == "__main__":
    part1("inputs/day03.txt")
    part2("inputs/day03.txt")