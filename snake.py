import tkinter as tk
import random

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20
SPEED = 120


# Colors
BG_COLOR = "black"
SNAKE_COLOR = "green"
FOOD_COLOR = "red"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        # Allow minimizing and maximizing with dynamic resizing
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(400, 400)
        self.root.maxsize(900, 900)
        
        self.canvas = tk.Canvas(root, bg=BG_COLOR, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.score = 0
        self.direction = 'Right'
        self.running = True
        self.paused = False

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.generate_food()

        self.draw_elements()
        self.root.bind('<KeyPress>', self.change_direction)
        self.root.bind('<space>', self.toggle_pause)
        self.update_game()

        # Buttons
        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack(side="left")

        self.new_game_button = tk.Button(root, text="New Game", command=self.new_game)
        self.new_game_button.pack(side="right")

    def draw_elements(self):
        self.canvas.delete('all')

        # Draw snake with head highlighted
        for i, (x, y) in enumerate(self.snake):
            color = "darkgreen" if i == 0 else SNAKE_COLOR
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=color)

        # Draw food like an apple
        fx, fy = self.food
        self.canvas.create_oval(fx, fy, fx + CELL_SIZE, fy + CELL_SIZE, fill=FOOD_COLOR)
        self.canvas.create_text(fx + CELL_SIZE / 2, fy + CELL_SIZE / 2, text="🍎", font=("Arial", 12))

        # Draw score
        self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 14))

    def generate_food(self):
        while True:
            x = random.randint(0, (WINDOW_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (WINDOW_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, event):
        if self.paused:
            return
        new_direction = event.keysym
        all_directions = {'Up', 'Down', 'Left', 'Right'}
        opposites = {('Up', 'Down'), ('Left', 'Right')}

        if new_direction in all_directions and (self.direction, new_direction) not in opposites:
            self.direction = new_direction

    def toggle_pause(self, event=None):
        if self.running:
            self.paused = not self.paused
            if self.paused:
                self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text="Paused", fill="white", font=("Arial", 30))
            else:
                self.update_game()

    def update_game(self):
        if not self.running or self.paused:
            return

        head_x, head_y = self.snake[0]

        if self.direction == 'Up':
            head_y -= CELL_SIZE
        elif self.direction == 'Down':
            head_y += CELL_SIZE
        elif self.direction == 'Left':
            head_x -= CELL_SIZE
        elif self.direction == 'Right':
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        # Collision with walls or itself
        if (head_x < 0 or head_x >= WINDOW_WIDTH or
            head_y < 0 or head_y >= WINDOW_HEIGHT or
            new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Check for food
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.draw_elements()
        self.root.after(SPEED, self.update_game)

    def game_over(self):
        self.running = False
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text="Game Over", fill="white", font=("Arial", 30))
        self.canvas.create_text(WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) + 40, text=f"Final Score: {self.score}", fill="white", font=("Arial", 20))

    def restart_game(self):
        self.running = True
        self.paused = False
        self.direction = 'Right'
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.generate_food()
        self.score = 0
        self.draw_elements()
        self.update_game()

    def new_game(self):
        self.restart_game()
        self.score = 0
        self.running = True

# Initialize game
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()