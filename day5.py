from collections import defaultdict, deque

def parse_input(file):
    with open(file, 'r') as f:
        rules_txt, updates_txt = f.read().strip().split('\n\n')

        rules = []
        for line in rules_txt.split('\n'):
            before, after = map(int, line.split('|'))
            rules.append((before, after))
        
        updates = []
        for line in updates_txt.split('\n'):
            pages = list(map(int, line.split(',')))
            updates.append(pages)
        
        return rules, updates

def is_valid_order(pages, rules):
    page_positions = {page: i for i, page in enumerate(pages)}

    for before, after in rules:
        if before in page_positions and after in page_positions:
            if page_positions[before] > page_positions[after]:
                return False

    return True

def find_middle_pages(valid_updates):
    s = 0
    for u in valid_updates:
        m_idx = len(u) // 2
        s += u[m_idx]
    return s

def build_graph(pages, rules):
    """
    Builds a directed graph from the rules that apply to the given pages.
    Returns:
    - graph: adjacency list representation
    - in_degree: number of incoming edges for each node
    """

    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for p in pages:
        in_degree[p] = 0

    for before, after in rules:
        if before in pages and after in pages:
            graph[before].append(after)
            in_degree[after] += 1
    
    return graph, in_degree

def topological_sort(pages, rules):
    """
    Kahn's algorithm for topological sorting.
    """

    graph, in_degree = build_graph(pages, rules)
    queue = deque([p for p in pages if in_degree[p] == 0])
    res = []

    while queue:
        p = queue.popleft()
        res.append(p)

        for neighbor in graph[p]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return res if len(res) == len(pages) else None

def part1(file):
    rules, updates = parse_input(file)
    valid_updates = [u for u in updates if is_valid_order(u, rules)]
    return find_middle_pages(valid_updates)

def part2(file):
    rules, updates = parse_input(file)
    reordered_updates = []
    for u in updates:
        if not is_valid_order(u, rules):
            correct_order = topological_sort(u, rules)
            if correct_order:
                reordered_updates.append(correct_order)
            else:
                print(f"Warning: Cycle detected in update {u}")
    
    return find_middle_pages(reordered_updates)

if __name__ == "__main__":
    print(part1("inputs/day05.txt"))
    print(part2("inputs/day05.txt"))