import random

class Ship():
    def __init__(self):
        try:
            self.D = int(input("Enter D x D Dimension: "))
        except ValueError:
            print("Needs to be an int")
            exit()

        # Up, down, left, right
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        self.ship = [['O'] * self.D for _ in range(self.D)]

        # Initialize bot and leak positions
        self.bot = (-1, -1)
        self.leak = (-1, -1)
        self.k_val = 0
        self.actions_counter = 0
        
    def __repr__(self):
        ship_str = ""
        for x in range(self.D):
            for y in range(self.D):
                cell = self.ship[x][y]
                if (x >= self.bot[0] - self.k_val) and (x <= self.bot[0] + self.k_val) and \
                (y >= self.bot[1] - self.k_val) and (y <= self.bot[1] + self.k_val):
                    if (x, y) != self.bot:
                        ship_str += '[' + "-" + ']'
                    else:
                        ship_str += '[' + cell + ']'
                else:
                    ship_str += '[' + cell + ']'
            ship_str += '\n'
        return ship_str


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

    def generate_ship(self):
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
                    
    def sense_action(self):  
        
        self.actions_counter += 1
        if any(cell == self.leak for cell in self.get_detection_square()):
            return True
        else:
            return False
        
    def get_detection_square(self):
        detection_square = []
        for x in range(self.bot[0] - k_val, self.bot[0] + k_val + 1):
            for y in range(self.bot[1] - k_val, self.bot[1] + k_val + 1):
                if 0 <= x < self.D and 0 <= y < self.D:
                    detection_square.append((x, y))
        return detection_square


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
            if self.actions_counter % 5 == 0:
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
            dx = self.leak[0] - self.bot[0]
            dy = self.leak[1] - self.bot[1]

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
                print(f"Backtracking to location ({self.bot[0]}, {self.bot[1]})")
            self.actions_counter += 1
            print(self)


    def run_bot_3(self, k_val):
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
