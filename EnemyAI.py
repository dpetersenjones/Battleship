from random import randint

class EnemyAI:
    def __init__(self) -> None:
        self.attempted_coor = []
        self.directions = [[0,1], [0,-1], [1, 0], [-1, 0]]
        self.last_hit = False
        self.last_dir = False

    def shoot(self, pos=False):
        if self.last_hit != False:
            pass
        elif pos != False:
            return pos
        else:
            x = randint(0,9)
            y = randint(0,9)
            if [y,x] in self.attempted_coor:
                return self.shoot()
            else:
                self.attempted_coor.append([y,x])
                return [y,x]
    
    def response(self, pos, hit=False, boat=False):
        if hit and boat:
            self.last_hit =False
            self.last_dir = False
        elif hit and not boat and self.last_dir != False:
            self.last_hit = pos
            new_pos = [pos[0]+self.last_dir[0], pos[1]+self.last_dir[1]]


        elif not hit and self.last_hit != False and self.last_dir != False:
            self.last_dir += 1
            new_pos = [self.last_hit[0]+self.directions[self.last_dir][0], self.last_hit[1]+self.directions[self.last_dir][0]]