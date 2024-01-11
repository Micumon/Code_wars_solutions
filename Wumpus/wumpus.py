class Field:
    def __init__(self, number, info):
        self.number = number
        self.adjacent = self.__neighbor_maker()
        self.__info = [info]
        self.possible_moves = self.__possible_moves_maker()
        self.made_moves = []

    def __str__(self):
        return str(self.number)

    def __int__(self):
        return self.number

    @property
    def left_moves(self):
        left_moves = [i for i in self.possible_moves if i not in self.made_moves]
        if left_moves:
            return left_moves
        else:
            return False

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
                              if 16 >= i > 0])


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
                self[field].possible_moves = [i for i in self[field].adjacent
                                              if i != pit.number and i not in [j.number for j in self.pits]]


class Agent:
    def __init__(self, ag_cave):
        self.cave = Cave(ag_cave)
        self.wumpus_knowledge = [i for i in range(1, 17)]
        self.pit_knowledge = dict()
        self.__been = [self.cave[1]]
        self.wumpus_killed = False
        self.pits_known = []

    @property
    def been(self):
        return self.__been

    @been.setter
    def been(self, new: Field):
        if new.number in self.wumpus_knowledge:
            self.wumpus_knowledge.remove(new.number)
        self.__been.append(new)

    def __where_to_go(self):
        if self.been[-1].left_moves:
            return self.cave[self.been[-1].left_moves[0]]
        else:
            return self.__go_back()

    def __go_back(self):
        for field in self.been:
            if field.left_moves:
                self.__been.append(field)
                return self.cave[field.left_moves[0]]
        return False

    def __move(self, destination: Field):
        self.been[-1].made_moves.append(destination.number)
        destination.made_moves.append(self.been[-1].number)
        self.been = destination

    def __check_field(self):
        for restr in self.been[-1].info:
            match restr:
                case "ww":
                    if not self.wumpus_killed:
                        new_wumpus_knowledge = [i for i in self.been[-1].adjacent if i in self.wumpus_knowledge]
                        self.wumpus_knowledge = new_wumpus_knowledge
                        if len(self.wumpus_knowledge) == 1:
                            self.cave.kill_wumpus()
                            self.wumpus_killed = True
                case "pp":
                    if len(self.pits_known) < self.cave.pits_count:
                        self.pit_knowledge.update({self.been[-1].number: list(self.been[-1].adjacent)})
                case "G":
                    return True
        return False

    def __analyze_information(self):
        decision_maker = []
        visited_fields = list(set([i.number for i in self.been]))
        if len(self.pits_known) < self.cave.pits_count:
            for field in self.pit_knowledge:
                for adj in self.pit_knowledge[field].copy():
                    if adj in visited_fields:
                        self.pit_knowledge[field].remove(adj)
            for field in self.pit_knowledge.copy():
                if len(self.pit_knowledge[field]) == 1:
                    if self.cave[self.pit_knowledge[field][0]] not in self.pits_known:
                        self.pits_known.append(self.cave[self.pit_knowledge[field][0]])
                        self.cave.located_pit(self.cave[self.pit_knowledge[field][0]])
                        try:
                            self.wumpus_knowledge.remove(self.pit_knowledge[field][0])
                        except ValueError:
                            pass
                        self.pit_knowledge.pop(field)
                        decision_maker.append("new moves")
        else:
            decision_maker.append("nothing new")
        if not self.wumpus_killed:
            if len(self.wumpus_knowledge) == 1:
                self.cave.kill_wumpus()
                decision_maker.append(["new moves"])
            else:
                decision_maker.append(["nothing new"])
        for decision in decision_maker:
            match decision:
                case "new moves":
                    return "go"
        return "lost"

    def run_simulation(self):
        for field in self.cave.pits:
            if field.number == 2 or field.number == 5:
                return False
        if self.cave.wumpus.number == 2 or self.cave.wumpus.number == 5:
            return False
        if self.cave.pits_count == 1:
            return True
        if self.cave.wumpus.number == 6:
            self.cave.kill_wumpus()
        if self.cave.pits_count == 2 and self.cave.treasure.number not in [4, 16, 13]:
            return True

        i = 0
        while i < 10000:
            move = self.__where_to_go()
            if move:
                self.__move(move)
                win = self.__check_field()
                if win:
                    return True
            else:
                decision = self.__analyze_information()
                if decision == "lost":
                    return False
            i += 1
        return "zjebałeś coś"


cave = [
    [*"__GP"],
    [*"_P__"],
    [*"W___"],
    [*"____"]]

def wumpus_world(cave):
    player = Agent(cave)
    return player.run_simulation()



print(wumpus_world(cave))



