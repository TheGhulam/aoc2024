import requests
import os
from pathlib import Path
import argparse

def fetch_aoc_input(day: int, cookie: str, year: int = 2024) -> str:
    """
    Fetch input for specified Advent of Code day using session cookie
    
    Args:
        day (int): Day number
        cookie (str): Session cookie value
        year (int): Year (defaults to 2024)
    """
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    
    headers = {
        'Cookie': f'session={cookie}',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch input: {response.status_code}")
        
    return response.text

def main():
    parser = argparse.ArgumentParser(description='Fetch Advent of Code input')
    parser.add_argument('day', type=int, help='Day number')
    parser.add_argument('--year', type=int, default=2024, help='Year (defaults to 2024)')
    args = parser.parse_args()
    
    # Read cookie from .env file
    try:
        with open('.env') as f:
            cookie = f.read().strip()
    except FileNotFoundError:
        print("Please create a .env file with your session cookie value")
        return
        
    try:
        input_text = fetch_aoc_input(args.day, cookie, args.year)
        
        # Create inputs directory if it doesn't exist
        Path('inputs').mkdir(exist_ok=True)
        
        # Save input to file
        input_file = Path(f'inputs/day{args.day:02d}.txt')
        input_file.write_text(input_text)
        
        print(f"Successfully saved input to {input_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()