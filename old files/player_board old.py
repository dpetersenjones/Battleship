import json

class PlayerBoard:
    def __init__(self) -> None:
        """
        This is the code that keeps track of the player's board.

        Args:
            pos (dict): This dictionary says the size of the boat, the starting position of the boat, and the orientation of the boat
        """
        ###Translate is only need if doing a text base game
        # self.translate = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7,"I":8, "J":9}
        # self.translate2 = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J"}
        ###TODO: Board might not be needed, just positions.
        self.shooting_attemps = []
        # self.enemy_attempts = []
        self.boat_info = {
            "all_boats_coor": [],
            "boat2": {
                "pos":[],
                "hits":0,
            },
            "boat3": {
                "pos":[],
                "hits":0,
            },
            "boat4": {
                "pos":[],
                "hits":0,
            },
            "boat5": {
                "pos":[],
                "hits":0,
            },
        }
        # self.all_boats_coor = []
        self.board = []
        # self.boat2_pos = []
        # self.boat2_hits = 0
        # self.boat3_pos = []
        # self.boat3_hits = 0
        # self.boat4_pos = []
        # self.boat4_hits = 0
        # self.boat5_pos = []
        # self.boat5_hits = 0
        self.create_board()

        
    def serialize(self):
        """
        Used to serialize the info, so it can be saved easier.
        """
        return json.dumps({
            "shots": self.shooting_attemps,
            "boats": self.boat_info,
        })

    def take_hit(self, pos):
        if pos in self.boat_info["all_boats_coor"]:
            self.board[pos[0]][pos[1]] = "X"
            if pos in self.boat_info["boat2"]["pos"]:
                self.boat_info["boat2"]["hits"] += 1
                if self.boat_info["boat2"]["hits"] == 2:
                    return [True, True]
                return [True, False]
            if pos in self.boat_info["boat3"]["pos"]:
                self.boat_info["boat3"]["hits"]+= 1
                if self.boat_info["boat3"]["hits"] == 3:
                    return [True, True]
                return [True, False]
            if pos in self.boat_info["boat4"]["pos"]:
                self.boat_info["boat4"]["hits"] += 1
                if self.boat_info["boat4"]["hits"] == 4:
                    return [True, True]
                return [True, False]
            if pos in self.boat_info["boat5"]["pos"]:
                self.boat_info["boat5"]["hits"] += 1
                if self.boat_info["boat5"]["hits"] == 5:
                    return [True, True]
                return [True, False]

        else:
            self.board[pos[0]][pos[1]] = "M"
            return [False, False]

    def game_over_check(self):
        if self.boat_info["boat2"]["hits"] == 2 and self.boat_info["boat3"]["hits"] == 3 and self.boat_info["boat4"]["hits"] == 4 and self.boat_info["boat5"]["hits"] == 5:
            print("You have lost. Try again.")
            return True
        return False

    def player_shoot(self, pos_coor:list):
        # pos = input("Where would you like to shoot? ")
        # pos_coor = self.translate_shot(pos)
        # while pos_coor[0] == -1 or pos_coor in self.shooting_attemps:
        #     if pos_coor[0] == -1:
        #         pos = input("That isn't an acceptable position. Try again. ")
        #     elif pos_coor in self.shooting_attemps:
        #         pos = input("You already fired there. Try again. ")
        #     pos_coor = self.translate_shot(pos)
        self.shooting_attemps.append(pos_coor)
        return pos_coor

    ###No need to translate shot since data will be pass through as a json
    # def translate_shot(self, phrase):
    #     answer = []
    #     #Remove Print Phrases
    #     print(phrase[0])
    #     print(phrase[0].upper() == "A")
    #     if phrase[0].upper() not in self.translate:
    #         return [-1, -1]
    #     answer.append(self.translate[phrase[0].upper()])
    #     #print(phrase[1:])
    #     try:
    #         if 0 <= int(phrase[1:]) - 1 <= 9:
    #             #print(phrase[1])
    #             answer.append(int(phrase[1:]) - 1)
    #         else:
    #             return [-1, -1]
    #     except:
    #         #print("Here 1")
    #         return [-1, -1]
    #     return answer

    def create_board(self):
        #Creating the board
        for _ in range(10):
            self.board.append(["0"]*10)

    def check(self, pos):
            if pos[0] == False and pos[1] == False:
                return False
            if pos in self.boat_info["all_boats_coor"]:
                return False
            for n in pos:
                if n < 0 or n > 9:
                    return False
            return True
    
    # def translator(self, phrase):
    #         answer = []
    #         print(phrase[0])
    #         print(phrase[0].upper() == "A")
    #         if phrase[0].upper() not in self.translate:
    #             return [-1, -1]
    #         answer.append(self.translate[phrase[0].upper()])
    #         #print(phrase[1:])
    #         try:
    #             if 0 <= int(phrase[1:]) - 1 <= 9:
    #                 #print(phrase[1])
    #                 answer.append(int(phrase[1:]) - 1)
    #             else:
    #                 return [-1, -1]
    #         except:
    #             #print("Here 1")
    #             return [-1, -1]
    #         if answer in self.all_boats_coor:
    #             #print("Here 2")
    #             return [-1, -1]
    #         return answer
    
    ###TODO: Make a function that takes A JSON or DICT to place boat.
    def place_boats(self, boats:dict):
        
        for boat in boats:
            temp = []
            length = boat["length"]
            oreintation = boat["orientation"]
            position = boat["position"]
            if  oreintation == "v":
                for i in range(length):
                    temp.append([position[0] + i, position[1]])
                    self.boat_info["all_boats_coor"].append([position[0] + i, position[1]])
            else:
                for i in range(length):
                    temp.append([position[0], position[1] + 1])
                    self.boat_info["all_boats_coor"].append([position[0], position[1] + 1])
            if length == 2:
                self.boat_info["boat2"]["pos"] = temp.copy()
            elif length == 3:
                self.boat_info["boat3"]["pos"] = temp.copy()
            elif length == 4:
                self.boat_info["boat4"]["pos"] = temp.copy()
            elif length == 5:
                self.boat_info["boat5"]["pos"] = temp.copy()

    ###Reworking to take an Object that has the information
    # def placement(self):
    #     def get_placement(shipsize):
    #         start = input("Where do you want to start you ship? ")
    #         start_coor = self.translator(start)
    #         while start_coor[0] == -1:
    #             start = input("That isn't an acceptable position. Please try again like A1. ")
    #             start_coor = self.translator(start)
    #         orientation = input("Do you want it to be (h)orizontal or (v)ertical? ")
    #         while orientation.lower() != "v" and orientation.lower() != "h":
    #             print(orientation)
    #             print(orientation.lower() != "v")
    #             print(orientation.lower() != "h")
    #             orientation = input("Please use v or h. ")
    #         pos = []
    #         pos.append(start_coor)
    #         if orientation == "h":
    #             for i in range(1, shipsize):
    #                 if not self.check([start_coor[0], start_coor[1] + i]):
    #                     print("This ship position won't work, please try again.")
    #                     return get_placement(shipsize)
    #                 pos.append([start_coor[0], start_coor[1]+i])
    #         elif orientation == "v":
    #             for i in range(1, shipsize):
    #                 if not self.check([start_coor[0] + i, start_coor[1]]):
    #                     print("This ship position won't work, please try again.")
    #                     return get_placement(shipsize)
    #                 pos.append([start_coor[0] + i, start_coor[1]])
    #         return pos


    #     #Boat 2 placement
    #     print("Boat 2")
    #     self.boat2_pos = get_placement(2)
    #     self.all_boats_coor += self.boat2_pos
    #     for c in self.boat2_pos:
    #         self.board[c[0]][c[1]] = "2"
    #     self.print_board()
    #     #Boat 3 placement
    #     print("Boat 3")
    #     self.boat3_pos = get_placement(3)
    #     self.all_boats_coor += self.boat3_pos
    #     for c in self.boat3_pos:
    #         self.board[c[0]][c[1]] = "3"
    #     self.print_board()
    #     #Boat 4 placement
    #     print("Boat 4")
    #     self.boat4_pos = get_placement(4)
    #     self.all_boats_coor += self.boat4_pos
    #     for c in self.boat4_pos:
    #         self.board[c[0]][c[1]] = "4"
    #     self.print_board()
    #     #Boat 5 Placement
    #     print("Boat 5")
    #     self.boat5_pos = get_placement(5)
    #     self.all_boats_coor += self.boat5_pos
    #     for c in self.boat5_pos:
    #         self.board[c[0]][c[1]] = "5"
    #     self.print_board()

    ###No need for a print function if there is a visual aspect.
    def print_board(self):
        print("    1    2    3    4    5    6    7    8    9    10")
        for i in range(len(self.board)):
            print(f"{self.board[i]}")

