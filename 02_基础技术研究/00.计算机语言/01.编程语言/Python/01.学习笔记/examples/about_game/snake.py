import tkinter as tk
import random

CELL_SIZE = 25
GRID_WIDTH = 20
GRID_HEIGHT = 15
FPS = 10


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("贪吃蛇")
        self.window.geometry(f"{GRID_WIDTH * CELL_SIZE}x{GRID_HEIGHT * CELL_SIZE + 50}")
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, bg="#c8f7c8")
        self.canvas.pack()

        self.score_label = tk.Label(self.window, text="得分: 0", font=("Arial", 14, "bold"), bg="#e8f8e8")
        self.score_label.pack(fill=tk.X)

        self.start_btn = tk.Button(self.window, text="开始", font=("Arial", 12), command=self.start_game)
        self.start_btn.pack(pady=5)

        self.canvas.bind("<KeyPress>", self.key_press)
        self.canvas.focus_set()

        self.snake = []
        self.direction = "Right"
        self.food = None
        self.score = 0
        self.running = False
        self.job = None

        self.draw_grid()
        self.spawn_food()

    def draw_grid(self):
        self.canvas.delete("grid")
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                self.canvas.create_rectangle(
                    x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                    (x + 1) * CELL_SIZE - 1, (y + 1) * CELL_SIZE - 1,
                    outline="#90d090", tags="grid"
                )

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def draw(self):
        self.canvas.delete("snake", "food")
        if self.food:
            fx, fy = self.food
            self.canvas.create_oval(
                fx * CELL_SIZE + 3, fy * CELL_SIZE + 3,
                (fx + 1) * CELL_SIZE - 3, (fy + 1) * CELL_SIZE - 3,
                fill="#ff6464", tags="food"
            )
        for i, (x, y) in enumerate(self.snake):
            color = "#228b22" if i == 0 else "#90ee90"
            self.canvas.create_oval(
                x * CELL_SIZE + 2, y * CELL_SIZE + 2,
                (x + 1) * CELL_SIZE - 2, (y + 1) * CELL_SIZE - 2,
                fill=color, tags="snake"
            )

    def start_game(self):
        if self.job:
            self.window.after_cancel(self.job)
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = "Right"
        self.score = 0
        self.score_label.config(text=f"得分: {self.score}")
        self.running = True
        self.spawn_food()
        self.draw()
        self.tick()

    def tick(self):
        if not self.running:
            return
        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - 1)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 1)
        elif self.direction == "Left":
            new_head = (head[0] - 1, head[1])
        else:
            new_head = (head[0] + 1, head[1])

        x, y = new_head
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT or new_head in self.snake:
            self.running = False
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2, GRID_HEIGHT * CELL_SIZE // 2,
                text=f"游戏结束\n得分: {self.score}", font=("Arial", 20, "bold"),
                fill="#ff0000", justify=tk.CENTER, tags="gameover"
            )
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f"得分: {self.score}")
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw()
        self.job = self.window.after(1000 // FPS, self.tick)

    def key_press(self, event):
        key = event.keysym
        opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if key in opposite and key != opposite.get(self.direction):
            self.direction = key
        elif key == "space" and not self.running:
            self.start_game()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    SnakeGame().run()