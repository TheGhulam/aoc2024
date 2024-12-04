def part1(grid):
    m, n = len(grid), len(grid[0])
    c = 0

    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]

    def check(x, y, dx, dy):
        target = "XMAS"
        if not (0 <= x < m and 0 <= y < n):
            return False

        for i in range(4):
            X = x + i * dx
            Y = y + i * dy

            if not (0 <= X < m and 0 <= Y < n):
                return False
            
            if grid[X][Y] != target[i]:
                return False

        return True
    
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "X":
                for dx, dy in directions:
                    if check(i, j, dx, dy):
                        c += 1

    return c

def part2(grid):
    m, n = len(grid), len(grid[0])
    res = 0

    def check_mas(r1, c1, r2, c2, r3, c3):
        chars = grid[r1][c1] + grid[r2][c2] + grid[r3][c3]
        return chars in ["MAS", "SAM"]

    def check_xmas(r, c):
        tl_br = check_mas(r-1, c-1, r, c, r+1, c+1)
        tr_bl = check_mas(r-1, c+1, r, c, r+1, c-1)
        br_tl = check_mas(r+1, c+1, r, c, r-1, c-1)
        bl_tr = check_mas(r+1, c-1, r, c, r-1, c+1)
    
        return (tl_br and tr_bl) or (tl_br and bl_tr) or (br_tl and tr_bl) or (br_tl and bl_tr)
    
    for r in range(1, m-1):
        for c in range(1, n-1):
            if grid[r][c] == "A" and check_xmas(r, c):
                res += 1
    
    return res

if __name__ == "__main__":
    with open("inputs/day04.txt", "r") as f:
        grid = f.read().splitlines()
    
    print(part1(grid))
    print(part2(grid))