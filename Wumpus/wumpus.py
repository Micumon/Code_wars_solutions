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

    @property
    def is_wumpus(self):
        return True if "W" in self.__info else False

    @property
    def is_pit(self):
        return True if "P" in self.__info else False

    @property
    def is_treasure(self):
        return True if "G" in self.__info else False

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
        self.layout = self.layout_maker(cave)
        self.__layout_info_filler()
        self.treasure = self.__treasure_pos()
        self.wumpus = self.__wumpus_pos()
        self.pits, self.pits_count = self.__pits_pos_count()

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

    def __treasure_pos(self):
        for field in self:
            if field.is_treasure:
                return field

    def __wumpus_pos(self):
        for field in self:
            if field.is_wumpus:
                return field

    def __pits_pos_count(self):
        result_pits = []
        for field in self:
            if field.is_pit:
                result_pits.append(field)
        pits = 0
        for field in self:
            pits += 1 if field.is_pit else 0
        return result_pits, pits

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
        self.wumpus.info.remove("W")
        if "pp" not in self.wumpus.info:
            self.wumpus.possible_moves = list(self.wumpus.adjacent)
        for neighbor in self.wumpus.adjacent:
            self[neighbor].info.remove("ww")
            if "pp" in self[neighbor].info:
                self[neighbor].possible_moves.append(self.wumpus.number)
            else:
                self[neighbor].possible_moves = list(self[neighbor].adjacent)

    def located_pit(self, pit: Field):
        for field in pit.adjacent:
            self[field].info.remove("pp")
            if "pp" not in self[field].info and "ww" not in self[field].info:
                self[field].possible_moves = [i for i in self[field].adjacent if i != pit.number]


class Agent:
    def __init__(self, ag_cave):
        self.cave = Cave(ag_cave)
        self.wumpus_knowledge = [i for i in self.cave]
        self.pit_knowledge = dict()
        self.__route = [self.cave[1]]

    def run_simulation(self):
        pass

    @staticmethod
    def win(self):
        return True

    @staticmethod
    def loose(self):
        return False


cave = [
    [*"__PG"],
    [*"___W"],
    [*"__PP"],
    [*"____"]
]


def wumpus_world(cave):
    player = Agent(cave)
    return player.run_simulation()



