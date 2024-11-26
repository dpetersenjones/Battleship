class PlayerBoard:
    def __init__(self) -> None:
        self.translate = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7,"I":8, "J":9}
        self.translate2 = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J"}
        self.all_boats_coor = []
        self.board = []
        self.boat2_pos = []
        self.boat2_hits = 0
        self.boat3_pos = []
        self.boat3_hits = 0
        self.boat4_pos = []
        self.boat4_hits = 0
        self.boat5_pos = []
        self.boat5_hits = 0
        self.create_board()


    def create_board(self):
        #Creating the board
        for _ in range(10):
            self.board.append(["0"]*10)

    
    def placement(self):
        def get_placement(shipsize):
            start = input("Where do you want to start you ship? ")
            start_coor = translator(start)
            while start_coor[0] == -1:
                start = input("That isn't an acceptable position. Please try again like A1. ")
                start_coor = translator(start)
            orientation = input("Do you want it to be (h)orizontal or (v)ertical? ")
            while orientation.lower() != "v" and orientation.lower() != "h":
                print(orientation)
                print(orientation.lower() != "v")
                print(orientation.lower() != "h")
                orientation = input("Please use v or h. ")
            pos = []
            pos.append(start_coor)
            if orientation == "h":
                for i in range(1, shipsize):
                    if not check([start_coor[0], start_coor[1] + i]):
                        print("This ship position won't work, please try again.")
                        return get_placement(shipsize)
                    pos.append([start_coor[0], start_coor[1]+i])
            elif orientation == "v":
                for i in range(1, shipsize):
                    if not check([start_coor[0] + i, start_coor[1]]):
                        print("This ship position won't work, please try again.")
                        return get_placement(shipsize)
                    pos.append([start_coor[0] + i, start_coor[1]])
            return pos


        def translator(phrase):
            answer = []
            print(phrase[0])
            print(phrase[0].upper() == "A")
            if phrase[0].upper() not in self.translate:
                return [-1, -1]
            answer.append(self.translate[phrase[0].upper()])
            #print(phrase[1:])
            try:
                if 0 <= int(phrase[1:]) - 1 <= 9:
                    #print(phrase[1])
                    answer.append(int(phrase[1:]) - 1)
            except:
                #print("Here 1")
                return [-1, -1]
            if answer in self.all_boats_coor:
                #print("Here 2")
                return [-1, -1]
            return answer
        


        def check(pos):
            if pos[0] == False and pos[1] == False:
                return False
            if pos in self.all_boats_coor:
                return False
            for n in pos:
                if n < 0 or n > 9:
                    return False
            return True

        #Boat 2 placement
        print("Boat 2")
        self.boat2_pos = get_placement(2)
        self.all_boats_coor += self.boat2_pos
        for c in self.boat2_pos:
            self.board[c[0]][c[1]] = "2"
        self.print_board()
        #Boat 3 placement
        print("Boat 3")
        self.boat3_pos = get_placement(3)
        self.all_boats_coor += self.boat3_pos
        for c in self.boat3_pos:
            self.board[c[0]][c[1]] = "3"
        self.print_board()
        #Boat 4 placement
        print("Boat 4")
        self.boat4_pos = get_placement(4)
        self.all_boats_coor += self.boat4_pos
        for c in self.boat4_pos:
            self.board[c[0]][c[1]] = "4"
        self.print_board()
        #Boat 5 Placement
        print("Boat 5")
        self.boat5_pos = get_placement(5)
        self.all_boats_coor += self.boat5_pos
        for c in self.boat5_pos:
            self.board[c[0]][c[1]] = "5"
        self.print_board()


    def print_board(self):
        print("    1    2    3    4    5    6    7    8    9    10")
        for i in range(len(self.board)):
            print(f"{self.translate2[i]} {self.board[i]}")


test = PlayerBoard()
test.print_board()
test.placement()
test.print_board()