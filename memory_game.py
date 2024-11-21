'''
This is the code for the memory game.
The game consists of a grid of cards, each with a front and back image. The player must match pairs of cards by flipping them over and revealing their faces. The game ends when all pairs have been matched or when the player runs out of moves.
The game is played on a 4x3 grid, with each card having a unique image. The game can be played with 8, 10, or 12 cards. The player can choose a card set (default, dog, or programming languages) and the number of cards to play with.
'''

# Import necessary modules
import turtle
import random
import os
import configparser

class Card:
    '''
    Represents a single card in the memory game.
    '''
    def __init__(self, x, y, front_image, back_image):
        '''
        Initializes a card with its position, front image, and back image.
        '''
        self.front_image = front_image
        self.back_image = back_image
        self.turtle = turtle.Turtle()
        self.turtle.shape(self.back_image)
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.is_flipped = False
        self.is_matched = False
        self.width = 70  # Width of the card
        self.height = 100  # Height of the card

    def flip(self):
        '''
        Flips the card to show either the front or back image.
        '''
        if not self.is_flipped:
            self.turtle.shape(self.front_image)
            self.is_flipped = True
        else:
            self.turtle.shape(self.back_image)
            self.is_flipped = False

    def match(self):
        '''
        Marks the card as matched.
        '''
        self.is_matched = True

    def hide(self):
        '''
        Hides the card and marks it as matched.
        '''
        self.turtle.hideturtle()
        self.is_matched = True

    def contains_point(self, x, y):
        '''
        Checks if a given point (x, y) is within the card's area.
        '''
        return self.turtle.distance(x, y) < 50

class MemoryGame:
    '''
    Represents the memory game, including logic and UI management.
    '''
    def __init__(self):
        '''
        Initializes the game screen, player data, and cards.
        '''
        # Load configuration data
        self.config = configparser.ConfigParser()
        self.config.read("config.txt")
        # Initialize the screen
        self.screen = turtle.Screen()
        self.screen.setup(width=600, height=800)
        self.screen.title("Memory Game")
        self.screen.bgcolor("white")
        # Load leaderboard data
        self.leaderboard_file = "leaderboard.txt"
        self.leaderboard = self.load_leaderboard()
        
        # Register message images
        self.screen.register_shape("assets/messages/winner.gif")
        self.screen.register_shape("assets/messages/quitmsg.gif")
        self.screen.register_shape("assets/messages/leaderboard_error.gif")
        self.screen.register_shape("assets/messages/file_error.gif")
        self.screen.register_shape("assets/messages/card_warning.gif")
        self.screen.register_shape("assets/banner.gif")
        # Prevents multiple clicks during animations
        self.click_lock = False  
        
        # Collect player input
        self.player_name = self.screen.textinput("Welcome!", "Enter your name (or leave blank for anonymous):")
        if not self.player_name:
            self.player_name = "Anonymous"
        self.card_set = self.choose_card_set()
        self.card_count = self.choose_card_count()
        
        # Draw game UI components
        self.draw_banner()
        self.draw_panel()
        
        # Initialize status
        self.status = turtle.Turtle()
        self.status.hideturtle()
        self.status.penup()
        self.status.goto(-300, -240)
        self.moves = 0
        self.matches = 0
        
        # Initialize quit button
        self.quit_button = turtle.Turtle()
        self.screen.register_shape("assets/buttons/quitbutton.gif")
        self.quit_button.shape("assets/buttons/quitbutton.gif")
        self.quit_button.penup()
        self.quit_button.goto(200, -280)
  
        self.quit_button.onclick(self.handle_quit)  # Handle quit button clicks
        self.screen.onclick(self.handle_click)  # Handle clicks on the screen
        
        # Initialize new game button
        self.new_game_button = turtle.Turtle()
        self.screen.register_shape("assets/buttons/newgame.gif") 
        self.new_game_button.shape("assets/buttons/newgame.gif")
        self.new_game_button.penup()
        self.new_game_button.goto(200, -340)  
        self.new_game_button.onclick(self.handle_new_game)  
        
        # Set up card back image
        self.back_image = f"assets/cards/{self.card_set}/card_back.gif"
        if not os.path.exists(self.back_image):
            raise FileNotFoundError(f"Back image not found: {self.back_image}")
        self.screen.register_shape(self.back_image)
        
        # Create cards
        self.cards = []
        self.selected_cards = []
        self.create_cards()
        
        # Update game status
        self.update_status(self.moves, self.matches)

    def draw_panel(self):
        '''
        Draws the game panel, including the game area and leaderboard.
        '''
        panel_drawer = turtle.Turtle()
        panel_drawer.hideturtle()
        panel_drawer.penup()
        panel_drawer.goto(-280, 250) 
        panel_drawer.pendown()
        panel_drawer.pensize(5)

        # Draw game area
        for _ in range(2):
            panel_drawer.forward(430)
            panel_drawer.right(90)
            panel_drawer.forward(500) 
            panel_drawer.right(90)

        # Draw leaderboard area
        panel_drawer.penup()
        panel_drawer.goto(170, 250)
        panel_drawer.pendown()
        panel_drawer.color("blue")  
        panel_drawer.forward(100)
        panel_drawer.right(90)
        panel_drawer.forward(500)
        panel_drawer.right(90)
        panel_drawer.forward(100)
        panel_drawer.right(90)
        panel_drawer.forward(500)

        # Draw status bar
        panel_drawer.penup()
        panel_drawer.goto(-280, -370)
        panel_drawer.pendown()
        panel_drawer.color("black") 
        panel_drawer.forward(100)
        panel_drawer.right(90)
        panel_drawer.forward(430)
        panel_drawer.right(90)
        panel_drawer.forward(100)
        panel_drawer.right(90)
        panel_drawer.forward(430)

        # Add leaderboard title
        panel_drawer.penup()
        panel_drawer.color("blue")
        panel_drawer.goto(190, 230)
        panel_drawer.write("Leaders:", font=("Arial", 16, "bold"))

        # Display leaderboard
        self.display_leaderboard()

    def choose_card_set(self):
        '''
        Prompt the user to select a card set using a number based on the configuration file.
        '''
        # Get the available card sets from the config file
        card_sets = list(self.config.sections())
        
        # Dynamically create the prompt message with numbers
        prompt_message = "Choose a card set by number:\n"
        for index, card_set in enumerate(card_sets, start=1):
            prompt_message += f"{index}. {card_set}\n"
        prompt_message += "Leave blank or enter an invalid number for default."
        
        # Show the prompt to the user
        card_set_choice = self.screen.textinput("Card Set", prompt_message)
        
        try:
            # Convert the input to an integer and get the corresponding card set
            card_set_index = int(card_set_choice) - 1
            if 0 <= card_set_index < len(card_sets):
                return card_sets[card_set_index]
        except (ValueError, TypeError):
            pass  # Invalid input or blank, fall back to default

            # Default to 'default' card set if input is invalid or blank
        return "default"


    def choose_card_count(self):
        '''
        Prompts the user to select the number of cards and ensures valid input.
        '''
        valid_input = False
        while not valid_input:
            card_count = self.screen.textinput(
                "Card Count",
                "Choose the number of cards to play with (8, 10, 12).\nDefault is 10 if left blank."
            )
            try:
                if not card_count:
                    return 10
                card_count = int(card_count)
                if card_count < 8:
                    self.display_error_message("Minimum value is 8. Please try again.")
                elif card_count > 12:
                    self.display_error_message("Maximum value is 12. Please try again.")
                elif card_count % 2 != 0:
                    self.display_message("assets/messages/card_warning.gif")
                    valid_input = True
                    return card_count + 1
                else:
                    valid_input = True
                    return card_count
            except ValueError:
                self.display_error_message("Invalid input. Please enter a valid number (e.g., 8, 10, 12).")


    def display_error_message(self, message):
        '''
        Displays an error message on the screen for a short time.
        '''
        error_writer = turtle.Turtle()
        error_writer.hideturtle()
        error_writer.penup()
        error_writer.goto(0, -190) 
        error_writer.color("red")
        error_writer.write(message, align="center", font=("Arial", 12, "bold"))
        self.screen.ontimer(error_writer.clear, 1000)  # Clears message after 1 second

    def get_card_images(self):
        '''
        Retrieve card images based on the selected set from the configuration file.
        '''
        path = self.config[self.card_set]['path']
        images = [
            f"{path}/{file}" for file in os.listdir(path)
            if file.endswith(".gif") and file != "card_back.gif"
        ]
        for image in images:
            self.screen.register_shape(image)
        return images

    def create_cards(self):
        '''
        Creates the card objects and arranges them in a grid, shuffling the images.
        '''
        card_images = self.get_card_images()[:self.card_count // 2] * 2
        random.shuffle(card_images)

        # Determine grid layout
        cols = 4  # Fixed number of columns
        start_x, start_y = -220, 170  # Starting position for grid
        x_spacing, y_spacing = 100, 150  # Spacing between cards

        # Create card objects
        for index, front in enumerate(card_images):
            row, col = divmod(index, cols)
            x = start_x + col * x_spacing
            y = start_y - row * y_spacing
            card = Card(x, y, front, self.back_image)
            self.cards.append(card)

    def update_status(self, moves, matches):
        '''
        Updates the status bar with the current game stats.
        '''
        self.status.clear()
        self.status.penup()
        self.status.goto(-220, -300)
        self.status.write(
            f"Player: {self.player_name} | Moves: {moves} | Matches: {matches}",
            font=("Arial", 16, "bold")
        )

    def handle_click(self, x, y):
        '''
        Handles screen clicks to flip cards and check for matches.
        '''
        if self.click_lock:  # Ignore clicks while animations are running
            return

        # Ignore clicks on the quit button
        if 200 - 50 < x < 200 + 50 and -300 - 30 < y < -300 + 30:
            return

        for card in self.cards:
            if card.contains_point(x, y) and not card.is_matched and card not in self.selected_cards:
                card.flip()
                self.selected_cards.append(card)
                if len(self.selected_cards) == 2:  # Check match if two cards are flipped
                    self.click_lock = True
                    self.screen.ontimer(self.check_match, 500)  # Delay before checking match
                    self.moves += 1
                    self.update_status(self.moves, self.matches)
                break

    def check_match(self):
        '''
        Checks if the flipped cards match and handles the result.
        '''
        if len(self.selected_cards) == 2:
            card1, card2 = self.selected_cards
            if card1.front_image == card2.front_image:
                card1.hide()
                card2.hide()
                self.matches += 1
            else:
                card1.flip()
                card2.flip()
            self.selected_cards = []
            self.update_status(self.moves, self.matches)
            self.check_game_won()  # Check if the game is won
            self.click_lock = False

    def run(self):
        '''
        Starts the game loop, listening for events.
        '''
        self.screen.mainloop()

    def display_message(self, message_image):
        '''
        Displays a message image in the center of the screen.
        '''
        message_turtle = turtle.Turtle()
        message_turtle.hideturtle()
        message_turtle.shape(message_image)
        message_turtle.penup()
        message_turtle.goto(0, 0)
        message_turtle.showturtle()
        self.screen.ontimer(lambda: message_turtle.hideturtle(), 3000)  # Hide message after 3 seconds

    def check_game_won(self):
        '''
        Checks if all cards are matched and displays a winning message.
        '''
        if all(card.is_matched for card in self.cards):
            self.display_message("assets/messages/winner.gif")
            self.update_leaderboard(self.moves)
            self.screen.ontimer(lambda: self.screen.bye(), 3000)  # Exit game after 3 seconds

    def handle_file_error(self, file_type):
        '''
        Displays an error message for file-related issues.
        '''
        if file_type == "leaderboard":
            self.display_message("assets/messages/leaderboard_error.gif")
        elif file_type == "config":
            self.display_message("assets/messages/file_error.gif")

    def handle_quit(self, x, y):
        '''
        Handles quit button clicks, displays a quit message, and exits the game.
        '''
        self.quit_button.onclick(None)  # Disable quit button
        self.display_message("assets/messages/quitmsg.gif")
        self.screen.ontimer(lambda: self.screen.bye(), 3000)  # Exit game after 3 seconds

    def load_leaderboard(self):
        '''
        Loads the leaderboard from a file and returns the top scores.
        '''
        if not os.path.exists(self.leaderboard_file):
            return []
        
        with open(self.leaderboard_file, "r") as file:
            lines = file.readlines()
        leaderboard = []
        for line in lines:
            try:
                moves, name = line.strip().split(", ")
                leaderboard.append((int(moves), name))
            except ValueError:
                continue
        return sorted(leaderboard)[:5]  # Return top 5 scores

    def update_leaderboard(self, moves):
        '''
        Updates the leaderboard with the current player's score.
        '''
        self.leaderboard.append((moves, self.player_name))
        self.leaderboard = sorted(self.leaderboard)[:5]  # Keep only top 5 scores

        with open(self.leaderboard_file, "w") as file:
            for score, name in self.leaderboard:
                file.write(f"{score}, {name}\n")

    def display_leaderboard(self):
        '''
        Displays the leaderboard on the screen.
        '''
        leaderboard_writer = turtle.Turtle()
        leaderboard_writer.hideturtle()
        leaderboard_writer.penup()
        leaderboard_writer.goto(185, 150)

        for i, (moves, name) in enumerate(self.leaderboard):
            leaderboard_writer.goto(180, 150 - i * 60)
            leaderboard_writer.write(f"No.{i + 1}\n{name}: \n{moves} moves\n---", font=("Arial", 14, "normal"))

    def draw_banner(self):
        '''
        Draws the title banner at the top of the screen.
        '''
        self.screen.register_shape("assets/banner.gif")
        title_turtle = turtle.Turtle()
        title_turtle.shape("assets/banner.gif")
        title_turtle.penup()
        title_turtle.goto(0, 350)
    def handle_new_game(self, x, y):
        '''
        Handles the New Game button click event.
        Restarts the game by resetting all the states.
        '''
        self.screen.clearscreen()  # 清空屏幕
        main()  # 重新调用主程序，开始新游戏
        
def main():
    '''
    Main function to initialize and run the memory game.
    '''
    game = MemoryGame()
    game.run()

if __name__ == "__main__":
    main()
