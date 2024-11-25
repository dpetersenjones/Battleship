from random import randint

class EnemyAI:
    def __init__(self) -> None:
        self.attempted_coor = []
        self.directions = [[0,1], [0,-1], [1, 0], [-1, 0]]
        self.last_hit = False
        self.last_dir = False
        self.curr_hit_streak = []
        self.dir_tried_on_attempt = []
        self.dfs = False

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
        if hit == True:
            self.last_hit = pos








        #The first hit is positive
        def first_hit():
            self.last_dir = self.directions[randint(0,3)]
            next_hit = [(pos[0] + self.directions[0]), (pos[1] + self.directions[1])]
            if next_hit in self.attempted_coor:
                return first_hit()
            self.dir_tried_on_attempt.append(self.last_dir)
            return next_hit
        
        #Continues to fire in the same direction
        # if that hit is has already been attempted
        # then it changes to the change_direction function
        def continue_direction():
            next_hit = [(pos[0] + self.directions[0]), (pos[1] + self.directions[1])]
            if next_hit in self.attempted_coor:
                return change_direction()
            return next_hit
        
        def change_direction():
            if len(self.curr_hit_streak) <= 1:
                if [pos[0] + (0 - self.last_dir[0]), pos[1] + (0 - self.last_dir[1])] not in self.attempted_coor:
                    return [pos[0] + (0 - self.last_dir[0]), pos[1] + (0 - self.last_dir[1])]
                for d in self.directions:
                    if [pos[0] + (0 - d[0]), pos[1] + (0 - d[1])] not in self.attempted_coor:
                        return [pos[0] + (0 - self.last_dir[0]), pos[1] + (0 - self.last_dir[1])]
            else:
                self.last_dir[0] = 0 - self.last_dir[0]
                self.last_dir[1] = 0 - self.last_dir[1]
                next_hit = pos
                while pos in self.curr_hit_streak and pos in self.attempted_coor:
                    pos[0] = pos[0] + self.last_dir[0]
                    pos[1] = pos[1] + self.last_dir[1]
                if pos in self.attempted_coor:
                    self.dfs = True
                    return dfs()
                return pos