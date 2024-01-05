class Field:
    def __init__(self, number, info):
        self.number = number
        self.adjacent = self.__neighbor_maker()
        self.__info = [info]
        self.possible_moves = self.__possible_moves_maker()
        self.made_moves = []

    def __str__(self):
        return ", ".join(self.__info)

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, info):
        self.__info.append(info)

    def __possible_moves_maker(self):
        if self.info == "P" or self.info == "W":
            return []
        else:
            return list(self.adjacent)

    def __neighbor_maker(self):
        match self.number:
            case 4:
                return 3, 8
            case 5:
                return 1, 6, 9
            case 8:
                return 4, 7, 12
            case 9:
                return 5, 10, 13
            case 12:
                return 8, 11, 16
            case 13:
                return 9, 14
            case _:
                return tuple([i for i in (self.number - 1, self.number + 1, self.number - 4, self.number + 4)
                              if 16 > i > 0])


class Cave:
    def __init__(self, cave):
        self.__iter_count = 0
        self.pits_count = self.pits_count(cave)
        self.layout = self.layout_maker(cave)
        self.__layout_info_filler()
        self.treasure = self.__treasure_pos()
        self.wumpus = self.__wumpus_pos()
        self.pits = self.__pits_pos()

    def __getitem__(self, item):
        return self.layout[item]

    def __next__(self):
        self.__iter_count += 1
        if self.__iter_count >= 17:
            self.__iter_count = 0
            raise StopIteration()
        return self[self.__iter_count]

    def __iter__(self):
        self.__iter_count = 0
        return self

    def __str__(self):
        string_out = ""
        for row in (1, 5, 9, 13):
            string_out += f"|\t{self[row]}\t||\t{self[row + 1]}\t||\t{self[row + 2]}\t||\t{self[row + 3]}\t|\n"
        return string_out

    @staticmethod
    def pits_count(cave):
        pits = 0
        for row in cave:
            pits += row.count("P")
        return pits

    def __treasure_pos(self):
        for field in self:
            for info in field.info:
                if info == "G":
                    return field

    def __wumpus_pos(self):
        for field in self:
            for info in field.info:
                if info == "W":
                    return field

    def __pits_pos(self):
        result_pits = []
        for field in self:
            for info in field.info:
                if info == "P":
                    result_pits.append(field)
        return result_pits


    @staticmethod
    def layout_maker(cave):

        string_form = ""
        for row in cave:
            for col in row:
                string_form += col
        result = {}
        for i in range(len(string_form)):
            result.update({i+1: Field(i+1, string_form[i])})
        return result

    def __layout_info_filler(self):
        for field in self:
            for info in field.info:
                if info == "W":
                    for neighbor in field.adjacent:
                        self[neighbor].info = "ww"
                        self[neighbor].possible_moves = []
                elif info == "P":
                    for neighbor in field.adjacent:
                        self[neighbor].info = "pp"
                        self[neighbor].possible_moves = []

    def kill_wumpus(self):
            pass


class Agent:
    def __init__(self, ag_cave):
        self.route = [(0, 0)]
        self.cave = Cave(ag_cave)
        self.wumpus_knowledge = [(i, j) for i in range(4) for j in range(4) if (i, j) != (0, 0)]
        self.__wumpus_knowledge_not = [(0, 0)]
        self.pit_knowledge = {m + 1: [(i, j) for i in range(4) for j in range(4) if (i, j) != (0, 0)]
                              for m in range(self.cave.pits_count)}
        self.__pit_knowledge_not = [(0, 0)]
        self.field_is_clear = [(0, 0)]
        self.back = ()
        self.map = {(0, 0): {"pos": self.possible_moves,
                             "made": []}
                    }

    @property
    def wumpus_knowledge_not(self):
        return self.__wumpus_knowledge_not

    @wumpus_knowledge_not.setter
    def wumpus_knowledge_not(self, value):
        try:
            self.wumpus_knowledge.remove(value)
        except ValueError:
            pass

        if value not in self.__wumpus_knowledge_not:
            self.__wumpus_knowledge_not.append(value)

    @property
    def pit_knowledge_not(self):
        return self.__pit_knowledge_not

    @pit_knowledge_not.setter
    def pit_knowledge_not(self, value):
        for i in self.pit_knowledge:
            try:
                self.pit_knowledge[i].remove(value)
            except ValueError:
                continue
        if value not in self.__pit_knowledge_not:
            self.__pit_knowledge_not.append(value)

    @property
    def field_restr(self):
        return cave[self.position[0]][self.position[1]].split("|")

    @property
    def position(self):
        return self.route[-1]

    @property
    def possible_moves(self):
        possible_moves = ["l", "r", "u", "d"]
        for restr in self.field_restr:
            match restr:
                case "ui":
                    try:
                        possible_moves.remove("u")
                    except ValueError:
                        continue
                case "li":
                    try:
                        possible_moves.remove("l")
                    except ValueError:
                        continue
                case "di":
                    try:
                        possible_moves.remove("d")
                    except ValueError:
                        continue
                case "ri":
                    try:
                        possible_moves.remove("r")
                    except ValueError:
                        continue
                case "G":
                    self.win()
        return possible_moves

    def check_wumpus_knowledge(self):
        if len(self.wumpus_knowledge) == 1:
            self.cave.kill_wumpus()

    def entered_ww(self):
        ww = self.position
        adjacent_to_ww = [(ww[0] - 1, ww[1]), (ww[0], ww[1] - 1), (ww[0] + 1, ww[1]), (ww[0], ww[1] + 1)]
        wumpus_maybe = self.wumpus_knowledge.copy()
        self.wumpus_knowledge = [i for i in adjacent_to_ww if i in wumpus_maybe]
        if len(self.wumpus_knowledge) == 1:
            self.cave.kill_wumpus()

    def entered_pp(self):
        pp = self.position
        adjacent_to_pp = [(pp[0] - 1, pp[1]), (pp[0], pp[1] - 1), (pp[0] + 1, pp[1]), (pp[0], pp[1] + 1)]

    def new_info(self):
        result = False
        for restr in self.field_restr:
            match restr:
                case "ww":
                    self.entered_ww()
                    result = True
                case "pp":
                    self.entered_pp()
                    result = True
        return result

    def check_new_moves(self):
        for field in self.map:
            if not set(self.map[field]["pos"]) == set(self.map[field]["made"]):
                self.go_to(field)

    def go_to(self, field):
        pass

    def move(self):
        self.pit_knowledge_not = self.position
        self.wumpus_knowledge_not = self.position
        back_move = self.new_info()
        if self.back == () and back_move:
            self.loose()
        if back_move:
            self.check_new_moves()

    def win(self):
        pass

    def loose(self):
        pass


cave = [
    [*"__PG"],
    [*"___W"],
    [*"__PP"],
    [*"____"]
]


def wumpus_world(cave):
    pass


for i in range(1, 17):
    print(f"dla {i}: " + str(Field(i, "a").adjacent))

a = Cave(cave)
for i in a:
    print(f"{i.number} = {i.possible_moves}, {i.info}")

print(a)
print(a[2].possible_moves)
print(a[1].possible_moves)
print(a.treasure.number, a.treasure.possible_moves, a.treasure)
print(a.wumpus.number)
print(a.pits[0].number, a.pits[1].number, a.pits[2].number)

