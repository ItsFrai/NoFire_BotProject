
import random
import math
import time

class Ship():
    def __init__(self):
        try:
            self.D = int(input("Enter D x D Dimension: "))
        except ValueError:
            print("Needs to be an int")
            exit()

        # Up, down, left, right
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        self.ship = [['X'] * self.D for _ in range(self.D)]

        # Initialize bot and leak positions
        self.dead_ends = []
        self.bot = (-1, -1)
        self.leak = (-1, -1)
        self.k_val = 0
        self.actions_counter = 0
        self.open_cells_list = [()]
        self.second_leak = None
        
    def __repr__(self):
        ship_str = ""
        for x in range(self.D):
            for y in range(self.D):
                cell = self.ship[x][y]
                if (x >= self.bot[0] - self.k_val) and (x <= self.bot[0] + self.k_val) and \
                (y >= self.bot[1] - self.k_val) and (y <= self.bot[1] + self.k_val):
                    if (x, y) != self.bot and cell != "X":
                        ship_str += '[-]'
                    else:
                        ship_str += '[' + cell + ']'
                else:
                    ship_str += '[' + cell + ']'
            ship_str += '\n'
        return ship_str

    # given a cordinate and what you're looking for, it will return number of neighbors next to an open cells
    def count_neighbors(self, x: int, y: int, item: str) -> int:
        count = 0
        for move_x, move_y in self.directions:
            new_x, new_y = x + move_x, y + move_y
            if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] == item:
                count += 1
        return count

    def generate_ship(self) -> None:
        # set of all possible square to open
        open_possibilities = set()

        #Choose a square in the interior to ‘open’ at random.
        rand_x_coord = random.randint(0, self.D-1)
        rand_y_coord = random.randint(0, self.D-1)
        self.ship[rand_x_coord][rand_y_coord] = 'O'

        open_possibilities.add((rand_x_coord, rand_y_coord))

        while open_possibilities:
            curr_x, curr_y = open_possibilities.pop()
            self.ship[curr_x][curr_y] = 'O'

            for x, y in self.directions:
                new_x, new_y = x + curr_x, y + curr_y
                # if within the ship dimensions and is blocked
                if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] == 'X':
                    # Check if the square is not already in open_possibilities
                    if (new_x, new_y) in open_possibilities:
                        open_possibilities.remove((new_x, new_y))
                        self.ship[new_x][new_y] = '-' # Not able to open
                    else:
                        open_possibilities.add((new_x,new_y))

        # now get intial num of deadends
        for x in range(self.D):
            for y in range(self.D):
                if self.ship[x][y] == 'O' and self.count_neighbors(x, y, "O") == 1:
                    self.dead_ends.append((x, y))

        half = len(self.dead_ends) // 2

        # make approximately half of deadends non dead ends
        while len(self.dead_ends) > half:
            curr_x, curr_y = random.choice(self.dead_ends)
            self.dead_ends.remove((curr_x,curr_y))

            # Remove one of the sides arbitrarily from the dead ends
            for x, y in random.sample(self.directions, len(self.directions)):
                new_x, new_y = x + curr_x, y + curr_y
                if  0 <= new_x < self.D and 0 <= new_y < self.D and (self.ship[new_x][new_y] in ['X', '-']):
                    self.ship[new_x][new_y] = 'O'
                    break

            new_dead_ends = [] # new deadend array to see how many deadends are removed
 
            # recompute the num of deadends
            for x in range(self.D):
                for y in range(self.D):
                    if self.ship[x][y] == 'O' and self.count_neighbors(x, y, "O") == 1:
                        new_dead_ends.append((x,y))
 
            self.dead_ends = new_dead_ends.copy()

            for x in range(self.D):
                for y in range(self.D):
                    if self.ship[x][y] == '-':
                        self.ship[x][y] = 'X' 

            while self.bot == (-1, -1) or self.leak == (-1, -1):
                rand_x_coord = random.randint(0, self.D - 1)
                rand_y_coord = random.randint(0, self.D - 1)

                if self.bot == (-1, -1):
                    self.ship[rand_x_coord][rand_y_coord] = self.colored_block('c')
                    self.bot = (rand_x_coord, rand_y_coord)
                elif self.leak == (-1, -1):


                    # Ensure the leak is at least k_val + 1 cells away from the square
                    while True:
                        leak_x = random.randint(0, self.D - 1)
                        leak_y = random.randint(0, self.D - 1)
                        if (abs(leak_x - self.bot[0]) > self.k_val + 1 or abs(leak_y - self.bot[1]) > self.k_val + 1):
                            self.ship[leak_x][leak_y] = self.colored_block('g')
                            self.leak = (leak_x, leak_y)
                            break
        for x in range(self.D):
            for y in range(self.D):
                if self.ship[x][y] == 'O' or (x,y) == self.leak:
                    self.open_cells_list.append((x,y))

    def colored_block(self, color):
        color_codes = {
            'r': '\033[31m',  # Red
            'g': '\033[32m',  # Green
            'b': '\033[34m',  # Blue
            'y': '\033[33m',  # Yellow
            'm': '\033[35m',  # Magenta
            'c': '\033[36m',  # Cyan
            'w': '\033[37m',  # White
        }

        reset_color = '\033[0m'

        if color in color_codes:
            return f"{color_codes[color]}\u2588{reset_color}"
        else:
            return f"Invalid color code: {color}"

        # Finds the shortest path from the start coordinate to the goal coordinate, considering constraints.
        # Returns the length of the shortest path or -1 if no path is found.
    def find_shortest_path(self, start: tuple, end: tuple, constraints: list = []) -> list:  
        fringe = dict()
        fringe.update({start: math.dist([start[0], start[1]], [end[0], end[1]])})
        parent = {}
        visited = []

        sorted_list = [(start[0], start[1])]
        while fringe:
            smallest_key = sorted_list.pop(0)
            curr_x, curr_y = smallest_key
            fringe.pop(smallest_key)

            # If button is found
            if curr_x == end[0] and curr_y == end[1]:
                path = [(curr_x, curr_y)]
                while smallest_key in parent and smallest_key != start:
                    path.insert(0, smallest_key)
                    smallest_key = parent[smallest_key]
                return path
            
            for x, y in self.directions:
                new_x, new_y = x + curr_x, y + curr_y
                # all of the neighbours inside this if statement are valid neighbours.
                if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] != 'X' and (new_x, new_y) not in constraints and (new_x, new_y) not in visited:
                    edist = math.dist([new_x, new_y], [end[0], end[1]])
                    fringe.update({(new_x, new_y): edist})
                    visited.append((new_x,new_y))
                    parent[(new_x, new_y)] = smallest_key

            sorted_list = [k for k, _ in sorted(fringe.items(), key=lambda item: item[1])]
        return None

    # Senses if the button is within the radius of the bot
    def sense_action(self):
        self.actions_counter += 1
        if any(cell == self.leak for cell in self.get_detection_square()):
            return True

        else:
            return False
    def sense_action_for_two(self):

        self.actions_counter += 1
        detection_square = self.get_detection_square()
        leaks_detected = [cell for cell in detection_square if cell == self.leak or cell == self.second_leak]
        if leaks_detected:  
            return True
        else:
            return False
        
    def sense_action_bothleaks(self):
        self.actions_counter += 1
        detection_square = self.get_detection_square()
        leaks_detected = [cell for cell in detection_square if cell == self.leak or cell == self.second_leak]
        return len(leaks_detected) == 2
        
        
    # Obtains the radius of the bot within ship bounds
    def get_detection_square(self):
        detection_square = []
        for x in range(self.bot[0] - k_val, self.bot[0] + k_val + 1):
            for y in range(self.bot[1] - k_val, self.bot[1] + k_val + 1):
                if 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                    detection_square.append((x, y))
        return detection_square
    
    def update_mat_enter(self, prob_mat) -> list[list[float]]:
        temp_mat = prob_mat
        sum_prob = 0
        for x in range(self.D):
            for y in range(self.D):
                sum_prob += prob_mat[x][y]
        
        print(sum_prob)

        for x in range(self.D):
            for y in range(self.D):
                prob_mat[x][y] = prob_mat[x][y] / sum_prob
        
        return prob_mat

    
            

    
    def run_bot_1(self):
        # Initialize a set to keep track of visited locations
        visited = set()

        while self.bot != self.leak:
            if self.sense_action():
                print("Leak found")
                # Leak is in the detection square, search for it
                for x in range(self.bot[0] - self.k_val, self.bot[0] + self.k_val + 1):
                    for y in range(self.bot[1] - self.k_val, self.bot[1] + self.k_val + 1):
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D  and self.ship[x][y] != 'X':
                            print(f"Moving to location ({x}, {y})")
                            visited.add((x, y))
                            self.ship[self.bot[0]][self.bot[1]] = 'O'
                            self.bot = (x, y)
                            self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')  
                        
                            if self.bot == self.leak:
                                print("Congratulations, you found the leak!")
                                print(f"Total amount of actions = {ship.actions_counter}")  
                                return

            else:
                print("Leak not found")
                # Leak is not in the detection square, move the bot
                possible_moves = [(self.bot[0] + dx, self.bot[1] + dy) for dx, dy in self.directions]
                valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X']
                unvisited_moves = [move for move in valid_moves if move not in visited]

                if unvisited_moves:
                    # Choose an unvisited location to move to
                    new_location = random.choice(unvisited_moves)
                    print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                    visited.add(new_location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = new_location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')  

                    self.actions_counter += 1
                                        
                else:
                    # All neighboring cells are visited; backtrack to a previous location
                    prev_location = self.bot
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = visited.pop()
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    print(f"Backtracking to location ({self.bot[0]}, {self.bot[1]})")
                    distance_traveled = int(math.sqrt((self.bot[0] - prev_location[0])**2 + (self.bot[1] - prev_location[1])**2))
                    self.actions_counter += distance_traveled
            print(self)
            
       

    
        #while self.leak != self.bot
            #do a sense check and see if it is in the square
                # if it is, then iterate through all the -'s within the bot and once you find the leak print you won and break
            #if it is not in the square after sensing, move the bot to any other location that wasn't visited in the grid based on its location, 
            # meaning up 1 down 1 left 1 or right 1. from here, go back up and do the while loop again, and then use the sense again until you find the leak


    def run_bot_2(self):
        # Initialize a set to keep track of visited locations
        visited = set()

        while self.bot != self.leak:
            # Sense only if it's been a while since the last sense or move
            if self.sense_action():
                for x in range(self.bot[0] - self.k_val, self.bot[0] + self.k_val + 1):
                    for y in range(self.bot[1] - self.k_val, self.bot[1] + self.k_val + 1):
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                            print(f"Moving to location ({x}, {y})")
                            visited.add((x, y))
                            self.ship[self.bot[0]][self.bot[1]] = 'O'
                            self.bot = (x, y)
                            self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')  
                        
                            if self.bot == self.leak:
                                print("Congratulations, you found the leak!")
                                print(f"Total amount of actions = {ship.actions_counter}")  
                                return
            # Calculate the direction towards the leak
            else:
                detection_square = self.get_detection_square()
                constraints = visited | {(x, y) for x in range(self.D) for y in range(self.D) if self.ship[x][y] == 'X'}
                shortest_path = None
                for location in detection_square:
                    path = self.find_shortest_path(start =location, end = self.leak)
                    if path and (shortest_path is None or len(path) < len(shortest_path)):
                        shortest_path = path

                # Move to the next location on the shortest path
                new_location = shortest_path[0]
                print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                visited.add(self.bot)
                self.ship[self.bot[0]][self.bot[1]] = 'O'
                self.bot = new_location
                self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                self.actions_counter += 1
                if (self.bot == self.leak):
                    print("Congrats you found the leak!")
                    return
               
            print(self)
            
            
        #sense_action (for probabilistic determination)
        #compute the probability of receiving a beep
            #based on that probability, re-initilize the probability matrix to take the new beep/no-beep probability
                #this is based on P(leak in matrix [x][y](the specific position in the interation for loop) | beep in current position) 
                # or P(leak in matrix [x][y] | NO beep in current position)
                # this might be trick because you have to find the shortest path (make another helper method for this, you can use the bfs algo from the last project but modified)
                # from the bot to the leak in order to get the D value for the probability (save this value as it might be used later)


    def run_bot_3(self, alpha):
        #create a probability matrix the same size of the ship
        #set the bot's initial position's probability to 0
        #initilize the matrix to be (1 / open spots on the ship) for all of the open places but the location of the bot
        #create a counter for the sense action and the move action
        
        # leak probability matrix
        leak_prob = [[1/ self.open_cells] * self.D for _ in range(self.D)]
        
        bot_x, bot_y = self.bot
        leak_prob[bot_x][bot_y] = 0
        
        dist_matrix = [[-1 * self.D for _ in range(self.D)] for _ in range(self.D)]

        # first compute each location's distance to the leak, if no path/is a X, return -1
        for i in range(self.D):
            for j in range(self.D):
                if self.ship[i][j] != 'X':
                    start = (i, j)
                    steps_to_leak = self.find_shortest_path(start=start, end=self.leak)
                    # print(len(steps_to_leak))
                    dist_matrix[i][j] = (len(steps_to_leak) - 1)
                    print(dist_matrix[i][j])
            print()

        while self.bot != self.leak:
            bot_x, bot_y = self.bot
            # get the distance of the bot to the leak
            bot_leak_steps = dist_matrix[bot_x][bot_y]

            beep_prob = math.exp(-alpha * (bot_leak_steps -1))
            random_val = random.random()
            # if there is a beep
            if beep_prob > random_val:
                # update each of the open cell possibilities via:
                # p_leak[x][y] = p_beep[x][y] * p_leak[x][y]/ p_beep |[bot.x][bot.y]
                # prob of leak = that matrix prob * curr prob of leak at that location / prob of leak at bot location
                for i in range(self.D):
                    for j in range(self.D):
                        if self.ship[i][j] != 'X':
                            step_dist = steps_to_leak[i][j]
                            leak_prob[i][j] = leak_prob[i][j] * math.exp(-alpha * (step_dist - 1)) / beep_prob
                            
                self.actions_counter += 1
            else:
               for i in range(self.D):
                    for j in range(self.D):
                        if self.ship[i][j] != 'X':
                            step_dist = steps_to_leak[i][j]
                            #todo: THIS FORMULA BELOW IS WRONG CHANGE IT AFTER
                            leak_prob[i][j] = leak_prob[i][j] * math.exp(-alpha * (step_dist - 1)) / beep_prob
            
            

            #for each (open) direction that the bot can move, organize their probabilities in descending order
                #select the one that has the highest probability of containing the leak for the new position of the Bot
                #move++
                
        #theres an edge case where you might get stuck at a dead end with probabilities of 0 all around you, if this happens, then run the shortest path from your current
        #position to the highest probability position adjacent to the 0s 
        # this should give you a path with X amounts of Steps
        # move += X; 
        
        pass

    def run_bot_5(self): 
        
        while True:
            new_x = random.randint(0, self.D - 1)
            new_y = random.randint(0, self.D - 1)
            if (new_x != self.leak[0] or new_y != self.leak[1]) and (new_x != self.bot[0] or new_y != self.bot[1]) and self.ship[new_x][new_y] != 'X':
                break

        # Add the second leak to the ship grid
        self.ship[new_x][new_y] = self.colored_block('g')
        self.second_leak = (new_x, new_y)

        visited = set()
        leaks_found = 0  # To keep track of the number of leaks found

        while leaks_found < 2:
            if self.sense_action_for_two():
                print("Leak found")
                # Leak is in the detection square, search for it
                for x in range(self.bot[0] - self.k_val, self.bot[0] + self.k_val + 1):
                    for y in range(self.bot[1] - self.k_val, self.bot[1] + self.k_val + 1):
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                            print(f"Moving to location ({x}, {y})")
                            visited.add((x, y))
                            self.ship[self.bot[0]][self.bot[1]] = 'O'
                            self.bot = (x, y)
                            self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                            
                            if leaks_found == 2:
                                print("You won")
                                print(self.actions_counter)
                                return
                            
                            if self.bot == self.leak:
                                self.ship[self.leak[0]][self.leak[1]] = 'O'
                                self.leak = None
                                print("first leak found")
                                leaks_found += 1
                            elif self.bot == self.second_leak:
                                print("second leak found")
                                self.ship[self.second_leak[0]][self.second_leak[1]] = 'O'
                                self.second_leak = None
                                leaks_found += 1
                                
            else:
                print("Leak not found")
                # Leak is not in the detection square, move the bot
                possible_moves = [(self.bot[0] + dx, self.bot[1] + dy) for dx, dy in self.directions]
                valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X']
                unvisited_moves = [move for move in valid_moves if move not in visited]

                if unvisited_moves:
                    # Choose an unvisited location to move to
                    new_location = random.choice(unvisited_moves)
                    print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                    visited.add(new_location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = new_location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    self.actions_counter += 1

                else:
                    # All neighboring cells are visited; backtrack to a previous location
                    prev_location = self.bot
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = visited.pop()
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    print(f"Backtracking to location ({self.bot[0]}, {self.bot[1]})")
                    distance_traveled = int(math.sqrt((self.bot[0] - prev_location[0])**2 + (self.bot[1] - prev_location[1])**2))
                    self.actions_counter += distance_traveled
            print(self)

    
    def run_bot_6(self):
        while True:
            new_x = random.randint(0, self.D - 1)
            new_y = random.randint(0, self.D - 1)
            if (new_x != self.leak[0] or new_y != self.leak[1]) and (new_x != self.bot[0] or new_y != self.bot[1]) and self.ship[new_x][new_y] != 'X':
                break

        # Add the second leak to the ship grid
        self.ship[new_x][new_y] = self.colored_block('g')
        self.second_leak = (new_x, new_y)

        visited = set()
        leaks_found = 0  # To keep track of the number of leaks found

        while leaks_found < 2:
            
            if self.sense_action_bothleaks():
                print("both leaks in detection square")
                
            elif self.sense_action_for_two():
                print("Leak found")
                # Leak is in the detection square, search for it
                for x in range(self.bot[0] - self.k_val, self.bot[0] + self.k_val + 1):
                    for y in range(self.bot[1] - self.k_val, self.bot[1] + self.k_val + 1):
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                            print(f"Moving to location ({x}, {y})")
                            visited.add((x, y))
                            self.ship[self.bot[0]][self.bot[1]] = 'O'
                            self.bot = (x, y)
                            self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                            
                            if leaks_found == 2:
                                print("You won")
                                print(self.actions_counter)
                                return
                            
                            if self.bot == self.leak:
                                self.ship[self.leak[0]][self.leak[1]] = 'O'
                                self.leak = None
                                print("first leak found")
                                leaks_found += 1
                            elif self.bot == self.second_leak:
                                print("second leak found")
                                self.ship[self.second_leak[0]][self.second_leak[1]] = 'O'
                                self.second_leak = None
                                leaks_found += 1
                                
            else:
                print("Leak not found")
                # Leak is not in the detection square, move the bot
                possible_moves = [(self.bot[0] + dx, self.bot[1] + dy) for dx, dy in self.directions]
                valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X']
                unvisited_moves = [move for move in valid_moves if move not in visited]

                if unvisited_moves:
                    # Choose an unvisited location to move to
                    new_location = random.choice(unvisited_moves)
                    print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                    visited.add(new_location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = new_location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    self.actions_counter += 1

                else:
                    # All neighboring cells are visited; backtrack to a previous location
                    prev_location = self.bot
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = visited.pop()
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    print(f"Backtracking to location ({self.bot[0]}, {self.bot[1]})")
                    distance_traveled = int(math.sqrt((self.bot[0] - prev_location[0])**2 + (self.bot[1] - prev_location[1])**2))
                    self.actions_counter += distance_traveled
            print(self)
    
    def run_bot_7(self, a_val):
        leak_prob = [[1/ (len(self.open_cells_list) - 1)] * self.D for _ in range(self.D)]
        for i in range(self.D):
            for j in range(self.D):
                if (i,j) not in self.open_cells_list:
                    leak_prob[i][j] = 0

        bot_x, bot_y = self.bot
        leak_prob[bot_x + 1][bot_y] = 0
        total_actions = 0

        dist_to_leak = self.find_shortest_path(self.bot, self.leak)
        prob_beep = math.exp(-1 * a_val * (dist_to_leak - 1))
        
        # while self.bot != self.leak:
        #     leak_prob[bot_x, bot_y] = 0
        #     leak_prob = self.update_mat_enter(leak_prob)
        #     #sense action
        #     dist_to_leak = self.find_shortest_path(self.bot, self.leak)
        #     prob_beep = math.exp(-1 * a_val * (dist_to_leak - 1))


    
    def run_bot_8(self, k_val):
        pass
    
    def run_bot_9(self, k_val):
        pass

if __name__ == "__main__":
    ship = Ship()
    k_val= int(input("Enter k value: "))
    ship.k_val = k_val
    ship.generate_ship()
    print(ship)

    ans = int(input("Which bot do you want to run?\n1.Bot 1\n2.Bot 2\n3.Bot 3\n4.Bot 4\n5.Bot 5\n6.Bot 6\n7.Bot 7\n8.Bot 8\n9.Bot: 9\n"))

    if ans == 1:
        ship.run_bot_1()
    elif ans == 2:
        ship.run_bot_2()
    elif ans == 3:
        alpha = int(input("What is your aplha value?\n"))
        ship.run_bot_3(alpha)
    elif ans == 4:
        ship.run_bot_4()
    elif ans == 5:
        ship.run_bot_5()
    elif ans == 6:
        ship.run_bot_6()
    elif ans == 7:
        ship.run_bot_7()
    elif ans == 8:
        ship.run_bot_8()
    elif ans == 9:
        ship.run_bot_9()
    else:
        print("Invalid bot choice.")
