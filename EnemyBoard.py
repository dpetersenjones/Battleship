from random import randint

class EnemyBoard:
    def __init__(self) -> None:
        self.board = []
        self.boat2_pos = []
        self.boat3_pos = []
        self.boat4_pos = []
        self.boat5_pos = []
        self.directions = [[0,1], [0,-1], [1, 0], [-1, 0]]
        self.all_boats_pos = []
        self.create_board()
        self.place_boats()

    def create_board(self):
        #Creating the board
        for _ in range(10):
            self.board.append([0]*10)
    def place_boats(self):
        #Get random starting position
        def get_start():
            x = randint(0,9)
            y = randint(0,9)
            if [y,x] in self.all_boats_pos:
                return get_start()
            else:
                return [y,x]
        #Creates the boat positioning
        def get_boat_pos(width):
            starting_pos = get_start()
            dir = self.directions[randint(0,3)]
            boat_coor = [starting_pos]
            switch = False
            curr_pos = starting_pos
            while len(boat_coor) < width:
                curr_pos = [curr_pos[0] + dir[0], curr_pos[1] + dir[1]]
                if curr_pos in self.all_boats_pos or curr_pos in boat_coor or curr_pos[0] < 0 or curr_pos[1] < 0 or curr_pos[0] > 9 or curr_pos[1] > 9:
                    if not switch:
                        switch = True
                        curr_pos = starting_pos
                        dir[0], dir[1] = 0 - dir[0], 0 - dir[1]
                    else:
                        return get_boat_pos(width)
                else:
                    boat_coor.append(curr_pos)
            return boat_coor
        #Boat 2 position
        self.boat2_pos = get_boat_pos(2)
        self.all_boats_pos = self.all_boats_pos + self.boat2_pos
        #Boat 3 position
        self.boat3_pos = get_boat_pos(3)
        self.all_boats_pos = self.all_boats_pos + self.boat3_pos
        #Boat 4 position
        self.boat4_pos = get_boat_pos(4)
        self.all_boats_pos = self.all_boats_pos + self.boat4_pos
        #Boat 5 position
        self.boat5_pos = get_boat_pos(5)
        self.all_boats_pos = self.all_boats_pos + self.boat5_pos
        for c in self.boat2_pos:
            self.board[c[0]][c[1]] = 2
        for c in self.boat3_pos:
            self.board[c[0]][c[1]] = 3
        for c in self.boat4_pos:
            self.board[c[0]][c[1]] = 4
        for c in self.boat5_pos:
            self.board[c[0]][c[1]] = 5
    def print_board(self):
        print("   A  B  C  D  E  F  G  H  I  J")
        for i in range(len(self.board)):
            print(f"{i} {self.board[i]}")


again = True
while again:
    test = EnemyBoard()
    test.print_board()
    print(test.boat2_pos)
    print(test.boat3_pos)
    print(test.boat4_pos)
    print(test.boat5_pos)
    response = input("Again? ")
    if response != "y":
        again = False