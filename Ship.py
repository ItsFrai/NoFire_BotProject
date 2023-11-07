import random
import math

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
        self.open_cells = 0
        
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
                    if self.ship[x][y] == 'O':
                        self.open_cells += 1

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
    def find_shortest_path(self, start: tuple, goal: tuple, constraints: list = []) -> int:
        fringe = dict()
        fringe.update({start: math.dist([start[0], start[1]], [goal[0], goal[1]])})
        parent = {}
        visited = []

        sorted_list = [start]
        while fringe:
            smallest_key = sorted_list.pop(0)
            curr_x, curr_y = smallest_key
            fringe.pop(smallest_key)

            # If the goal is found
            if smallest_key == goal:
                # Calculate the length of the path
                length = 0
                while smallest_key in parent:
                    length += 1
                    smallest_key = parent[smallest_key]
                return length

            for x, y in self.directions:
                new_x, new_y = x + curr_x, y + curr_y
                # Check if the neighbor is a valid one
                if 0 <= new_x < self.D and 0 <= new_y < self.D and self.ship[new_x][new_y] != 'X' and (new_x, new_y) not in constraints and (new_x, new_y) not in visited:
                    edist = math.dist([new_x, new_y], [goal[0], goal[1]])
                    fringe.update({(new_x, new_y): edist})
                    visited.append((new_x, new_y))
                    parent[(new_x, new_y)] = smallest_key

            sorted_list = [k for k, _ in sorted(fringe.items(), key=lambda item: item[1])]

        # No path found
        return -1

    # Senses if the button is within the radius of the bot
    def sense_action(self):
        self.actions_counter += 1
        if any(cell == self.leak for cell in self.get_detection_square()):
            return True
        else:
            return False

    # Obtains the radius of the bot within ship bounds
    def get_detection_square(self):
        detection_square = []
        for x in range(self.bot[0] - k_val, self.bot[0] + k_val + 1):
            for y in range(self.bot[1] - k_val, self.bot[1] + k_val + 1):
                if 0 <= x < self.D and 0 <= y < self.D and self.ship[x][y] != 'X':
                    detection_square.append((x, y))
        return detection_square

    # Obtains the closest square to the leak
    def find_closest_square(self):
        closest_square = None
        closest_distance = float('inf')

        for x in range(self.bot[0] - self.k_val, self.bot[0] + self.k_val + 1):
            for y in range(self.bot[1] - self.k_val, self.bot[1] + self.k_val + 1):
                if (x, y) != self.bot and 0 <= x < self.D and 0 <= y < self.D:
                    dx = self.leak[0] - x
                    dy = self.leak[1] - y
                    distance = abs(dx) + abs(dy)

                    if distance < closest_distance:
                        closest_square = (x, y)
                        closest_distance = distance
        return closest_square

    def run_bot_1(self):
        # Initialize a set to keep track of visited locations
        visited = set()

        while self.bot != self.leak:
            if self.sense_action():
                print("Leak found")
                # Leak is in the detection square, search for it
                for x in range(self.bot[0] - self.k_val, self.bot[0] + self.k_val + 1):
                    for y in range(self.bot[1] - self.k_val, self.bot[1] + self.k_val + 1):
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D:
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
                valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < self.D and 0 <= y < self.D]
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
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = visited.pop()
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    print(f"Backtracking to location ({self.bot[0]}, {self.bot[1]})")
                    self.actions_counter += 1
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
                        if (x, y) not in visited and 0 <= x < self.D and 0 <= y < self.D:
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
                x,y = self.find_closest_square()
                dx = self.leak[0] - x
                dy = self.leak[1] - y

                # Try to move closer to the leak
                if abs(dx) > abs(dy):
                    new_location = (self.bot[0] + (1 if dx > 0 else -1), self.bot[1])
                else:
                    new_location = (self.bot[0], self.bot[1] + (1 if dy > 0 else -1))

                # Ensure the new location is within the grid
                if 0 <= new_location[0] < self.D and 0 <= new_location[1] < self.D:
                    print(f"Moving to location ({new_location[0]}, {new_location[1]})")
                    visited.add(self.bot)
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = new_location
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                else:
                    # If moving in the calculated direction is not possible, backtrack to a visited cell
                    self.ship[self.bot[0]][self.bot[1]] = 'O'
                    self.bot = visited.pop()
                    self.ship[self.bot[0]][self.bot[1]] = self.colored_block('c')
                    print(f"Back tracking to location ({self.bot[0]}, {self.bot[1]})")
                    self.actions_counter += 1
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
        
        dist_matrix = [-1 * self.D for _ in range(self.D)]
        
        # first compute each location's distance, if no path/
        for i in range(self.D):
            for j in range(self.D):
                if self.ship[i][j] != 'X':
                    start = (i, j)
                    steps_to_leak = self.find_shortest_path(start=start, goal=self.leak)
                    dist_matrix[i][j] = steps_to_leak


        while self.bot != self.leak:
        # the higher the alpha, the lower the beep prob

            bot_leak_steps = self.find_shortest_path(self.bot, self.leak)
            beep_prob = math.exp(-alpha * (bot_leak_steps -1))
            random_val = random.random()
            # if there is a beep
            if beep_prob > random_val:
                # go through each of the matrix prob and update it with changing factor of distance
                # p_leak[x][y] = p_beep[x][y] * p_leak[x][y]/ p_beep |[bot.x][bot.y]
                # prob of leak = that matrix prob * curr prob of leak at that location / prob of leak at bot location
                
                self.actions_counter += 1
                # Leak is in the detection square, search for it
                pass
            else:
                pass
        #now the run_bot_3 itself is pretty simple:
        #while (bot's position != leaks position)

            #set the current position probability to 0
        
            #start by performing a sense action (THIS SHOULD BE A HELPER FUNCTION)
            #sense++

            #for each (open) direction that the bot can move, organize their probabilities in descending order
                #select the one that has the highest probability of containing the leak for the new position of the Bot
                #move++
                
        #theres an edge case where you might get stuck at a dead end with probabilities of 0 all around you, if this happens, then run the shortest path from your current
        #position to the highest probability position adjacent to the 0s 
        # this should give you a path with X amounts of Steps
        # move += X; 
        
        pass

    def run_bot_5(self, k_val):
        pass
    
    def run_bot_6(self, k_val):
        pass
    
    def run_bot_7(self, k_val):
        pass
    
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

    ans = int(input("Which bot do you want to run?\n1.Bot 1\n2.Bot 2\n3.Bot 3\n4.Bot 4\nBot: "))

    if ans == 1:
        ship.run_bot_1()
    elif ans == 2:
        ship.run_bot_2()
    elif ans == 3:
        ship.run_bot_3(k_val)
    elif ans == 4:
        ship.run_bot_4(k_val)
    elif ans == 5:
        ship.run_bot_5(k_val)
    elif ans == 6:
        ship.run_bot_6(k_val)
    elif ans == 7:
        ship.run_bot_7(k_val)
    elif ans == 8:
        ship.run_bot_8(k_val)
    elif ans == 9:
        ship.run_bot_9(k_val)
    else:
        print("Invalid bot choice.")
