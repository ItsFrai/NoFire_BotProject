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

    def __repr__(self):
        ship_str = ""
        for row in self.ship:
            ship_str += '[' + ' '.join(row) + ']\n'
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
                self.ship[rand_x_coord][rand_y_coord] = self.colored_block('g')
                self.leak = (rand_x_coord, rand_y_coord)

    def run_bot_1(self, probability):
        pass

    def run_bot_2(self, probability):
        pass

    def run_bot_3(self, probability):
        pass

    def run_bot_5(self, probability):
        pass
    
    def run_bot_6(self, probability):
        pass
    
    def run_bot_7(self, probability):
        pass
    
    def run_bot_8(self, probability):
        pass
    
    def run_bot_9(self, probability):
        pass

if __name__ == "__main__":
    ship = Ship()
    ship.generate_ship()
    print(ship)

    ans = int(input("Which bot do you want to run?\n1.Bot 1\n2.Bot 2\n3.Bot 3\n4.Bot 4\nBot: "))
    prob = float(input("What is the probability: "))

    if ans == 1:
        ship.run_bot_1(prob)
    elif ans == 2:
        ship.run_bot_2(prob)
    elif ans == 3:
        ship.run_bot_3(prob)
    elif ans == 4:
        ship.run_bot_4(prob)
    elif ans == 5:
        ship.run_bot_5(prob)
    elif ans == 6:
        ship.run_bot_6(prob)
    elif ans == 7:
        ship.run_bot_7(prob)
    elif ans == 8:
        ship.run_bot_8(prob)
    elif ans == 9:
        ship.run_bot_9(prob)
    else:
        print("Invalid bot choice.")
