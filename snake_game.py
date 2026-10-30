
import random
import turtle



WIDTH = 700
HEIGHT = 700
GRID = 20
WALL_LIMIT = 280
HIGH_SCORE_FILE = "snake_high_score.txt"

DIFFICULTIES = {
    "Easy": 180,
    "Medium": 130,
    "Hard": 90
}

# -------------------- GAME WINDOW --------------------

screen = turtle.Screen()
screen.title("SnakeX - Advanced Python Snake Game")
screen.bgcolor("black")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)

# -------------------- SNAKE HEAD --------------------

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# -------------------- FOOD --------------------

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food_kind = "normal"

# -------------------- SCORE DISPLAY --------------------

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()

# -------------------- GAME VARIABLES --------------------

segments = []
obstacles = []

score = 0
level = 1
ticks = 0
slow_until_tick = 0

difficulty = "Medium"
base_delay = DIFFICULTIES[difficulty]

state = "menu"
game_over_message = "GAME OVER"

# -------------------- HIGH SCORE --------------------

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


high_score = load_high_score()


def save_high_score():
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(high_score))
    except OSError:
        pass


# -------------------- POSITIONS --------------------

def get_occupied_positions(include_food=False):
    occupied = [tuple(head.position())]

    for segment in segments:
        occupied.append(tuple(segment.position()))

    occupied.extend(obstacles)

    if include_food:
        occupied.append(tuple(food.position()))

    return occupied


def random_position(occupied=None):
    if occupied is None:
        occupied = get_occupied_positions()

    occupied = set(occupied)

    available = [
        (x, y)
        for x in range(-260, 261, GRID)
        for y in range(-260, 261, GRID)
        if (x, y) not in occupied
    ]

    if not available:
        return None

    return random.choice(available)


def spawn_food():
    global food_kind, state, game_over_message

    position = random_position(get_occupied_positions())

    if position is None:
        state = "gameover"
        game_over_message = "YOU WIN!"
        return

    food.goto(position)

    chance = random.random()

    if chance < 0.15:
        food_kind = "bonus"
        food.color("gold")
        food.shapesize(1.2, 1.2)
    elif chance < 0.30:
        food_kind = "slow"
        food.color("deepskyblue")
        food.shapesize(1.2, 1.2)
    else:
        food_kind = "normal"
        food.color("red")
        food.shapesize(1, 1)


# -------------------- OBSTACLES --------------------

def add_obstacles(amount):
    for _ in range(amount):
        position = random_position(
            get_occupied_positions(include_food=True)
        )

        if position is None:
            return

        obstacles.append(position)

        block = turtle.Turtle()
        block.speed(0)
        block.shape("square")
        block.color("gray")
        block.penup()
        block.goto(position)


def clear_obstacles():
    global obstacles

    # Remove the visible obstacle turtles by
    # clearing the screen's turtle objects is not needed.
    # Each obstacle is stored as a coordinate.
    obstacles = []


# -------------------- DISPLAY --------------------

def write_line(y, message, size=16, color="white",
               style="normal"):
    pen.goto(0, y)
    pen.color(color)
    pen.write(
        message,
        align="center",
        font=("Arial", size, style)
    )


def draw_display():
    pen.clear()

    if state == "menu":
        write_line(190, "SNAKEX", 36, "lime", "bold")
        write_line(140, "ADVANCED PYTHON SNAKE GAME", 16)
        write_line(75, "Choose Difficulty", 20, "gold", "bold")
        write_line(35, "1 - Easy     2 - Medium     3 - Hard", 16)
        write_line(-20, "Press ENTER to Start", 18, "lime", "bold")
        write_line(-75, "Arrow Keys or W A S D to Move", 14)
        write_line(-110, "SPACE = Pause / Resume", 14)
        write_line(-145, "R = Restart     M = Main Menu", 14)
        write_line(-205, "Red: +10   Gold: +50   Blue: Slow Power-Up",
                   13, "cyan")
        write_line(-260, f"High Score: {high_score}", 18, "gold")

    elif state in ("playing", "paused"):
        write_line(
            315,
            f"Score: {score}   Best: {high_score}   "
            f"Level: {level}   Mode: {difficulty}",
            14,
            "white",
            "bold"
        )

        write_line(
            290,
            "Red +10 | Gold +50 | Blue slows the snake",
            11,
            "cyan"
        )

        if state == "paused":
            write_line(50, "PAUSED", 32, "gold", "bold")
            write_line(0, "Press SPACE to Resume", 17)

    elif state == "gameover":
        write_line(130, game_over_message, 34, "red", "bold")
        write_line(65, f"Your Score: {score}", 22)
        write_line(25, f"High Score: {high_score}", 20, "gold")
        write_line(-40, "Press R to Play Again", 18, "lime", "bold")
        write_line(-80, "Press M for Main Menu", 16)


# -------------------- RESET GAME --------------------

def reset_game():
    global score, level, ticks, slow_until_tick

    score = 0
    level = 1
    ticks = 0
    slow_until_tick = 0

    head.goto(0, 0)
    head.direction = "stop"

    for segment in segments:
        segment.hideturtle()
        segment.goto(1000, 1000)

    segments.clear()

    # Hide old obstacles before removing their coordinates.
    for item in screen.turtles():
        if item.shape() == "square" and item is not head:
            if item is not pen:
                item.hideturtle()

    clear_obstacles()

    spawn_food()


def start_game():
    global state, base_delay, game_over_message

    base_delay = DIFFICULTIES[difficulty]
    reset_game()

    game_over_message = "GAME OVER"
    state = "playing"

    draw_display()
    screen.update()


def show_menu():
    global state

    head.direction = "stop"
    state = "menu"
    draw_display()
    screen.update()


def end_game(message="GAME OVER"):
    global state, game_over_message

    head.direction = "stop"
    state = "gameover"
    game_over_message = message

    save_high_score()
    draw_display()
    screen.update()


# -------------------- DIFFICULTY --------------------

def choose_easy():
    global difficulty, base_delay

    if state == "menu":
        difficulty = "Easy"
        base_delay = DIFFICULTIES[difficulty]
        draw_display()
        screen.update()


def choose_medium():
    global difficulty, base_delay

    if state == "menu":
        difficulty = "Medium"
        base_delay = DIFFICULTIES[difficulty]
        draw_display()
        screen.update()


def choose_hard():
    global difficulty, base_delay

    if state == "menu":
        difficulty = "Hard"
        base_delay = DIFFICULTIES[difficulty]
        draw_display()
        screen.update()


# -------------------- MOVEMENT --------------------

def go_up():
    if state == "playing" and head.direction != "down":
        head.direction = "up"


def go_down():
    if state == "playing" and head.direction != "up":
        head.direction = "down"


def go_left():
    if state == "playing" and head.direction != "right":
        head.direction = "left"


def go_right():
    if state == "playing" and head.direction != "left":
        head.direction = "right"


def move_head():
    x = head.xcor()
    y = head.ycor()

    if head.direction == "up":
        y += GRID
    elif head.direction == "down":
        y -= GRID
    elif head.direction == "left":
        x -= GRID
    elif head.direction == "right":
        x += GRID

    return (int(x), int(y))


# -------------------- PAUSE AND RESTART --------------------

def toggle_pause():
    global state

    if state == "playing":
        state = "paused"
    elif state == "paused":
        state = "playing"

    draw_display()
    screen.update()


def restart_game():
    if state != "menu":
        start_game()


def return_to_menu():
    show_menu()


# -------------------- GAME SPEED --------------------

def get_delay():
    # Increase speed every 20 points.
    speed = max(55, base_delay - (score // 20) * 5)

    # Blue power-up temporarily slows the snake.
    if ticks < slow_until_tick:
        speed = min(300, int(speed * 1.6))

    return speed


# -------------------- MAIN GAME LOGIC --------------------

def update_game():
    global score, high_score, level, ticks
    global slow_until_tick

    if head.direction == "stop":
        return

    ticks += 1

    next_position = move_head()
    x, y = next_position

    # Wall collision.
    if abs(x) > WALL_LIMIT or abs(y) > WALL_LIMIT:
        end_game()
        return

    # Obstacle collision.
    if next_position in obstacles:
        end_game()
        return

    # Food collision.
    eating = next_position == tuple(food.position())

    # The tail moves away unless the snake is eating.
    body_to_check = segments if eating else segments[:-1]

    for segment in body_to_check:
        if next_position == tuple(segment.position()):
            end_game()
            return

    old_head_position = tuple(head.position())

    if segments:
        old_tail_position = tuple(segments[-1].position())
    else:
        old_tail_position = old_head_position

    # Move the body from back to front.
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].position())

    if segments:
        segments[0].goto(old_head_position)

    head.goto(next_position)

    # Process food after moving the head.
    if eating:
        if food_kind == "normal":
            score += 10

        elif food_kind == "bonus":
            score += 50

        elif food_kind == "slow":
            score += 10
            slow_until_tick = ticks + 35

        # Grow the snake at its previous tail position.
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("darkgreen")
        new_segment.penup()
        new_segment.goto(old_tail_position)

        segments.append(new_segment)

        # Update and save the high score.
        if score > high_score:
            high_score = score
            save_high_score()

        # Add two obstacles for each new level.
        new_level = score // 50 + 1

        while level < new_level:
            level += 1
            add_obstacles(2)

        spawn_food()


# -------------------- GAME LOOP --------------------

def game_loop():
    if state == "playing":
        update_game()

    draw_display()
    screen.update()

    if state == "playing":
        screen.ontimer(game_loop, get_delay())
    else:
        screen.ontimer(game_loop, 100)


# -------------------- KEYBOARD CONTROLS --------------------

screen.listen()

screen.onkey(start_game, "Return")

screen.onkey(choose_easy, "1")
screen.onkey(choose_medium, "2")
screen.onkey(choose_hard, "3")

screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

screen.onkey(go_up, "w")
screen.onkey(go_down, "s")
screen.onkey(go_left, "a")
screen.onkey(go_right, "d")

screen.onkey(toggle_pause, "space")
screen.onkey(restart_game, "r")
screen.onkey(return_to_menu, "m")



spawn_food()
draw_display()
screen.update()

screen.ontimer(game_loop, 100)
screen.mainloop()
