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
        if any(cell == self.leak for cell in self.get_detection_square()):
            print("Leak detected in the detection square or the current square.")
            return True
        else:
            print("No leak detected in the detection square or the current square.")
            return False
        
    def get_detection_square(self):
        detection_square = []
        k_val = int(self.k_val) 
        for x in range(self.bot[0] - k_val, self.bot[0] + k_val + 1):
            for y in range(self.bot[1] - k_val, self.bot[1] + k_val + 1):
                if 0 <= x < self.D and 0 <= y < self.D:
                    detection_square.append((x, y))
        return detection_square



    def run_bot_1(self):
        detection_square = self.get_detection_square()
        leak_detected = self.sense_action()
        
        print(detection_square)
        print(leak_detected)

            
    def run_bot_2(self, k_val):
        pass

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
    k_val= float(input("Enter k value: "))
    ship.k_val = k_val
    ship.generate_ship()
    print(ship)

    ans = int(input("Which bot do you want to run?\n1.Bot 1\n2.Bot 2\n3.Bot 3\n4.Bot 4\nBot: "))

    if ans == 1:
        ship.run_bot_1()
    elif ans == 2:
        ship.run_bot_2(k_val)
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
