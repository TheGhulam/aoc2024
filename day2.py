import numpy as np

def is_safe_report(report):
    diff = np.diff(report) #len(diff) = len(report) - 1

    if np.any(diff == 0): return False
    if not np.all((abs(diff) >= 1) & (abs(diff) <= 3)): return False
    if not (np.all(diff > 0) or np.all(diff < 0)): return False

    return True

def is_almost_safe_report(report):
    if is_safe_report(report): return True

    for i in range(len(report)):
        dampened_report = np.delete(report, i)
        if is_safe_report(dampened_report): return True

    return False

def main():
    data = open('inputs/day02.txt', 'r').read()
    reports = [np.array([int(x) for x in line.strip().split()]) for line in data.strip().split('\n')]

    safe_levels = sum([is_safe_report(report) for report in reports])
    print("Safe levels: ", safe_levels)

    almost_safe_levels = sum([is_almost_safe_report(report) for report in reports])
    print("Almost safe levels: ", almost_safe_levels)
    

if __name__ == "__main__":
    main()