import json

class PlayerBoard:
    def __init__(self, boats: list[dict]=None) -> None:
        """
        This is the code that keeps track of the player's board.

        Args:
            pos (dict): This dictionary says the size of the boat, the starting position of the boat, and the orientation of the boat
        """
        self.shooting_attemps = []
        self.boat_info = {
            "all_boats_coor": [],
            "boats" : {
                "destroyer": {
                    "pos":[],
                    "start":None,
                    "hits":0,
                    "length":2,
                    "direction":None,
                    "sunk":False,
                },
                "submarine": {
                    "pos":[],
                    "start":None,
                    "hits":0,
                    "length":3,
                    "direction":None,
                    "sunk":False,
                },
                "cruiser": {
                    "pos":[],
                    "start":None,
                    "hits":0,
                    "length":3,
                    "direction":None,
                    "sunk":False,
                },
                "battleship": {
                    "pos":[],
                    "start":None,
                    "hits":0,
                    "length":4,
                    "direction":None,
                    "sunk":False,
                },
                "carrier": {
                    "pos":[],
                    "start":None,
                    "hits":0,
                    "length":5,
                    "direction":None,
                    "sunk":False,
                },}
        }
        self.board = []
        if boats:
            self.place_boats(boats)
        self.create_board()

    def get_boat_positions(self):
        data = {}
        for name, boat_data in self.boat_info["boats"].items():
            data[name] = {
            "type": name,
            "length": boat_data["length"],
            "direction": boat_data["direction"],
            "start": boat_data["start"]
        }
        return json.dumps({
            "data":data
        })
        
    def serialize(self):
        """
        Used to serialize the info, so it can be saved easier.
        """
        return json.dumps({
            "shots": self.shooting_attemps,
            "boats": self.boat_info,
        })
        
    @classmethod
    def deserialize(cls, info):
        new_class = cls()
        new_class.shooting_attemps = info.get("shots", [])
        new_class.boat_info = info.get("boats", {})
        return new_class
        

    def take_hit(self, coor) -> dict:
        """
        Handles taking a hit on the player's board. Returns a dictionary indicating hit/miss and if a ship was sunk.
        """
        if coor in self.boat_info["all_boats_coor"]:
            self.board[coor[0]][coor[1]] = "X"
            for boat_key, boat in self.boat_info["boats"].items():
                if coor in boat["pos"]:
                    boat["hits"] += 1
                    # Mark as sunk if all parts hit
                    if boat["hits"] == len(boat["pos"]):
                        boat["sunk"] = True
                        return {"hit": True, "sink": True, "ship": boat_key}
                    return {"hit": True, "sink": False, "ship": boat_key}
        else:
            self.board[coor[0]][coor[1]] = "M"
            return {"hit": False, "sink": False}


    def game_over_check(self):
        for boat in self.boat_info["boats"].values():
            if boat["hits"] < boat["length"]:
                return False
        return True

    def player_shoot(self, pos_coor:list):
        self.shooting_attemps.append(pos_coor)
        return pos_coor



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

    # def place_boats(self, boats:dict):
    #     for boat in boats:
    #         temp = []
    #         boat_type = boat["ship"]["type"]
    #         if boat_type not in self.boat_info:
    #             raise KeyError("Ship type not correct.")
    #         length = boat["ship"]["length"]
    #         direction = boat["ship"]["directon"]
    #         start = (boats["x"], boats["y"])
    #         if  direction == "vertical":
    #             for i in range(length):
    #                 temp.append([start[0] + i, start[1]])
    #                 self.boat_info["all_boats_coor"].append([start[0] + i, start[1]])
    #         else:
    #             for i in range(length):
    #                 temp.append([start[0], start[1] + i])
    #                 self.boat_info["all_boats_coor"].append([start[0], start[1] + i])
    #         self.boat_info[boat_type]["pos"] = temp.copy()
    #         self.boat_info[boat_type]["start"] = start
    #         self.boat_info[boat_type]["direction"] = direction

    def place_boats(self, boats: list[dict]):
        for boat in boats:
            temp = []
            boat_type = boat["type"]
            if boat_type not in self.boat_info["boats"]:
                raise KeyError("Invalid ship type.")
            length = boat["length"]
            direction = boat["direction"]
            start = (boat["x"], boat["y"])

            if direction == "vertical":
                for i in range(length):
                    coord = [start[1] + i, start[0]]
                    temp.append(coord)
                    self.boat_info["all_boats_coor"].append(coord)
            else:
                for i in range(length):
                    coord = [start[1], start[0] + i]
                    temp.append(coord)
                    self.boat_info["all_boats_coor"].append(coord)

            self.boat_info["boats"][boat_type]["pos"] = temp.copy()
            self.boat_info["boats"][boat_type]["start"] = start
            self.boat_info["boats"][boat_type]["direction"] = direction

    ###No need for a print function if there is a visual aspect.
    def print_board(self):
        print("    1    2    3    4    5    6    7    8    9    10")
        for i in range(len(self.board)):
            print(f"{self.board[i]}")

