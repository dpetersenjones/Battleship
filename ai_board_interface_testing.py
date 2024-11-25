from enemy_board import EnemyBoard
from enemy_ai import EnemyAI
import time

test = EnemyAI()


board = EnemyBoard()

testing = True
response = False
board.print_board()

while testing:
    if not response:
        next_hit = test.shoot()
        print(f"Firing at {next_hit}")
        check = board.taking_a_hit(next_hit)
        if check[0]:
            print("Hit")
        response = test.response(next_hit, check[0], check[1])
    else:
        print(f"Firing at {response}")
        check = board.taking_a_hit(response)
        if check[0]:
            print("Hit")
        response = test.response(response, check[0], check[1])
    print(f"Next hit is {response}")
    print(test.attempted_coor)
    board.print_board()
    

    r = input("Stop? ")
    if r == "y":
        testing = False
