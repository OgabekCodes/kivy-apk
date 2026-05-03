import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock

Window.fullscreen = True

TILE = 60
SIZE = 8

# --------------------
# MAZE
# --------------------
def generate_maze():
    maze = [[1 for _ in range(SIZE)] for _ in range(SIZE)]

    for y in range(1, SIZE - 1):
        for x in range(1, SIZE - 1):
            maze[y][x] = 0 if random.random() > 0.3 else 1

    maze[1][1] = 0
    maze[SIZE - 2][SIZE - 2] = 2

    return maze


# --------------------
# MENU
# --------------------
class MenuScreen(Screen):
    def on_key_down(self, key, *args):
        if key == 13:
            self.manager.current = "game"


# --------------------
# GAME
# --------------------
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.level = 1
        self.stars = 0

        self.load_level()

        Window.bind(on_key_down=self.key_action)
        Clock.schedule_interval(self.update, 1 / 10)

    # ---------------- SAFE CHECK ----------------
    def safe_cell(self, x, y):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            return self.maze[y][x]
        return 1  # devor

    # ---------------- LEVEL ----------------
    def load_level(self):
        self.maze = generate_maze()
        self.player_x = 1
        self.player_y = 1

        self.enemy_x = SIZE - 2
        self.enemy_y = SIZE - 2

    # ---------------- DRAW ----------------
    def draw(self):
        self.canvas.clear()
        with self.canvas:

            for y in range(SIZE):
                for x in range(SIZE):
                    if self.maze[y][x] == 1:
                        Color(0, 0.7, 1)
                        Rectangle(pos=(x * TILE, y * TILE), size=(TILE, TILE))

                    if self.maze[y][x] == 2:
                        Color(0, 1, 0)
                        Rectangle(pos=(x * TILE, y * TILE), size=(TILE, TILE))

            # Enemy
            Color(1, 0, 0)
            Rectangle(pos=(self.enemy_x * TILE, self.enemy_y * TILE), size=(TILE, TILE))

            # Player
            Color(1, 1, 0)
            Rectangle(pos=(self.player_x * TILE, self.player_y * TILE), size=(TILE, TILE))

    # ---------------- MOVE ----------------
    def move(self, dx, dy):
        nx = self.player_x + dx
        ny = self.player_y + dy

        if self.safe_cell(nx, ny) != 1:
            self.player_x = nx
            self.player_y = ny
            self.stars += 1

        # WIN
        if self.safe_cell(nx, ny) == 2:
            self.level += 1
            self.load_level()

        # LOSE
        if self.player_x == self.enemy_x and self.player_y == self.enemy_y:
            self.load_level()

    # ---------------- ENEMY ----------------
    def enemy_move(self):
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        nx = self.enemy_x + dx
        ny = self.enemy_y + dy

        if self.safe_cell(nx, ny) != 1:
            self.enemy_x = nx
            self.enemy_y = ny

    # ---------------- KEY ----------------
    def key_action(self, window, key, *args):
        if key == 273:
            self.move(0, 1)
        elif key == 274:
            self.move(0, -1)
        elif key == 275:
            self.move(1, 0)
        elif key == 276:
            self.move(-1, 0)
        elif key == 13:
            self.manager.current = "menu"

    # ---------------- LOOP ----------------
    def update(self, dt):
        self.enemy_move()
        self.draw()


# --------------------
# APP
# --------------------
class MazeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.current = "menu"
        return sm

        
MazeApp().run()