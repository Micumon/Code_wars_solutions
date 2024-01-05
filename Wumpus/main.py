cave = [
    [*"__PG"],
    [*"___W"],
    [*"__PP"],
    [*"____"]
]


def wumpus_pos(cave):
    for row in range(4):
        for col in range(4):
            if "W" in cave[row][col]:
                return row, col


def pits_pos(cave):
    pos = []
    for row in range(4):
        for col in range(4):
            if "P" in cave[row][col]:
                pos.append((row, col))
    return pos


def list_of_wumpus_corners(w):
    corners = [(w[0] - 1, w[1] - 1), (w[0] - 1, w[1] + 1), (w[0] + 1, w[1] - 1), (w[0] + 1, w[1] + 1)]
    return corners


def wumpus_in_corridor(cave):
    wumpus = wumpus_pos(cave)
    pits = pits_pos(cave)
    wumpus_corners = list_of_wumpus_corners(wumpus)
    corner_pits_count = 0
    corner_pits = []
    for pit in pits:
        if pit in wumpus_corners:
            corner_pits_count += 1
            corner_pits.append(pit)
    if corner_pits_count >= 3:
        return True
    elif corner_pits_count < 2:
        return False
    elif corner_pits_count == 2:
        if (corner_pits[0][0] == corner_pits[1][0]) or (corner_pits[0][1] == corner_pits[1][1]):
            return True


def new_route_id(routes):
    return max(list(routes.keys())) + 1


def kill_wumpus(cave, routes):
    for route in routes:
        if "stop" in routes[route]:
            routes[route].remove("stop")
    for row in range(4):
        for col in range(4):
            if ",ww," in cave[row][col]:
                cave[row][col] = cave[row][col].replace(",ww,","")
            if "W" in cave[row][col]:
                cave[row][col] = cave[row][col].replace("W", "_")
                if col != 0 and row != 0 and row != 3 and col != 3:
                    cave[row-1][col] = cave[row-1][col].replace(",di,", "")
                    cave[row+1][col] = cave[row+1][col].replace(",ui,", "")
                    cave[row][col-1] = cave[row][col-1].replace(",ri,", "")
                    cave[row][col+1] = cave[row][col+1].replace(",li,", "")
                elif col == 0 and row != 0 and row != 3:
                    cave[row-1][col] = cave[row-1][col].replace(",di,", "")
                    cave[row+1][col] = cave[row+1][col].replace(",ui,", "")
                    cave[row][col+1] = cave[row][col+1].replace(",li,", "")
                elif col != 0 and row == 0 and col != 3:
                    cave[row+1][col] = cave[row+1][col].replace(",ui,", "")
                    cave[row][col-1] = cave[row][col-1].replace(",ri,", "")
                    cave[row][col+1] = cave[row][col+1].replace(",li,", "")
                elif col != 0 and row == 3 and col != 3:
                    cave[row-1][col] = cave[row-1][col].replace(",di,", "")
                    cave[row][col-1] = cave[row][col-1].replace(",ri,", "")
                    cave[row][col+1] = cave[row][col+1].replace(",li,", "")
                elif row != 0 and row != 3 and col == 3:
                    cave[row-1][col] = cave[row-1][col].replace(",di,", "")
                    cave[row+1][col] = cave[row+1][col].replace(",ui,", "")
                    cave[row][col-1] = cave[row][col-1].replace(",ri,", "")
                elif row == 3 and col == 3:
                    cave[row-1][col] = cave[row-1][col].replace(",di,", "")
                    cave[row][col-1] = cave[row][col-1].replace(",ri,", "")
                elif row == 0 and col == 3:
                    cave[row+1][col] = cave[row+1][col].replace(",ui,", "")
                    cave[row][col-1] = cave[row][col-1].replace(",ri,", "")
                elif col == 0 and row == 3:
                    cave[row-1][col] = cave[row-1][col].replace(",di,", "")
                    cave[row][col+1] = cave[row][col+1].replace(",li,", "")


def check_routes(route, cave, routes, route_id, ww):
    field = route[-1]
    if field == "stop":
        return False, ww
    field_restr = cave[field[0]][field[1]].split(",")
    possible_moves = ["l", "r", "u", "d"]
    if "ww" in field_restr and field not in ww:
        ww.append(field)

    for restr in field_restr:
        match restr:
            case "ui":
                try:
                    possible_moves.remove("u")
                except:
                    continue
            case "li":
                try:
                    possible_moves.remove("l")
                except:
                    continue
            case "di":
                try:
                    possible_moves.remove("d")
                except:
                    continue
            case "ri":
                try:
                    possible_moves.remove("r")
                except:
                    continue
            case "G":
                return True, ww

    new_routes = []
    if len(possible_moves) == 0 and len(ww) >= 2:
        routes.pop(route_id)
    elif len(possible_moves) == 0 and len(ww) < 2:
        routes[route_id].append("stop")
    else:
        for i in range(len(possible_moves)):
            if i == 0:
                new_routes.append(route_id)
            else:
                new_routes.append(new_route_id(routes))
                routes.update({new_routes[i]: route.copy()})
        for move, r_id in zip(possible_moves, new_routes):
            match move:
                case "l":
                    routes[r_id].append((field[0], field[1]-1))
                    cave[field[0]][field[1]-1] += ",ri,"
                    cave[field[0]][field[1]] += ",li,"
                case "r":
                    routes[r_id].append((field[0], field[1]+1))
                    cave[field[0]][field[1]+1] += ",li,"
                    cave[field[0]][field[1]] += ",ri,"
                case "u":
                    routes[r_id].append((field[0]-1, field[1]))
                    cave[field[0]-1][field[1]] += ",di,"
                    cave[field[0]][field[1]] += ",ui,"
                case "d":
                    routes[r_id].append((field[0]+1, field[1]))
                    cave[field[0]+1][field[1]] += ",ui,"
                    cave[field[0]][field[1]] += ",di,"
    return False, ww


def stop_check(routes):
    i = len(routes)
    for route in routes:
        if "stop" in routes[route]:
            i -= 1
    if i <= 0:
        return False
    return True

def cave_restrict(cave):
    for row in range(4):
        for col in range(4):
            if col != 0 and row != 0 and row != 3 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
                cave[row - 1][col] += ",di," + ",ww," if cave[row][col] == "W" else ",di,"
                cave[row + 1][col] += ",ui," + ",ww," if cave[row][col] == "W" else ",ui,"
                cave[row][col - 1] += ",ri," + ",ww," if cave[row][col] == "W" else ",ri,"
                cave[row][col + 1] += ",li," + ",ww," if cave[row][col] == "W" else ",li,"
            elif col == 0 and row != 0 and row != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
                cave[row - 1][col] += ",di," + ",ww," if cave[row][col] == "W" else ",di,"
                cave[row + 1][col] += ",ui," + ",ww," if cave[row][col] == "W" else ",ui,"
                cave[row][col + 1] += ",li," + ",ww," if cave[row][col] == "W" else ",li,"
            elif col != 0 and row == 0 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
                cave[row + 1][col] += ",ui," + ",ww," if cave[row][col] == "W" else ",ui,"
                cave[row][col - 1] += ",ri," + ",ww," if cave[row][col] == "W" else ",ri,"
                cave[row][col + 1] += ",li," + ",ww," if cave[row][col] == "W" else ",li,"
            elif col != 0 and row == 3 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
                cave[row - 1][col] += ",di," + ",ww," if cave[row][col] == "W" else ",di,"
                cave[row][col - 1] += ",ri," + ",ww," if cave[row][col] == "W" else ",ri,"
                cave[row][col + 1] += ",li," + ",ww," if cave[row][col] == "W" else ",li,"
            elif row != 0 and row != 3 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
                cave[row - 1][col] += ",di," + ",ww," if cave[row][col] == "W" else ",di,"
                cave[row + 1][col] += ",ui," + ",ww," if cave[row][col] == "W" else ",ui,"
                cave[row][col - 1] += ",ri," + ",ww," if cave[row][col] == "W" else ",ri,"
            elif row == 3 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
                cave[row - 1][col] += ",di," + ",ww," if cave[row][col] == "W" else ",di,"
                cave[row][col - 1] += ",ri," + ",ww," if cave[row][col] == "W" else ",ri,"
            elif row == 0 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
                cave[row + 1][col] += ",ui," + ",ww," if cave[row][col] == "W" else ",ui,"
                cave[row][col - 1] += ",ri," + ",ww," if cave[row][col] == "W" else ",ri,"
            elif col == 0 and row == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
                cave[row - 1][col] += ",di," + ",ww," if cave[row][col] == "W" else ",di,"
                cave[row][col + 1] += ",li," + ",ww," if cave[row][col] == "W" else ",li,"

            if row == 0:
                cave[row][col] += ",ui,"
            if row == 3:
                cave[row][col] += ",di,"
            if col == 0:
                cave[row][col] += ",li,"
            if col == 3:
                cave[row][col] += ",ri,"


def wumpus_world(cave):
    agent_know = 0
    routes = {0: [(0, 0)]}
    agent_know_ww = []
    treasure = [5,5]

    for row in cave:
        agent_know += row.count("P")

    for row in range(4):
        for col in range(4):
            if cave[row][col] == "G":
                treasure = [row, col]
    if treasure == [5, 5]:
        print(treasure)

    if agent_know <= 2 and 0 < treasure[0] < 3 and 0 < treasure[1] < 3:
        return True

    cave_restrict(cave)

    if agent_know >= 2 and wumpus_in_corridor(cave):
        kill_wumpus(cave, routes)

    win = False
    while not win:
        routes_copy = routes.copy()
        for i in routes_copy:
            win, agent_know_ww = check_routes(routes[i], cave, routes, i, agent_know_ww)
            if win:
                return True
        if len(routes) == 0 or not stop_check(routes):
            return False
        if 2 <= len(agent_know_ww) <= 100:
            kill_wumpus(cave, routes)
            agent_know_ww *= 101

    return True





print(wumpus_world(cave))

#         if col != 0 and row != 0 and row != 3 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
#             cave[row - 1][col] += ww_or_pp(cave[row][col], "di")
#             cave[row + 1][col] += ww_or_pp(cave[row][col], "ui")
#             cave[row][col - 1] += ww_or_pp(cave[row][col], "ri")
#             cave[row][col + 1] += ww_or_pp(cave[row][col], "li")
#         elif col == 0 and row != 0 and row != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
#             cave[row - 1][col] += ww_or_pp(cave[row][col], "di")
#             cave[row + 1][col] += ww_or_pp(cave[row][col], "ui")
#             cave[row][col + 1] += ww_or_pp(cave[row][col], "li")
#         elif col != 0 and row == 0 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
#             cave[row + 1][col] += ww_or_pp(cave[row][col], "ui")
#             cave[row][col - 1] += ww_or_pp(cave[row][col], "ri")
#             cave[row][col + 1] += ww_or_pp(cave[row][col], "li")
#         elif col != 0 and row == 3 and col != 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
#             cave[row - 1][col] += ww_or_pp(cave[row][col], "di")
#             cave[row][col - 1] += ww_or_pp(cave[row][col], "ri")
#             cave[row][col + 1] += ww_or_pp(cave[row][col], "li")
#         elif row != 0 and row != 3 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
#             cave[row - 1][col] += ww_or_pp(cave[row][col], "di")
#             cave[row + 1][col] += ww_or_pp(cave[row][col], "ui")
#             cave[row][col - 1] += ww_or_pp(cave[row][col], "ri")
#         elif row == 3 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
#             cave[row - 1][col] += ww_or_pp(cave[row][col], "di")
#             cave[row][col - 1] += ww_or_pp(cave[row][col], "ri")
#         elif row == 0 and col == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
#             cave[row + 1][col] += ww_or_pp(cave[row][col], "ui")
#             cave[row][col - 1] += ww_or_pp(cave[row][col], "ri")
#         elif col == 0 and row == 3 and (cave[row][col] == "W" or cave[row][col] == "P"):
#             cave[row - 1][col] += ww_or_pp(cave[row][col], "di")
#             cave[row][col + 1] += ww_or_pp(cave[row][col], "li")
#
#         if row == 0:
#             cave[row][col] += "|ui"
#         if row == 3:
#             cave[row][col] += "|di"
#         if col == 0:
#             cave[row][col] += "|li"
#         if col == 3:
#             cave[row][col] += "|ri"
# return cave