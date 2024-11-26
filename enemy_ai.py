from random import randint

class EnemyAI:
    def __init__(self) -> None:
        self.attempted_coor = []
        self.directions = [[0,1], [0,-1], [1, 0], [-1, 0]]
        self.last_hit = False
        self.last_dir = False
        self.curr_hit_streak = []
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

                #The first hit is positive
        def first_hit():
            self.last_dir = self.directions[randint(0,3)]
            next_hit = [(pos[0] + self.last_dir[0]), (pos[1] + self.last_dir[1])]
            if next_hit in self.attempted_coor or next_hit[0] < 0 or next_hit[0] > 9 or next_hit[1] < 0 or next_hit[1] > 9:
                return first_hit()
            return next_hit
        
        #Continues to fire in the same direction
        # if that hit is has already been attempted
        # then it changes to the change_direction function
        def continue_direction():
            next_hit = [(pos[0] + self.last_dir[0]), (pos[1] + self.last_dir[1])]
            if next_hit in self.attempted_coor or next_hit[0] < 0 or next_hit[0] > 9 or next_hit[1] < 0 or next_hit[1] > 9:
                return change_direction()
            return next_hit
        
        #If it is on the first hit, it tries the other direction
        #However, if it is the end of a line and the ship hasn't sucken, then it checks the other direction
        #If the other direction doesn't come up with a sinking status, then it does a dfs
        def change_direction():
            next_hit = [0, 0]
            next_hit[0] = self.curr_hit_streak[-1][0]
            next_hit[1] = self.curr_hit_streak[-1][1]
            if len(self.curr_hit_streak) <= 1:
                if [next_hit[0] + (0 - self.last_dir[0]), next_hit[1] + (0 - self.last_dir[1])] not in self.attempted_coor:
                    self.last_dir[0] = 0 - self.last_dir[0]
                    self.last_dir[1] = 0 - self.last_dir[1]
                    if next_hit[0] + (self.last_dir[0]) >= 0 and next_hit[0] + (self.last_dir[0]) <= 9 and next_hit[1] + (self.last_dir[1]) >= 0 and next_hit[1] + (self.last_dir[1]) <= 9:
                        return [next_hit[0] + (self.last_dir[0]), next_hit[1] + (self.last_dir[1])]
                for d in self.directions:
                    if [next_hit[0] + d[0], next_hit[1] + d[1]] not in self.attempted_coor and next_hit[0] + d[0] >= 0 and next_hit[0] + d[0] <= 9 and next_hit[1] + d[1] >= 0 and next_hit[1] + d[1] <=9:
                        self.last_dir = d
                        return [next_hit[0] + d[0], next_hit[1] + d[1]]
            else:
                self.last_dir[0] = 0 - self.last_dir[0]
                self.last_dir[1] = 0 - self.last_dir[1]
                counter = 0
                while next_hit in self.curr_hit_streak: # and pos in self.attempted_coor:
                    next_hit[0] = next_hit[0] + self.last_dir[0]
                    next_hit[1] = next_hit[1] + self.last_dir[1]
                    counter += 1
                    if counter == 10:
                        return False
                if next_hit in self.attempted_coor or next_hit[0] < 0 or next_hit[0] > 9 or next_hit[1] < 0 or next_hit[1] > 9:
                    self.dfs = True
                    return dfs()
                return next_hit
            
        #Common dfs, basically checks around all all current hits
        def dfs():
            for p in self.curr_hit_streak:
                for d in self.directions:
                    if [p[0] + d[0], p[1] + d[1]] not in self.attempted_coor and 0 <= p[0] + d[0] <= 9 and 0 <= p[1] + d[1] <= 9:
                        return [p[0] + d[0], p[1] + d[1]]

        if hit:
            
            self.curr_hit_streak.append(pos)
        if not hit and not self.last_hit:
            print("Miss")
            return False
        elif hit and boat:
            print("Ship sunk")
            self.last_hit = False
            self.last_dir = False
            self.dfs = False
            self.curr_hit_streak = []
            return False
        elif hit and not self.last_hit:
            #print("First Hit")
            self.last_hit = pos
            next_hit = first_hit()
        elif hit and self.last_hit:
            #print("Continue Direction")
            self.last_hit = pos
            next_hit = continue_direction()
        elif self.dfs:
            #print("DFS")
            self.last_hit = pos
            next_hit = dfs()
        elif not hit and self.last_hit:
            #print("Changing Direction")
            next_hit = change_direction()
        else:
            #print("In else")
            next_hit = dfs()


        if next_hit in self.attempted_coor:
            print("Something Fucked up")
            return False
        self.attempted_coor.append(next_hit)
        return next_hit