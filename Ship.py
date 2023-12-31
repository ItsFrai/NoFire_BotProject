import random
import math
import time
from collections import deque
import matplotlib.pyplot as plt


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
        self.bot = (-1, -1) # sets it to a inital position that is not valid
        self.leak = (-1, -1)
        self.second_leak = (-1,-1)
        self.init_bot_location = (-1,-1)
        self.k_val = 0
        self.actions_counter = 0
        self.open_cells_list = [()]
        self.found_1 = 0
        self.found_2 = 0


    # Reset instance variables to their initial values
    def reset(self):
        bot_x, bot_y = self.bot
        self.ship[bot_x][bot_y] = 'O'
        self.bot = (-1,-1)
                    
        while self.bot == (-1, -1):
                rand_x_coord = random.randint(0, self.D - 1)
                rand_y_coord = random.randint(0, self.D - 1)
                if self.ship[rand_x_coord][rand_y_coord] != "X": #can't be inside a wall
                    if self.count_neighbors(rand_x_coord, rand_y_coord, "O") != 0: # can't be blocked in
                        self.ship[rand_x_coord][rand_y_coord] = self.colored_block('c')
                        self.init_bot_location = self.bot = (rand_x_coord, rand_y_coord)
                          
        bot_x, bot_y = self.bot
        self.ship[bot_x][bot_y] = self.colored_block('c')


        leak_x,leak_y = self.leak
        self.ship[leak_x][leak_y] = 'O'
        self.leak = (-1,-1)
        while self.leak == (-1, -1):
            leak_x = random.randint(0, self.D - 1)
            leak_y = random.randint(0, self.D - 1)
            if (abs(leak_x - self.bot[0]) > k + 1 or abs(leak_y - self.bot[1]) > k + 1 and self.ship[leak_x][leak_y] != "X"):
                self.ship[leak_x][leak_y] = self.colored_block('g')
                self.leak = (leak_x, leak_y)
                break
            
        self.visited = set()
        self.actions_counter = 0

    def __repr__(self):
        ship_str = ""
        for x in range(self.D):
            for y in range(self.D):
                cell = self.ship[x][y]
                ship_str += "[" + cell + "]"
            ship_str += "\n"

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

            while self.bot == (-1, -1):
                rand_x_coord = random.randint(0, self.D - 1)
                rand_y_coord = random.randint(0, self.D - 1)
                if self.ship[rand_x_coord][rand_y_coord] != "X": #can't be inside a wall
                    if self.count_neighbors(rand_x_coord, rand_x_coord, "O") != 0: # can't be blocked in
                        self.ship[rand_x_coord][rand_y_coord] = self.colored_block('c')
                        self.init_bot_location = self.bot = (rand_x_coord, rand_y_coord)
                        

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
        k_val = int(self.k_val)         
        for x in range(self.bot[0] - k_val, self.bot[0] + k_val + 1):
            for y in range(self.bot[1] - k_val, self.bot[1] + k_val + 1):
                if 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                    detection_square.append((x, y))
        return detection_square

    def update_mat_enter(self, prob_mat) -> list[list[float]]:
        sum_prob = 0
        for x in range(self.D):
            for y in range(self.D):
                sum_prob += prob_mat[x][y]

        for x in range(self.D):
            for y in range(self.D):
                prob_mat[x][y] = prob_mat[x][y] / sum_prob
        
        return prob_mat

    def update_mat_beep(self, prob_mat, a_val) -> list[list[float]]:
        temp_mat = [[0.0 for _ in range(self.D)] for _ in range(self.D)]
        sum_prob = 0.0
        
        # for each cell, finds prob of beep based on distance to bot if open cell
        for x in range(self.D):
            for y in range(self.D):
                dist = 0
                if (x,y) in self.open_cells_list:
                    dist = len(self.find_shortest_path((x,y), self.bot)) - 1
                    temp_mat[x][y] = math.exp( -a_val * (dist - 1))

        for x in range(self.D):
            for y in range(self.D):
                if (x,y) in self.open_cells_list:
                    temp_mat[x][y] = (temp_mat[x][y] * prob_mat[x][y])
                    sum_prob += temp_mat[x][y]
        
        for x in range(self.D):
            for y in range(self.D):
                temp_mat[x][y] = temp_mat[x][y] / sum_prob

        return temp_mat    

    def update_mat_nobeep(self, prob_mat, a_val) -> list[list[float]]:
        temp_mat = [[0.0 for _ in range(self.D)] for _ in range(self.D)]
        sum_prob = 0.0
        
        for x in range(self.D):
            for y in range(self.D):
                dist = 0
                if (x,y) in self.open_cells_list:
                    dist = len(self.find_shortest_path((x,y), self.bot)) - 1
                    temp_mat[x][y] = 1 - (math.exp( -a_val * (dist - 1)))

        for x in range(self.D):
            for y in range(self.D):
                if (x,y) in self.open_cells_list:
                    temp_mat[x][y] = (temp_mat[x][y] * prob_mat[x][y])
                    sum_prob += temp_mat[x][y]
        
        for x in range(self.D):
            for y in range(self.D):
                temp_mat[x][y] = temp_mat[x][y] / sum_prob
 
        return temp_mat

    def update_mat_enter_mult(self, prob_mat) -> dict:
        sum_prob = sum(prob_mat.values())
        
        for key,value in prob_mat.items():
            prob_mat[key] /= sum_prob
            
        return prob_mat

    def update_mat_beep_mult(self, prob_mat, a_val) -> dict:
        sum_prob = 0
        
        for key, value in prob_mat.items():
            leak_1, leak_2 = key
            if (self.found_1 == 1):
                leak_1 = self.leak
            if (self.found_2 == 2):
                leak_2 = self.second_leak
            dist_leak_1 = len(self.find_shortest_path((self.bot), (leak_1))) - 1
            dist_leak_2 = len(self.find_shortest_path((self.bot), (leak_2))) - 1
            prob_beep_1 = math.exp( -a_val * (dist_leak_1 - 1))
            prob_beep_2 = math.exp( -a_val * (dist_leak_2 - 1))
            prob_beep = prob_beep_1 + prob_beep_2 - (prob_beep_1 * prob_beep_2)
            prob_mat[key] *= prob_beep
            sum_prob += prob_mat[key]
            
        for key, value in prob_mat.items():
            prob_mat[key] /= sum_prob
            
        total_sum = sum(prob_mat.values())
        print(total_sum)
        
        return prob_mat

    def update_mat_no_beep_mult(self, prob_mat, a_val) -> dict:
        
        sum_prob = 0
        
        for key, value in prob_mat.items():
            leak_1, leak_2 = key
            if (self.found_1 == 1):
                leak_1 = self.leak
            if (self.found_2 == 2):
                leak_2 = self.second_leak
            dist_leak_1 = len(self.find_shortest_path((self.bot), (leak_1))) - 1
            dist_leak_2 = len(self.find_shortest_path((self.bot), (leak_2))) - 1
            prob_beep_1 = math.exp( -a_val * (dist_leak_1 - 1))
            prob_beep_2 = math.exp( -a_val * (dist_leak_2 - 1))
            prob_beep = prob_beep_1 + prob_beep_2 - (prob_beep_1 * prob_beep_2)
            prob_mat[key] *= (1 - prob_beep)
            sum_prob += prob_mat[key]
            
        for key, value in prob_mat.items():
            prob_mat[key] /= sum_prob
            
        total_sum = sum(prob_mat.values())
        print(total_sum)
        
        return prob_mat

    def create_prob_mat(self, leak_prob) -> list[list[float]]:
        prob_mat = [[0.0]* self.D for _ in range(self.D)]
        for x in range(self.D):
            for y in range(self.D):
                visited = []
                for key, value in leak_prob.items():
                    t_1 , t_2 = key
                    
                    if (t_1 == (x,y)) and (x,y) not in visited:
                        prob_mat[x][y] += leak_prob[key]
                    
        total_sum = 0
        for x in range(self.D):
            for y in range(self.D):            
                total_sum += prob_mat[x][y]
                
        return prob_mat

    def run_bot_1(self, k):
        # Initialize a queue for BFS
        queue = deque([self.bot])  
        # Initialize a set to keep track of visited locations
        visited = set()
        
        if self.leak == (-1, -1):
            while True:
                leak_x = random.randint(0, self.D - 1)
                leak_y = random.randint(0, self.D - 1)
                if (abs(leak_x - self.bot[0]) > k + 1 or abs(leak_y - self.bot[1]) > k + 1):
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.leak = (leak_x, leak_y)
                    print(f"Leak generated at location {self.leak}")
                    break

        while queue:
            current_location = queue.popleft()
            
            # Check if the current location is the leak
            if current_location == self.leak:
                print("Congratulations, you found the leak!")
                print(f"Total amount of actions = {self.actions_counter}")
                return
            
            # Sense action and mark the location as visited
            if self.sense_action():
                print("Leak found")
                for x in range(self.bot[0] - k, self.bot[0] + k + 1):
                    for y in range(self.bot[1] - k, self.bot[1] + k + 1):
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                            print(f"Moving to location ({x}, {y})")
                            print(self)
                            visited.add((x, y))
                            self.ship[self.bot[0]][self.bot[1]] = 'O'
                            self.bot = (x, y)
                            self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                            self.actions_counter += 1  
                        
                            if self.bot == self.leak:
                                print("Congratulations, you found the leak!")
                                print(f"Total amount of actions = {ship.actions_counter}")  
                                return

            # Explore neighboring cells
            for dx, dy in self.directions:
                new_location = (current_location[0] + dx, current_location[1] + dy)

                # Check if the new location is valid and not visited
                if 0 <= new_location[0] < self.D and 0 <= new_location[1] < self.D and self.ship[new_location[0]][new_location[1]] != 'X' and new_location not in visited:
                    print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                    print(self)
                    visited.add(new_location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = new_location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    queue.append(new_location)
                    self.actions_counter += 1
                    
    def run_bot_1_simulation(self, num_simulations):
        results = []
        for k in range(1, 15):
            total_actions = 0
            for _ in range(num_simulations):
                ship.reset()
                self.k_val = k
                self.run_bot_1(k)
                total_actions += self.actions_counter
            average_actions = total_actions / num_simulations
            results.append((k, average_actions))
        return results
            
    def run_bot_2(self, k):
        
        queue = deque([self.bot])  

        # Initialize a set to keep track of visited locations
        visited = set()

        # Initialize a set to keep track of sensed locations
        sensed_locations = set()

        if self.leak == (-1, -1):
            while True:
                leak_x = random.randint(0, self.D - 1)
                leak_y = random.randint(0, self.D - 1)
                if (abs(leak_x - self.bot[0]) > k + 1 or abs(leak_y - self.bot[1]) > k + 1):
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.leak = (leak_x, leak_y)
                    break

        while queue:
            current_location = queue.popleft()

            # Check if the current location is the leak
            if current_location == self.leak:
                return
            
            
            detection_square = self.get_detection_square()
            unsensed_count = sum(1 for location in detection_square if location not in sensed_locations) 

            # Only sense if more than half of the cells are not sensed
            if (unsensed_count > len(detection_square) // 2):
                sensed_action_result = self.sense_action()
                for location in detection_square:
                    if location not in visited:
                        if not sensed_action_result:
                            sensed_locations.add(location)
                if self.sense_action():
                    print("Leak found")
                    for x in range(self.bot[0] - k, self.bot[0] + k + 1):
                        for y in range(self.bot[1] - k, self.bot[1] + k + 1):
                            if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                                print(f"Moving to location ({x}, {y})")
                                print(self)
                                visited.add((x, y))
                                self.ship[self.bot[0]][self.bot[1]] = 'O'
                                self.bot = (x, y)
                                self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                                self.actions_counter += 1  
                            
                                if self.bot == self.leak:
                                   print("Congratulations, you found the leak!")
                                   print(f"Total amount of actions = {ship.actions_counter}")  
                                   return

            # Explore neighboring cells
            for dx, dy in self.directions:
                new_location = (current_location[0] + dx, current_location[1] + dy)

                # Check if the new location is valid and not visited
                if 0 <= new_location[0] < self.D and 0 <= new_location[1] < self.D and self.ship[new_location[0]][new_location[1]] != 'X' and new_location not in visited:
                    print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                    print(self)
                    visited.add(new_location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = new_location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    queue.append(new_location)
                    self.actions_counter += 1

     
    def run_bot_2_simulation(self, num_simulations):
        results = []
        for k in range(1, 15):
            total_actions = 0
            for _ in range(num_simulations):
                ship.reset()
                self.k_val = k
                self.run_bot_2(k)
                total_actions += self.actions_counter
            average_actions = total_actions / num_simulations
            results.append((k, average_actions))
        return results
                       
        #sense_action (for probabilistic determination)
        #compute the probability of receiving a beep
            #based on that probability, re-initilize the probability matrix to take the new beep/no-beep probability
                #this is based on P(leak in matrix [x][y](the specific position in the interation for loop) | beep in current position) 
                # or P(leak in matrix [x][y] | NO beep in current position)
                # this might be trick because you have to find the shortest path (make another helper method for this, you can use the bfs algo from the last project but modified)
                # from the bot to the leak in order to get the D value for the probability (save this value as it might be used later)

    def run_bot_3(self, a_val):
        # sets the leak if it hasn't been set previously
        while self.leak == (-1, -1):
            leak_x = random.randint(0, self.D - 1)
            leak_y = random.randint(0, self.D - 1)
            if self.count_neighbors(leak_x, leak_y, "O") > 0 and self.ship[leak_x][leak_y] != "X":
                self.ship[leak_x][leak_y] = self.colored_block('g')
                self.leak = (leak_x, leak_y)
                print(f"Leak generated at location {self.leak}")
        
        # starts the prob matrix with equal probability for all cells
        leak_prob = [[1/ (len(self.open_cells_list) - 1)] * self.D for _ in range(self.D)]
        for i in range(self.D):
            for j in range(self.D):
                if (i,j) not in self.open_cells_list:
                    leak_prob[i][j] = 0

        total_actions = 0
        
        while self.bot != self.leak:
            # set the current bot location to not have the leak and update the matrix accordingly
            bot_x, bot_y = self.bot
            leak_prob[bot_x][bot_y] = 0
            leak_prob = self.update_mat_enter(leak_prob)
            beep = 0
            #sense action
            dist_to_leak = len(self.find_shortest_path(self.bot, self.leak)) - 1
            prob_beep = math.exp( -a_val * (dist_to_leak - 1))
            rand = random.random()
            if rand <= prob_beep:
                beep = 1
            total_actions += 1

            #updating probability matrix depending if there is a beep
            if beep == 1:
                leak_prob = self.update_mat_beep(leak_prob, a_val)
            else:
                leak_prob = self.update_mat_nobeep(leak_prob, a_val)

            
            # first gets the max value
            max_val = leak_prob[0][0]
            new_x = new_y = 0
            for i in range(self.D):
                for j in range(self.D):
                    if leak_prob[i][j] > max_val:
                        max_val = leak_prob[i][j]
                        new_x, new_y = i, j
        
            # checks for duplicates of that max
            max_prob_ties = [] # list for cells with multiple max probabilites 
            
            for i in range(self.D):
                for j in range(self.D):
                    if leak_prob[i][j] == max_val:
                        max_prob_ties.append((i,j))
            
            # get the min coord
            min_coord = min(max_prob_ties, key=lambda tie: len(self.find_shortest_path((bot_x, bot_y), (tie[0], tie[1]))) - 1)

            total_actions += (len(self.find_shortest_path((bot_x, bot_y), (min_coord[0], min_coord[1]))) - 1)
            self.ship[bot_x][bot_y] = "O"
            self.ship[min_coord[0]][min_coord[1]] = self.colored_block('c')
            print(f"RELOCATING TO {(new_x, new_y)}")
            print(f"BEGAN AT: {(bot_x, bot_y)}")
            print(self)
            self.bot = (new_x, new_y)
            
        print(f"Congratulations! You found the leak in {total_actions} actions!")
        return total_actions
    
    def run_bot_4(self, a_val):
        # sets the leak if it hasn't been set previously
        while self.leak == (-1, -1):
            leak_x = random.randint(0, self.D - 1)
            leak_y = random.randint(0, self.D - 1)
            if self.count_neighbors(leak_x, leak_y, "O") > 0 and self.ship[leak_x][leak_y] != "X":
                self.ship[leak_x][leak_y] = self.colored_block('g')
                self.leak = (leak_x, leak_y)
                print(f"Leak generated at location {self.leak}")
        
         # starts the prob matrix with equal probability for all cells
        leak_prob = [[1/ (len(self.open_cells_list) - 1)] * self.D for _ in range(self.D)]
        for i in range(self.D):
            for j in range(self.D):
                if (i,j) not in self.open_cells_list:
                    leak_prob[i][j] = 0

        total_actions = 0 
        
        while self.bot != self.leak:
            # set the current bot location to not have the leak and update the matrix accordingly
            bot_x, bot_y = self.bot
            leak_prob[bot_x][bot_y] = 0
            leak_prob = self.update_mat_enter(leak_prob)
            beep = 0
            #sense action
            dist_to_leak = len(self.find_shortest_path(self.bot, self.leak)) - 1
            prob_beep = math.exp( -a_val * (dist_to_leak - 1))
            rand = random.random()
            if rand <= prob_beep:
                beep = 1
            total_actions += 1

            # updating probability matrix depending if there is a beep
            if beep == 1:
                leak_prob = self.update_mat_beep(leak_prob, a_val)
            else:
                leak_prob = self.update_mat_nobeep(leak_prob, a_val)

            max_val = leak_prob[0][0]
            max_x = max_y = 0
            sec_max_x = sec_max_y = 0
            for i in range(self.D):
                for j in range(self.D):
                    if leak_prob[i][j] > max_val:
                        sec_max_x, sec_max_y = max_x, max_y
                        max_val = leak_prob[i][j]
                        max_x, max_y = i, j

            # now, instead of just going to the highest prob directly see which one is closer to the bot's starting location
            # the second location offers a better risk to potential ratio (don't travel too far)
            max_dist = len(self.find_shortest_path((bot_x, bot_y), (max_x, max_y))) - 1 # distance of best prob
            second_dist = len(self.find_shortest_path((bot_x, bot_y), (sec_max_x, sec_max_y))) - 1 # dist of second best

            if second_dist > max_dist:
                total_actions += second_dist
                self.ship[bot_x][bot_y] = "O"
                self.ship[sec_max_x][sec_max_y] = self.colored_block('c')
                print(f"RELOCATING TO {(sec_max_x, sec_max_y)}")
                print(f"BEGAN AT: {(bot_x, bot_y)}")
                print(self)
                self.bot = (sec_max_x, sec_max_y)
            else:
                total_actions += max_dist
                self.ship[bot_x][bot_y] = "O"
                self.ship[max_x][max_y] = self.colored_block('c')
                print(f"RELOCATING TO {(max_x, max_y)}")
                print(f"BEGAN AT: {(bot_x, bot_y)}")
                print(self)
                self.bot = (max_x, max_y)
            
        print(f"Congratulations! You found the leak in {total_actions} actions!")
        return total_actions

    def run_bot_5(self, k): 
        
        if self.leak == (-1, -1):
            while True:
                leak_x = random.randint(0, self.D - 1)
                leak_y = random.randint(0, self.D - 1)
                if (abs(leak_x - self.bot[0]) > k + 1 or abs(leak_y - self.bot[1]) > k + 1):
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.leak = (leak_x, leak_y)
                    print(f"Leak generated at location {self.leak}")
                    break
        while True:
        
            new_x = random.randint(0, self.D - 1)
            new_y = random.randint(0, self.D - 1)
            if (new_x != self.leak[0] or new_y != self.leak[1]) and (new_x != self.bot[0] or new_y != self.bot[1]) and self.ship[new_x][new_y] != 'X' and (abs(new_x - self.bot[0]) > k + 1 or abs(new_y - self.bot[1]) > k + 1):
                break
        # Add the second leak to the ship grid
        self.ship[new_x][new_y] = self.colored_block('g')
        self.second_leak = (new_x, new_y)

        queue = deque([self.bot])  # Each queue element is a tuple (location, distance)

        visited = set()

        # Keep track of leaks found
        leaks_found = 0

        while queue and leaks_found < 2:
            current_location = queue.popleft()

            # Sense action and mark the location as visited
            if self.sense_action_for_two():
                print("Leak found")
                for x in range(self.bot[0] - k, self.bot[0] + k + 1):
                    for y in range(self.bot[1] - k, self.bot[1] + k + 1):
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                            print(f"Moving to location ({x}, {y})")
                            print(self)
                            visited.add((x, y))
                            self.ship[self.bot[0]][self.bot[1]] = 'O'
                            self.bot = (x, y)
                            self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                            self.actions_counter += 1  
                        
                            if self.bot == self.leak:
                                print("Congratulations, you found the original leak!")
                                print(f"Total amount of actions so far = {ship.actions_counter}") 
                                leaks_found += 1
                                self.leak = (-1,-1)
                                
                            if self.bot == self.second_leak:
                                print("Congratulations, you found the second leak!")
                                print(f"Total amount of actions so far = {ship.actions_counter}")
                                leaks_found += 1
                                self.second_leak = (-1,-1)
            if leaks_found == 2:
                print("Both leaks found!")
                print(f"Total amount of actions = {ship.actions_counter}")
                break

            # Explore neighboring cells
            for dx, dy in self.directions:
                new_location = (current_location[0] + dx, current_location[1] + dy)

                # Check if the new location is valid and not visited
                if 0 <= new_location[0] < self.D and 0 <= new_location[1] < self.D and self.ship[new_location[0]][new_location[1]] != 'X' and new_location not in visited:
                    print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                    print(self)
                    visited.add(new_location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = new_location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    queue.append(new_location)
                    self.actions_counter += 1
                    
    def run_bot_5_simulation(self, num_simulations):
        results = []
        for k in range(1, 15):
            total_actions = 0
            for _ in range(num_simulations):
                ship.reset()
                self.k_val = k
                self.run_bot_1(k)
                total_actions += self.actions_counter
            average_actions = total_actions / num_simulations
            results.append((k, average_actions))
        return results

    
    def run_bot_6(self, k):
        
        if self.leak == (-1, -1):
            while True:
                leak_x = random.randint(0, self.D - 1)
                leak_y = random.randint(0, self.D - 1)
                if (abs(leak_x - self.bot[0]) > k + 1 or abs(leak_y - self.bot[1]) > k + 1):
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.leak = (leak_x, leak_y)
                    print(f"Leak generated at location {self.leak}")
                    break
        
        while True:
            new_x = random.randint(0, self.D - 1)
            new_y = random.randint(0, self.D - 1)
            if (new_x != self.leak[0] or new_y != self.leak[1]) and (new_x != self.bot[0] or new_y != self.bot[1]) and self.ship[new_x][new_y] != 'X' and (abs(new_x - self.bot[0]) > k + 1 or abs(new_y - self.bot[1]) > k + 1):
                break
        # Add the second leak to the ship grid
        self.ship[new_x][new_y] = self.colored_block('g')
        self.second_leak = (new_x, new_y)

        visited = set()
        
        queue = deque([self.bot])

        leaks_found = 0  # To keep track of the number of leaks found

        while queue and leaks_found < 2:
            
            current_location = queue.popleft()
                        
            if self.sense_action_bothleaks():
                print("Both leaks found good job!")
                print(self)
                
                # Find the shortest path to the first leak
                path_to_first_leak = self.find_shortest_path(start=self.bot, end=self.leak)
                # Find the shortest path to the second leak
                path_to_second_leak = self.find_shortest_path(start=self.bot, end=self.second_leak)

                # Determine which path is shorter
                if len(path_to_first_leak) <= len(path_to_second_leak):
                    shortest_path = path_to_first_leak
                    target_leak = self.leak
                    other_path = path_to_second_leak
                    other_target_leak = self.second_leak
                else:
                    shortest_path = path_to_second_leak
                    target_leak = self.second_leak
                    other_path = path_to_first_leak
                    other_target_leak = self.leak

                # Move along the shortest path to the first leak
                for location in shortest_path:
                    print(f"Moving to location ({location[0]}, {location[1]})")
                    visited.add(location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    self.actions_counter += 1

                    if self.bot == target_leak:
                        print(f"Congratulations, you found the leak at {target_leak}!")
                        print(f"Total amount of actions so far = {ship.actions_counter}") 

                        leaks_found += 1
                        if target_leak == self.leak:
                            self.leak = None     
                        else:
                            self.second_leak = None
                # Move along the other path
                for location in other_path:
                    print(f"Moving to location ({location[0]}, {location[1]})")
                    visited.add(location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    self.actions_counter += 1

                    if self.bot == other_target_leak:
                        print(f"Congratulations, you found the leak at {other_target_leak}!")
                        print(f"Total amount of actions = {ship.actions_counter}") 

                        leaks_found += 1
                        if other_target_leak == self.leak:
                            self.leak = (-1,-1)
                        else:
                            self.second_leak = (-1,-1)
                continue 
                              
            if self.sense_action_for_two():
                print("Leak found")
                for x in range(self.bot[0] - k, self.bot[0] + k + 1):
                    for y in range(self.bot[1] - k, self.bot[1] + k + 1):
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                            print(f"Moving to location ({x}, {y})")
                            print(self)
                            visited.add((x, y))
                            self.ship[self.bot[0]][self.bot[1]] = 'O'
                            self.bot = (x, y)
                            self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                            self.actions_counter += 1  
                        
                            if self.bot == self.leak:
                                print("Congratulations, you found the original leak!")
                                print(f"Total amount of actions so far = {ship.actions_counter}") 
                                leaks_found += 1
                                self.leak = (-1,-1)
                                
                            if self.bot == self.second_leak:
                                print("Congratulations, you found the second leak!")
                                print(f"Total amount of actions so far = {ship.actions_counter}")
                                leaks_found += 1
                                self.second_leak = (-1,-1)
            if leaks_found == 2:
                print("Both leaks found!")
                print(f"Total amount of actions = {ship.actions_counter}")
                break
                                
            for dx, dy in self.directions:
                new_location = (current_location[0] + dx, current_location[1] + dy)

                # Check if the new location is valid and not visited
                if 0 <= new_location[0] < self.D and 0 <= new_location[1] < self.D and self.ship[new_location[0]][new_location[1]] != 'X' and new_location not in visited:
                    print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                    print(self)
                    visited.add(new_location)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = new_location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    queue.append(new_location)
                    self.actions_counter += 1
                    
    def run_bot_6_simulation(self, num_simulations):
        results = []
        for k in range(1, 15):
            total_actions = 0
            for _ in range(num_simulations):
                ship.reset()
                self.k_val = k
                self.run_bot_1(k)
                total_actions += self.actions_counter
            average_actions = total_actions / num_simulations
            results.append((k, average_actions))
        return results 


    def run_bot_7(self, a_val: float):
        # sets the leaks if it hasn't been set previously
        while self.leak == (-1, -1) or self.second_leak == (-1,-1):
            leak_x = random.randint(0, self.D - 1)
            leak_y = random.randint(0, self.D - 1)
            if self.count_neighbors(leak_x, leak_y, "O") > 0 and self.ship[leak_x][leak_y] != "X":
                if self.leak == (-1,-1):
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.leak = (leak_x, leak_y)
                    print(f"Leak generated at location {self.leak}")
                elif self.second_leak != self.leak: # new value for second leak
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.second_leak = (leak_x, leak_y)
                    print(f"Second Leak generated at location {self.second_leak}")

        print(self)

        #the reason that there is a -1 because you have to remove the bots starting location
        leak_prob = [[1/ (len(self.open_cells_list) - 1)] * self.D for _ in range(self.D)]
        for i in range(self.D):
            for j in range(self.D):
                if (i,j) not in self.open_cells_list:
                    leak_prob[i][j] = 0

        total_actions = 0
        visited = []
            
        while self.bot != self.leak:
            bot_x, bot_y = self.bot
            if (self.bot == self.second_leak):
                self.found_2 = 1
            leak_prob[bot_x][bot_y] = 0
            visited.append((bot_x, bot_y))
            leak_prob = self.update_mat_enter(leak_prob)
            beep = 0

            #sense action
            dist_to_leak = len(self.find_shortest_path(self.bot, self.leak)) - 1
            prob_beep = math.exp( -a_val * (dist_to_leak - 1))
            rand = random.random()
            if rand <= prob_beep:
                beep = 1
            total_actions += 1

            if beep == 1:
                leak_prob = self.update_mat_beep(leak_prob, a_val)
            else:
                leak_prob = self.update_mat_nobeep(leak_prob, a_val)
            
            max_val = leak_prob[0][0]
            new_x = 0
            new_y = 0
            for i in range(self.D):
                for j in range(self.D):
                    if leak_prob[i][j] > max_val:
                        max_val = leak_prob[i][j]
                        new_x = i
                        new_y = j

            total_actions += (len(self.find_shortest_path((bot_x, bot_y), (new_x, new_y))) - 1)
            self.ship[bot_x][bot_y] = "O"
            self.ship[new_x][new_y] = self.colored_block('c')
            print(f"RELOCATING TO {(new_x, new_y)}")
            print(f"BEGAN AT: {(bot_x, bot_y)}")
            print(self) 
            self.bot = (new_x, new_y)

        #at this point the first leak has been found and now the initilization of the second prob matrix is happening
        print(visited)
        print(len(visited))
        print(len(self.open_cells_list))
        
        leak_prob_2 = [[1/ (len(self.open_cells_list) - 1 - len(visited))] * self.D for _ in range(self.D)]
        for i in range(self.D):
            for j in range(self.D):
                if (i,j) not in self.open_cells_list or (i,j) in visited:
                    leak_prob_2[i][j] = 0


        while self.bot != self.second_leak and self.found_2 == 0:
            bot_x, bot_y = self.bot
            leak_prob_2[bot_x][bot_y] = 0
            visited.append((bot_x, bot_y))
            leak_prob_2 = self.update_mat_enter(leak_prob_2)
            beep = 0

            #sense action
            dist_to_leak = len(self.find_shortest_path(self.bot, self.second_leak)) - 1
            prob_beep = math.exp( -a_val * (dist_to_leak - 1))
            rand = random.random()
            if rand <= prob_beep:
                beep = 1
            total_actions += 1

            if beep == 1:
                leak_prob_2 = self.update_mat_beep(leak_prob_2, a_val)
            else:
                leak_prob_2 = self.update_mat_nobeep(leak_prob_2, a_val)
            
            max_val = leak_prob_2[0][0]
            new_x = 0
            new_y = 0
            for i in range(self.D):
                for j in range(self.D):
                    if leak_prob_2[i][j] > max_val:
                        max_val = leak_prob_2[i][j]
                        new_x = i
                        new_y = j

            total_actions += (len(self.find_shortest_path((bot_x, bot_y), (new_x, new_y))) - 1)
            self.ship[bot_x][bot_y] = "O"
            self.ship[new_x][new_y] = self.colored_block('c')
            print(f"RELOCATING TO {(new_x, new_y)}")
            print(f"BEGAN AT: {(bot_x, bot_y)}")
            print(self) 
            self.bot = (new_x, new_y)
            
        print(f"Congratulations! You found the leaks in {total_actions} actions!")
        return total_actions
            

    def run_bot_8(self, a_val):

        while self.leak == (-1, -1) or self.second_leak == (-1,-1):
            leak_x = random.randint(0, self.D - 1)
            leak_y = random.randint(0, self.D - 1)
            if self.count_neighbors(leak_x, leak_y, "O") > 0 and self.ship[leak_x][leak_y] != "X":

                if self.leak == (-1,-1):
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.leak = (leak_x, leak_y)
                    print(f"Leak generated at location {self.leak}")
                elif self.second_leak != self.leak: # new value for second leak
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.second_leak = (leak_x, leak_y)
                    print(f"Second Leak generated at location {self.second_leak}")
        
        
        #initilizing the main prob list for all of the possible leak combinations
        leak_prob = {}
        for x in range(self.D):
            for y in range(self.D):
                for a in range(x, self.D):
                    for b in range(y, self.D):
                        if (x,y) in self.open_cells_list and (a,b) in self.open_cells_list and (x,y) != (a,b):
                            leak_prob[((x,y), (a,b))] = 0.0
        print(len(leak_prob))
        
        #initilizing the probability matrix for the 2-Dimensional array
        prob_mat = []
        
        total_actions = 0


        for key, value in leak_prob.items():
            leak_prob[key] = 1 / len(leak_prob)
        
        bot_x, bot_y = self.bot
                    
        while self.found_1 == 0 or self.found_2 == 0:
            if (self.bot == self.leak):
                self.found_1 = 1
                print("you found the first leak")
                
            if (self.bot == self.second_leak):
                self.found_2 = 1
                print("you found the second leak")
                
            if self.found_1 == 1 and self.found_2 == 1:
                break
                
            bot_x, bot_y = self.bot
            for a in range(self.D):
                for b in range(self.D):
                    if (a,b) in self.open_cells_list:
                        leak_prob[((bot_x, bot_y), (a,b))] = 0.0
                        
            leak_prob = self.update_mat_enter_mult(leak_prob) 
            
            #sense action
            beep = 0
            dist_leak_1 = len(self.find_shortest_path((self.bot), (self.leak))) - 1
            dist_leak_2 = len(self.find_shortest_path(self.bot, self.second_leak)) - 1
            prob_beep_1 = math.exp( -a_val * (dist_leak_1 - 1))
            prob_beep_2 = math.exp( -a_val * (dist_leak_2 - 1))
            prob_beep = prob_beep_1 + prob_beep_2 - (prob_beep_1 * prob_beep_2)
            rand = random.random()
            if rand <= prob_beep:
                beep = 1
            total_actions += 1
                        
            #update probabilities based on the occurence of the beep
            if beep == 1:
                leak_prob = self.update_mat_beep_mult(leak_prob, a_val)
            else:
                leak_prob = self.update_mat_no_beep_mult(leak_prob, a_val)
                
            prob_mat = self.create_prob_mat(leak_prob)

            # first gets the max value
            max_val = prob_mat[0][0]
            new_x = new_y = 0
            for i in range(self.D):
                for j in range(self.D):
                    if prob_mat[i][j] > max_val:
                        max_val = prob_mat[i][j]
                        new_x, new_y = i, j
        
            # checks for duplicates of that max
            max_prob_ties = [] # list for cells with multiple max probabilites 
            
            for i in range(self.D):
                for j in range(self.D):
                    if prob_mat[i][j] == max_val:
                        max_prob_ties.append((i,j))
            
            # get the min coord
            min_coord = min(max_prob_ties, key=lambda tie: len(self.find_shortest_path((bot_x, bot_y), (tie[0], tie[1]))) - 1)

            total_actions += (len(self.find_shortest_path((bot_x, bot_y), (min_coord[0], min_coord[1]))) - 1)
            self.ship[bot_x][bot_y] = "O"
            self.ship[min_coord[0]][min_coord[1]] = self.colored_block('c')
            print(f"RELOCATING TO {(new_x, new_y)}")
            print(f"BEGAN AT: {(bot_x, bot_y)}")
            print(self)
            self.bot = (new_x, new_y)
            

            
        print(f"Congratulations! You found the leaks in {total_actions} actions!")
        return total_actions
    
    def run_bot_9(self, a_val):

        while self.leak == (-1, -1) or self.second_leak == (-1,-1):
            leak_x = random.randint(0, self.D - 1)
            leak_y = random.randint(0, self.D - 1)
            if self.count_neighbors(leak_x, leak_y, "O") > 0 and self.ship[leak_x][leak_y] != "X":

                if self.leak == (-1,-1):
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.leak = (leak_x, leak_y)
                    print(f"Leak generated at location {self.leak}")
                elif self.second_leak != self.leak: # new value for second leak
                    self.ship[leak_x][leak_y] = self.colored_block('g')
                    self.second_leak = (leak_x, leak_y)
                    print(f"Second Leak generated at location {self.second_leak}")
        
        
        #initilizing the main prob list for all of the possible leak combinations
        leak_prob = {}
        for x in range(self.D):
            for y in range(self.D):
                for a in range(x, self.D):
                    for b in range(y, self.D):
                        if (x,y) in self.open_cells_list and (a,b) in self.open_cells_list and (x,y) != (a,b):
                            leak_prob[((x,y), (a,b))] = 0.0
        print(len(leak_prob))
        
        #initilizing the probability matrix for the 2-Dimensional array
        prob_mat = []
        
        total_actions = 0
        switch = 0


        for key, value in leak_prob.items():
            leak_prob[key] = 1 / len(leak_prob)
        
        bot_x, bot_y = self.bot
                    
        while self.found_1 == 0 or self.found_2 == 0:
            if (self.bot == self.leak):
                self.found_1 = 1
                print("you found the first leak")
                
            if (self.bot == self.second_leak):
                self.found_2 = 1
                print("you found the second leak")
                
            if self.found_1 == 1 and self.found_2 == 1:
                break
                
            bot_x, bot_y = self.bot
            for a in range(self.D):
                for b in range(self.D):
                    if (a,b) in self.open_cells_list:
                        leak_prob[((bot_x, bot_y), (a,b))] = 0.0
                        
            leak_prob = self.update_mat_enter_mult(leak_prob) 
            
            #sense action
            beep = 0
            dist_leak_1 = len(self.find_shortest_path((self.bot), (self.leak))) - 1
            dist_leak_2 = len(self.find_shortest_path(self.bot, self.second_leak)) - 1
            prob_beep_1 = math.exp( -a_val * (dist_leak_1 - 1))
            prob_beep_2 = math.exp( -a_val * (dist_leak_2 - 1))
            prob_beep = prob_beep_1 + prob_beep_2 - (prob_beep_1 * prob_beep_2)
            rand = random.random()
            if rand <= prob_beep:
                beep = 1
            total_actions += 1
                        
            #update probabilities based on the occurence of the beep
            if beep == 1:
                leak_prob = self.update_mat_beep_mult(leak_prob, a_val)
            else:
                leak_prob = self.update_mat_no_beep_mult(leak_prob, a_val)
                
            prob_mat = self.create_prob_mat(leak_prob)


            if switch  == 0:
                # first gets the max value
                max_val = prob_mat[0][0]
                new_x = new_y = 0
                for i in range(self.D):
                    for j in range(self.D):
                        if prob_mat[i][j] > max_val:
                            max_val = prob_mat[i][j]
                            new_x, new_y = i, j
            
                # checks for duplicates of that max
                max_prob_ties = [] # list for cells with multiple max probabilites 
                
                for i in range(self.D):
                    for j in range(self.D):
                        if prob_mat[i][j] == max_val:
                            max_prob_ties.append((i,j))
                
                # get the min coord
                min_coord = min(max_prob_ties, key=lambda tie: len(self.find_shortest_path((bot_x, bot_y), (tie[0], tie[1]))) - 1)

                total_actions += (len(self.find_shortest_path((bot_x, bot_y), (min_coord[0], min_coord[1]))) - 1)
                self.ship[bot_x][bot_y] = "O"
                self.ship[min_coord[0]][min_coord[1]] = self.colored_block('c')
                print(f"RELOCATING TO {(new_x, new_y)}")
                print(f"BEGAN AT: {(bot_x, bot_y)}")
                print(self)
                self.bot = (new_x, new_y)
                switch = 1
            else:
                max_tuple_x, max_tuple_y = bot_x, bot_y
                for x, y in self.directions:
                    new_x, new_y = x + bot_x, y + bot_y
                    if self.ship[new_x][new_y] != "X" and prob_mat[new_x][new_y] > prob_mat[max_tuple_x][max_tuple_y]:
                        max_tuple_x = new_x
                        max_tuple_y = new_y

                total_actions += 1
                self.bot = (max_tuple_x, max_tuple_y)
                switch = 0
                    
            
        print(f"Congratulations! You found the leaks in {total_actions} actions!")
        return total_actions

if __name__ == "__main__":
    ship = Ship()
    ship.generate_ship()
    # print(ship)
    while True:
        print(ship)
        ans = int(input("Which bot do you want to run?\n1.Bot 1\n2.Bot 2\n3.Bot 3\n4.Bot 4\n5.Bot 5\n6.Bot 6\n7.Bot 7\n8.Bot 8\n9.Bot 9\n0.Exit\n"))

        if ans == 1 or ans == 2: # bots 1 & 2
            k = int(input("What is your k value?\n"))
            ship.k_val = k
            if ans == 1:
                ship.run_bot_1(k)
            else:
                ship.run_bot_2(k)

        elif ans == 3 or ans == 4: # bots 3 & 4
            alpha = float(input("What is your alpha value?\n"))
            if ans == 3:
                ship.run_bot_3(alpha)
            else:
                ship.run_bot_4(alpha)

        elif ans in [5,6,7,8,9]: # if bots 5,6,7,8,9
            if ans == 5 or ans == 6:
                k = int(input("What is your k value?\n"))
                ship.k_val = k
                if ans == 5:
                    ship.run_bot_5(k)
                else:
                    ship.run_bot_6(k)
        
            if ans in [7,8,9]:
                alpha = float(input("Insert the Alpha value:\n"))
                if ans == 7:
                    ship.run_bot_7(alpha)
                elif ans == 8:
                    ship.run_bot_8(alpha)
                else:
                    ship.run_bot_9()
                    
        elif ans == 0:
            break  # Exit the loop if the user chooses to exit
        else:
            print("Invalid bot choice.")
            
        run_another = input("Do you want to run another bot or run a simulation? (bot(b)/simulation(s)/no(n)): ").lower()

        if run_another == 'n':
            break  # Exit the loop if the user doesn't want to run another bot or simulation
        elif run_another == 's':
            num_simulations = 500
            simulation_type = int(input("Which simulation do you want to run?\n1. Bot 1 Simulation\n2. Bot 2 Simulation\n3. Bot 3 Simulation\n4. Bot 4 Simulation\n5. Bot 5 Simulation\n6. Bot 6 Simulation\n7. Bot 7 Simulation\n8. Bot 8 Simulation\n9. Bot 9 Simulation\n"))
            if simulation_type == 1:
                simulation_results = ship.run_bot_1_simulation(num_simulations)
                k_values, average_actions = zip(*simulation_results)

                plt.plot(k_values, average_actions, marker='o')
                plt.title('Bot 1 Simulation Results')
                plt.xlabel('k Value')
                plt.ylabel('Average Actions')
                plt.grid(True)
                plt.show()
            elif simulation_type == 2:
                simulation_results = ship.run_bot_2_simulation(num_simulations)
                k_values, average_actions = zip(*simulation_results)

                plt.plot(k_values, average_actions, marker='o')
                plt.title('Bot 2 Simulation Results')
                plt.xlabel('k Value')
                plt.ylabel('Average Actions')
                plt.grid(True)
                plt.show()
            elif simulation_type == 3:
                #simulation_results = ship.run_bot_3_simulation(num_simulations, alpha_value) 
                pass
            elif simulation_type == 4:
                #simulation_results = ship.run_bot_4_simulation(num_simulations, alpha_value)  
                pass
            elif simulation_type == 5:
                simulation_results = ship.run_bot_5_simulation(num_simulations)
                k_values, average_actions = zip(*simulation_results)

                plt.plot(k_values, average_actions, marker='o')
                plt.title('Bot 5 Simulation Results')
                plt.xlabel('k Value')
                plt.ylabel('Average Actions')
                plt.grid(True)
                plt.show()            
            elif simulation_type == 6:
                simulation_results = ship.run_bot_6_simulation(num_simulations)
                k_values, average_actions = zip(*simulation_results)

                plt.plot(k_values, average_actions, marker='o')
                plt.title('Bot 6 Simulation Results')
                plt.xlabel('k Value')
                plt.ylabel('Average Actions')
                plt.grid(True)
                plt.show()     
                
            elif simulation_type == 7:
                #simulation_results = ship.run_bot_7_simulation(num_simulations, alpha_value)
                pass  
            elif simulation_type == 8:
                #simulation_results = ship.run_bot_8_simulation(num_simulations, alpha_value)
                pass 
            elif simulation_type == 9:
                #simulation_results = ship.run_bot_9_simulation(num_simulations)  
                pass
            
        # Ask the user if they want to run another bot
        run_another = input("Do you want to run another bot? (yes(y)/no(n)): ").lower()
        if run_another == 'n':
            break  # Exit the loop if the user doesn't want to run another bot
        ship.reset()
