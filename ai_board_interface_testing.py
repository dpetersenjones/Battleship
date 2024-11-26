from enemy_board import EnemyBoard
from enemy_ai import EnemyAI
from player_board import PlayerBoard
import time

test = EnemyAI()
player = PlayerBoard()
board = EnemyBoard()

player.print_board()
player.placement()
player.print_board()

testing = True
response = False


while testing:
    print("Enemy's Board")
    board.print_board()
    time.sleep(.5)
    player_shot = player.player_shoot()
    player_check = board.taking_a_hit(player_shot)
    if player_check[0] == True:
        print("Hit!")
        if player_check[1] == True:
            print("And sink!")
            time.sleep(.5)
    print("Enemy's board")
    print(board.print_board())
    time.sleep(1)

    if not response:
        next_hit = test.shoot()
        print(f"Firing at {next_hit}")
        check = player.take_hit(next_hit)
        if check[0]:
            print("Hit")
        response = test.response(next_hit, check[0], check[1])
    else:
        print(f"Firing at {response}")
        check = player.take_hit(response)
        if check[0]:
            print("Hit")
        response = test.response(response, check[0], check[1])
    for x in test.attempted_coor:
        if 0 <= x[0] <= 9 or 0 <= x[1] <= 9:
            pass
        else:
            print("Error")
    #print(test.attempted_coor)
    print("Your board")
    player.print_board()
    

    r = input("Stop? ")
    if r == "y" or board.check_game_over():
        print("Game is finished")
        testing = False



