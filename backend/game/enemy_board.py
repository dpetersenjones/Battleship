from random import randint
import json

class EnemyBoard:
    """
    This keeps track of the enemy board. There is a seperate AI for the enemy's shot placement.
    """
    def __init__(self) -> None:
        self.board = []
        self.boat_info = {
            "all_boats_coor": [],
            "boats": {
                "destroyer": {
                    "pos":[],
                    "hits":0,
                    "length":2,
                    #TODO: Do I need Directions?
                    "direction":None,
                    "start":None,
                },
                "submarine": {
                    "pos":[],
                    "hits":0,
                    "length":3,
                    "direction":None,
                    "start":None,
                },
                "cruiser": {
                    "pos":[],
                    "hits":0,
                    "length":3,
                    "direction":None,
                    "start":None,
                },
                "battleship": {
                    "pos":[],
                    "hits":0,
                    "length":4,
                    "direction":None,
                    "start":None,
                },
                "carrier": {
                    "pos":[],
                    "hits":0,
                    "length":5,
                    "direction":None,
                    "start":None,
            },}
        }
        self.directions = [[0,1], [1, 0]]
        self.create_board()
        self.place_boats()
        
    def serialize(self):
        """
        Used to serialize the info, so it can be saved easier.
        """
        return json.dumps({
            "boats": self.boat_info,
        })
        
    @classmethod
    def deserialize(cls, info):
        new_class = cls()
        new_class.boat_info = info.get("boats", {})
        return new_class

    def check_game_over(self) -> bool:
        for boat in self.boat_info["boats"].values():
            if boat["hits"] < boat["length"]:
                return False
        return True

        
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
                        return {"hit": True, "sink": True, "ship": boat}
                    return {"hit": True, "sink": False, "ship": boat}
        else:
            self.board[coor[0]][coor[1]] = "M"
            return {"hit": False, "sink": False}


    def create_board(self):
        #Creating the board, won't be needed
        for _ in range(10):
            self.board.append(["0"]*10)

    def place_boats(self) -> None:
        #Get random starting position
        def get_start():
            x = randint(0,9)
            y = randint(0,9)
            if [y,x] in self.boat_info["all_boats_coor"]:
                return get_start()
            else:
                return [y,x]
        #Creates the boat positioning
        def get_boat_pos(width) -> dict:
            starting_pos = get_start()
            dir = self.directions[randint(0,1)]
            final_direction = "horizontal" if dir == self.directions[0] else "vertical"
            boat_coor = [starting_pos]
            switch = False
            curr_pos = starting_pos
            while len(boat_coor) < width:
                curr_pos = [curr_pos[0] + dir[0], curr_pos[1] + dir[1]]
                if curr_pos[0] < starting_pos[0] or curr_pos[1] < starting_pos[1]:
                    starting_pos = curr_pos
                if curr_pos in self.boat_info["all_boats_coor"] or curr_pos in boat_coor or curr_pos[0] < 0 or curr_pos[1] < 0 or curr_pos[0] > 9 or curr_pos[1] > 9:
                    if not switch:
                        switch = True
                        curr_pos = starting_pos
                        dir[0], dir[1] = 0 - dir[0], 0 - dir[1]
                    else:
                        return get_boat_pos(width)
                else:
                    boat_coor.append(curr_pos)
            return {"pos":boat_coor, "direction":final_direction, "start":starting_pos}
        
        # Destroyer
        destroyer_result = get_boat_pos(2)
        self.boat_info["boats"]["destroyer"]["pos"] = destroyer_result["pos"]
        self.boat_info["boats"]["destroyer"]["start"] = destroyer_result["start"]
        self.boat_info["boats"]["destroyer"]["direction"] = destroyer_result["direction"]
        self.boat_info["all_boats_coor"] += destroyer_result["pos"]

        # Submarine
        submarine_result = get_boat_pos(3)
        self.boat_info["boats"]["submarine"]["pos"] = submarine_result["pos"]
        self.boat_info["boats"]["submarine"]["start"] = submarine_result["start"]
        self.boat_info["boats"]["submarine"]["direction"] = submarine_result["direction"]
        self.boat_info["all_boats_coor"] += submarine_result["pos"]

        # Cruiser
        cruiser_result = get_boat_pos(3)
        self.boat_info["boats"]["cruiser"]["pos"] = cruiser_result["pos"]
        self.boat_info["boats"]["cruiser"]["start"] = cruiser_result["start"]
        self.boat_info["boats"]["cruiser"]["direction"] = cruiser_result["direction"]
        self.boat_info["all_boats_coor"] += cruiser_result["pos"]

        # Battleship
        battleship_result = get_boat_pos(4)
        self.boat_info["boats"]["battleship"]["pos"] = battleship_result["pos"]
        self.boat_info["boats"]["battleship"]["start"] = battleship_result["start"]
        self.boat_info["boats"]["battleship"]["direction"] = battleship_result["direction"]
        self.boat_info["all_boats_coor"] += battleship_result["pos"]

        # Carrier
        carrier_result = get_boat_pos(5)
        self.boat_info["boats"]["carrier"]["pos"] = carrier_result["pos"]
        self.boat_info["boats"]["carrier"]["start"] = carrier_result["start"]
        self.boat_info["boats"]["carrier"]["direction"] = carrier_result["direction"]
        self.boat_info["all_boats_coor"] += carrier_result["pos"]

        
    def print_board(self) -> None:
        #Won't be needed
        print("    1    2    3    4    5    6    7    8    9    10")
        for i in range(len(self.board)):
            print(f"{self.translate[i]} {self.board[i]}")
