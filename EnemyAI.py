from random import randint

class EnemyAI():
    def __init__(self) -> None:
        self.attempted_coor = []

        
    def shoot(self):
            x = randint(0,9)
            y = randint(0,9)
            if [y,x] in self.attempted_coor:
                return self.shoot()
            else:
                return [y,x]