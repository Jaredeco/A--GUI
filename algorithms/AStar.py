def a_star(grid):
    rs, cs = grid.start
    start_node = grid.grid[rs][cs]
    start_node.g = start_node.h = start_node.f = 0
    rt, ct = grid.target
    end_node = grid.grid[rt][ct]
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []
    open_list.append(start_node)
    while len(open_list) > 0:
        min_node = open_list[0]
        min_idx = 0
        for idx, node in enumerate(open_list):
            if node.f < min_node.f:
                min_node = node
                min_idx = idx
        open_list.pop(min_idx)
        closed_list.append(min_node)
        if min_node == end_node:
            path = []
            cur = min_node
            while cur is not None:
                path.append(cur.pos)
                cur = cur.parent
            grid.shortest_path = path[::-1]
            return

        mr, mc = min_node.pos
        neighbours = []
        n_positions = [(mr + 1, mc), (mr, mc + 1), (mr - 1, mc), (mr, mc - 1), (mr + 1, mc + 1),
                       (mr - 1, mc - 1), (mr + 1, mc - 1), (mr - 1, mc + 1)]
        for rn, cn in n_positions:
            dim = grid.dim
            if not (0 <= rn < dim and 0 <= cn < dim) or grid.grid[rn][cn].is_wall:
                continue
            neighbours.append(grid.grid[rn][cn])

        for nn in neighbours:
            if len([cn for cn in closed_list if cn == nn]):
                continue
            nn.parent = min_node
            nn.g = (((nn.pos[0] - nn.parent.pos[0]) ** 2) + ((nn.pos[1] - nn.parent.pos[1]) ** 2))**0.5
            nn.h = (((nn.pos[0] - end_node.pos[0]) ** 2) + ((nn.pos[1] - end_node.pos[1]) ** 2))**0.5
            nn.f = nn.g + nn.h
            if len([on for on in open_list if nn.pos == on.pos and nn.g > on.g]):
                continue
            open_list.append(nn)
    print("No path!")
    return []
