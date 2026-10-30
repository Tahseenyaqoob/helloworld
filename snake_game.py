import turtle
import random
import math
from pathlib import Path

# =====================================================
# SNAKEX - EMERALD QUEST
# =====================================================

WIDTH = 900
HEIGHT = 760
GRID = 20

BOUND_X = 420
BOUND_Y = 310

SAVE_FILE = Path(__file__).with_name("snakex_highscore.txt")

# ---------------- SCREEN ----------------

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("SNAKEX | Emerald Quest")
screen.bgcolor("#07130f")
screen.tracer(0)

# ---------------- COLORS ----------------

GREEN = "#087a42"
DARK_GREEN = "#034d2b"
LIGHT_GREEN = "#39d98a"
MINT = "#9bffcf"
GOLD = "#ffd166"
WHITE = "#f4fff8"
RED = "#ff5252"
CYAN = "#45e6ff"

# ---------------- HIGH SCORE ----------------

try:
    high_score = int(SAVE_FILE.read_text())
except (ValueError, FileNotFoundError):
    high_score = 0

def save_score():
    global high_score
    if score > high_score:
        high_score = score
        SAVE_FILE.write_text(str(high_score))

# ---------------- GAME VARIABLES ----------------

score = 0
level = 1
difficulty = "MEDIUM"

speed_settings = {
    "EASY": 145,
    "MEDIUM": 105,
    "HARD": 75
}

base_delay = speed_settings[difficulty]
delay = base_delay

state = "menu"
direction = "right"

snake = []
food_position = (0, 0)
food_type = "apple"

bomb_position = (0, 0)
bomb_active = False
bomb_timer = 0
bomb_blink = 0
next_bomb_tick = 100

shield_position = (0, 0)
shield_active = False
shield_timer = 0
shield_available = False
next_shield_tick = 180

ticks = 0
combo = 0
last_food_tick = -100
message_timer = 0
game_message = ""

# ---------------- TURTLE HELPERS ----------------

def make_turtle(shape="turtle", color=WHITE):
    t = turtle.Turtle()
    t.shape(shape)
    t.color(color)
    t.penup()
    t.speed(0)
    return t

def make_writer():
    t = make_turtle()
    t.hideturtle()
    return t

ui = make_writer()
menu_text = make_writer()
popup = make_writer()

# ---------------- BACKGROUND DECORATION ----------------

stars = []

for _ in range(45):
    star = make_turtle("circle", "#163a2b")
    star.shapesize(0.12)
    star.goto(
        random.randint(-430, 430),
        random.randint(-350, 350)
    )
    stars.append(star)

# ---------------- HUD ----------------

def draw_hud():
    ui.clear()
    ui.color(WHITE)

    ui.goto(-420, 335)
    ui.write("SNAKEX", font=("Arial", 20, "bold"))

    ui.goto(-420, 305)
    ui.color(MINT)
    ui.write(
        f"SCORE  {score}     BEST  {high_score}",
        font=("Arial", 12, "bold")
    )

    ui.goto(130, 335)
    ui.color(GOLD)
    ui.write(
        f"LEVEL {level}   |   {difficulty}",
        font=("Arial", 15, "bold")
    )

    ui.goto(130, 305)
    ui.color(WHITE)
    ui.write(
        f"COMBO x{combo}     SHIELD {'READY' if shield_available else 'OFF'}",
        font=("Arial", 11, "normal")
    )

    ui.goto(-420, -350)
    ui.color("#8ba99a")
    ui.write(
        "WASD / ARROWS: MOVE     SPACE: PAUSE     R: RESTART     M: MENU",
        font=("Arial", 10, "normal")
    )

# ---------------- SNAKE MODEL ----------------

head = make_turtle("circle", GREEN)
head.shapesize(1.25)

head_shadow = make_turtle("circle", DARK_GREEN)
head_shadow.shapesize(1.4)

# Face details
left_eye = make_turtle("circle", WHITE)
right_eye = make_turtle("circle", WHITE)

left_pupil = make_turtle("circle", "#061c12")
right_pupil = make_turtle("circle", "#061c12")

left_eye.shapesize(0.23)
right_eye.shapesize(0.23)
left_pupil.shapesize(0.11)
right_pupil.shapesize(0.11)

cheek_left = make_turtle("circle", "#ff91a4")
cheek_right = make_turtle("circle", "#ff91a4")
cheek_left.shapesize(0.15)
cheek_right.shapesize(0.15)

smile = make_writer()

def create_segment(position):
    shadow = make_turtle("circle", "#022d1a")
    shadow.shapesize(0.95)

    body = make_turtle("circle", GREEN)
    body.shapesize(0.82)

    highlight = make_turtle("circle", LIGHT_GREEN)
    highlight.shapesize(0.18)

    scale = make_turtle("circle", DARK_GREEN)
    scale.shapesize(0.16)

    segment = {
        "shadow": shadow,
        "body": body,
        "highlight": highlight,
        "scale": scale
    }

    move_segment(segment, position)
    return segment

def move_segment(segment, position):
    x, y = position

    segment["shadow"].goto(x + 3, y - 4)
    segment["body"].goto(x, y)
    segment["highlight"].goto(x - 4, y + 4)
    segment["scale"].goto(x + 4, y - 3)

def hide_segment(segment):
    for part in segment.values():
        part.hideturtle()

def update_face():
    x, y = head.position()

    if direction == "right":
        eye_positions = [(x + 7, y + 6), (x + 7, y - 6)]
        cheek_positions = [(x + 9, y + 1), (x + 9, y - 5)]
        pupil_positions = [(x + 9, y + 6), (x + 9, y - 6)]
        smile_pos = (x + 11, y - 6)

    elif direction == "left":
        eye_positions = [(x - 7, y + 6), (x - 7, y - 6)]
        cheek_positions = [(x - 9, y + 1), (x - 9, y - 5)]
        pupil_positions = [(x - 9, y + 6), (x - 9, y - 6)]
        smile_pos = (x - 11, y - 6)

    elif direction == "up":
        eye_positions = [(x - 6, y + 7), (x + 6, y + 7)]
        cheek_positions = [(x - 10, y + 1), (x + 10, y + 1)]
        pupil_positions = [(x - 6, y + 9), (x + 6, y + 9)]
        smile_pos = (x - 4, y + 1)

    else:
        eye_positions = [(x - 6, y - 7), (x + 6, y - 7)]
        cheek_positions = [(x - 10, y - 1), (x + 10, y - 1)]
        pupil_positions = [(x - 6, y - 9), (x + 6, y - 9)]
        smile_pos = (x - 4, y - 5)

    left_eye.goto(eye_positions[0])
    right_eye.goto(eye_positions[1])

    left_pupil.goto(pupil_positions[0])
    right_pupil.goto(pupil_positions[1])

    cheek_left.goto(cheek_positions[0])
    cheek_right.goto(cheek_positions[1])

    smile.clear()
    smile.goto(smile_pos)
    smile.color("#062c1a")
    smile.dot(3)

# ---------------- FRUIT SYSTEM ----------------

fruit = make_turtle("circle", RED)
fruit.shapesize(0.75)

fruit_leaf = make_turtle("circle", GREEN)
fruit_leaf.shapesize(0.22)

fruit_stem = make_turtle("circle", "#8b572a")
fruit_stem.shapesize(0.12)

fruit_glow = make_turtle("circle", "#ff9999")
fruit_glow.shapesize(1.0)

FRUITS = [
    ("apple", "#ff354f", 10),
    ("pear", "#c4ec37", 20),
    ("orange", "#ff9f1c", 15),
    ("cherries", "#e51b54", 25),
    ("grapes", "#a56eff", 30),
    ("blueberry", "#459bff", 35),
    ("golden fruit", "#ffd700", 50)
]

def draw_fruit():
    x, y = food_position

    color = next(item[1] for item in FRUITS if item[0] == food_type)

    fruit.goto(x, y)
    fruit.color(color)
    fruit.shapesize(0.75)

    fruit_glow.goto(x, y)
    fruit_glow.color(color)

    fruit_leaf.goto(x + 5, y + 9)
    fruit_stem.goto(x, y + 10)

    if food_type == "cherries":
        fruit.shapesize(0.55)
        fruit_leaf.shapesize(0.18)

    elif food_type == "grapes":
        fruit.shapesize(0.45)

    elif food_type == "golden fruit":
        fruit.shapesize(0.95)

def occupied_positions():
    positions = [tuple(map(round, head.position()))]

    for segment in snake:
        positions.append(
            tuple(map(round, segment["body"].position()))
        )

    if bomb_active:
        positions.append(bomb_position)

    if shield_available:
        positions.append(shield_position)

    return positions

def random_position():
    occupied = occupied_positions()

    for _ in range(300):
        x = random.randrange(-20, 21) * GRID
        y = random.randrange(-15, 16) * GRID

        if (x, y) not in occupied:
            return x, y

    return 0, 0

def spawn_fruit():
    global food_position, food_type

    food_position = random_position()

    # The skull is completely removed.
    # Every new fruit is randomly selected.
    food_type, _, _ = random.choices(
        FRUITS,
        weights=[25, 18, 17, 12, 10, 10, 8],
        k=1
    )[0]

    draw_fruit()

# ---------------- BOMB SYSTEM ----------------

bomb = make_turtle("circle", "#303030")
bomb.shapesize(0.85)

bomb_fuse = make_turtle("circle", "#ffb000")
bomb_fuse.shapesize(0.25)

bomb_flash = make_turtle("circle", RED)
bomb_flash.shapesize(1.0)

explosion = make_turtle("circle", "#ffb000")
explosion.hideturtle()

explosion_text = make_writer()

def spawn_bomb():
    global bomb_active, bomb_position, bomb_timer

    bomb_position = random_position()
    bomb_active = True
    bomb_timer = 80

    draw_bomb()

def draw_bomb():
    x, y = bomb_position

    bomb.goto(x, y)
    bomb.color("#333333")
    bomb.shapesize(0.85)

    bomb_fuse.goto(x + 5, y + 11)
    bomb_fuse.color("#ffae00")

    bomb_flash.goto(x, y)
    bomb_flash.color(
        RED if ticks % 8 < 4 else "#ffb000"
    )

def hide_bomb():
    global bomb_active

    bomb_active = False
    bomb.hideturtle()
    bomb_fuse.hideturtle()
    bomb_flash.hideturtle()

def explode_bomb():
    global state

    state = "exploding"
    hide_bomb()

    x, y = bomb_position

    def explosion_frame(frame=0):
        if frame >= 8:
            explosion.clear()
            explosion_text.clear()
            game_over("BOOM! THE GARDEN EXPLODED!")
            return

        explosion.goto(x, y)
        explosion.color(
            ["#fff176", "#ffb000", "#ff7043", "#ff2525"][frame % 4]
        )
        explosion.shapesize(1 + frame * 0.65)

        explosion_text.clear()
        explosion_text.goto(x, y + 35)
        explosion_text.color("#ffcf70")
        explosion_text.write(
            "BOOM!",
            align="center",
            font=("Arial", 16, "bold")
        )

        screen.update()
        screen.ontimer(lambda: explosion_frame(frame + 1), 80)

    explosion.showturtle()
    explosion_frame()

# ---------------- SHIELD POWER-UP ----------------

shield = make_turtle("circle", CYAN)
shield.shapesize(0.65)

def spawn_shield():
    global shield_available, shield_position

    shield_position = random_position()
    shield_available = True

    shield.goto(shield_position)
    shield.color(CYAN)
    shield.shapesize(0.65)
    shield.showturtle()

def hide_shield():
    global shield_available

    shield_available = False
    shield.hideturtle()

# ---------------- GAME MESSAGES ----------------

def show_popup(text, color=GOLD):
    popup.clear()
    popup.goto(0, 250)
    popup.color(color)
    popup.write(
        text,
        align="center",
        font=("Arial", 18, "bold")
    )

def clear_popup():
    popup.clear()

# ---------------- MOVEMENT ----------------

def move_head():
    x, y = head.position()

    if direction == "up":
        y += GRID
    elif direction == "down":
        y -= GRID
    elif direction == "left":
        x -= GRID
    elif direction == "right":
        x += GRID

    # Wall wrapping
    if x > BOUND_X:
        x = -BOUND_X
    elif x < -BOUND_X:
        x = BOUND_X

    if y > BOUND_Y:
        y = -BOUND_Y
    elif y < -BOUND_Y:
        y = BOUND_Y

    head.goto(x, y)
    head_shadow.goto(x + 3, y - 4)

    update_face()

def move_up():
    global direction
    if direction != "down" and state == "playing":
        direction = "up"

def move_down():
    global direction
    if direction != "up" and state == "playing":
        direction = "down"

def move_left():
    global direction
    if direction != "right" and state == "playing":
        direction = "left"

def move_right():
    global direction
    if direction != "left" and state == "playing":
        direction = "right"

# ---------------- SCORING ----------------

def eat_fruit():
    global score, combo, last_food_tick, level, delay

    if head.distance(food_position) >= 18:
        return

    points = next(item[2] for item in FRUITS if item[0] == food_type)

    if ticks - last_food_tick <= 35:
        combo += 1
    else:
        combo = 1

    last_food_tick = ticks

    bonus = min(combo - 1, 5) * 5
    gained = points + bonus
    score += gained

    # Grow the snake
    last_position = snake[-1]["body"].position()
    snake.append(create_segment(last_position))

    new_level = score // 100 + 1

    if new_level > level:
        level = new_level
        show_popup(f"LEVEL {level} UNLOCKED!", GOLD)

    delay = max(45, base_delay - (level - 1) * 5)

    show_popup(f"+{gained} POINTS!  COMBO x{combo}", MINT)

    save_score()
    spawn_fruit()
    draw_hud()

# ---------------- COLLISION ----------------

def check_self_collision():
    for segment in snake:
        if head.distance(segment["body"]) < 13:
            game_over("YOU BUMPED INTO YOURSELF!")
            return True

    return False

def check_bomb_collision():
    if not bomb_active:
        return False

    if head.distance(bomb_position) < 18:

        if shield_available:
            hide_shield()
            hide_bomb()
            show_popup("SHIELD SAVED YOU!", CYAN)
            return True

        explode_bomb()
        return True

    return False

def check_shield_collision():
    if shield_available and head.distance(shield_position) < 18:
        global shield_timer

        hide_shield()
        shield_timer = 250
        show_popup("SHIELD ACTIVATED!", CYAN)

def update_bomb():
    global bomb_timer, next_bomb_tick

    if not bomb_active:
        if ticks >= next_bomb_tick:
            spawn_bomb()
            next_bomb_tick = ticks + random.randint(130, 200)
        return

    bomb_timer -= 1
    draw_bomb()

    if bomb_timer <= 0:
        hide_bomb()
        next_bomb_tick = ticks + random.randint(100, 160)

# ---------------- GAME OVER ----------------

def game_over(reason):
    global state

    if state == "gameover":
        return

    state = "gameover"
    save_score()

    head.hideturtle()
    head_shadow.hideturtle()

    for part in [left_eye, right_eye, left_pupil, right_pupil,
                 cheek_left, cheek_right]:
        part.hideturtle()

    for segment in snake:
        hide_segment(segment)

    fruit.hideturtle()
    fruit_leaf.hideturtle()
    fruit_stem.hideturtle()
    fruit_glow.hideturtle()

    hide_bomb()
    hide_shield()

    menu_text.clear()

    menu_text.goto(0, 90)
    menu_text.color(RED)
    menu_text.write(
        "GAME OVER",
        align="center",
        font=("Arial", 38, "bold")
    )

    menu_text.goto(0, 35)
    menu_text.color(WHITE)
    menu_text.write(
        reason,
        align="center",
        font=("Arial", 14, "bold")
    )

    menu_text.goto(0, -20)
    menu_text.color(GOLD)
    menu_text.write(
        f"YOUR SCORE: {score}",
        align="center",
        font=("Arial", 22, "bold")
    )

    menu_text.goto(0, -75)
    menu_text.color(MINT)
    menu_text.write(
        f"PERSONAL BEST: {high_score}",
        align="center",
        font=("Arial", 15, "bold")
    )

    menu_text.goto(0, -135)
    menu_text.color(WHITE)
    menu_text.write(
        "PRESS R TO PLAY AGAIN",
        align="center",
        font=("Arial", 15, "bold")
    )

    menu_text.goto(0, -170)
    menu_text.write(
        "PRESS M FOR MAIN MENU",
        align="center",
        font=("Arial", 12, "normal")
    )

    draw_hud()
    screen.update()

# ---------------- PAUSE ----------------

def pause_game():
    global state

    if state == "playing":
        state = "paused"
        show_popup("PAUSED - PRESS SPACE TO RESUME", WHITE)

    elif state == "paused":
        state = "playing"
        clear_popup()
        game_loop()

# ---------------- MAIN GAME LOOP ----------------

def game_loop():
    global ticks, shield_timer, next_shield_tick

    if state != "playing":
        return

    ticks += 1

    # Move body
    for i in range(len(snake) - 1, 0, -1):
        old_position = snake[i - 1]["body"].position()
        move_segment(snake[i], old_position)

    if snake:
        move_segment(snake[0], head.position())

    move_head()

    if check_self_collision():
        return

    if check_bomb_collision():
        if state != "playing":
            return

    check_shield_collision()

    eat_fruit()

    update_bomb()

    # Spawn a shield occasionally
    if not shield_available and ticks >= next_shield_tick:
        spawn_shield()
        next_shield_tick = ticks + random.randint(250, 350)

    if shield_timer > 0:
        shield_timer -= 1

        if shield_timer == 0:
            show_popup("SHIELD EXPIRED!", RED)

    draw_hud()
    screen.update()

    screen.ontimer(game_loop, delay)

# ---------------- START / RESET ----------------

def reset_game():
    global score, level, direction, state
    global ticks, combo, last_food_tick
    global bomb_active, shield_available
    global next_bomb_tick, next_shield_tick
    global shield_timer, base_delay, delay

    for segment in snake:
        hide_segment(segment)

    snake.clear()

    score = 0
    level = 1
    combo = 0
    last_food_tick = -100
    ticks = 0

    direction = "right"
    state = "playing"

    bomb_active = False
    shield_available = False
    shield_timer = 0

    next_bomb_tick = 100
    next_shield_tick = 180

    base_delay = speed_settings[difficulty]
    delay = base_delay

    menu_text.clear()
    popup.clear()
    explosion.clear()
    explosion_text.clear()

    head.goto(0, 0)
    head.showturtle()

    head_shadow.goto(3, -4)
    head_shadow.showturtle()

    for part in [left_eye, right_eye, left_pupil, right_pupil,
                 cheek_left, cheek_right]:
        part.showturtle()

    for i in range(3):
        snake.append(create_segment((-20 * (i + 1), 0)))

    fruit.showturtle()
    fruit_leaf.showturtle()
    fruit_stem.showturtle()
    fruit_glow.showturtle()

    update_face()
    spawn_fruit()
    draw_hud()

    screen.update()
    game_loop()

# ---------------- MAIN MENU ----------------

def show_menu():
    global state

    state = "menu"

    for segment in snake:
        hide_segment(segment)

    snake.clear()

    head.hideturtle()
    head_shadow.hideturtle()

    for part in [left_eye, right_eye, left_pupil, right_pupil,
                 cheek_left, cheek_right]:
        part.hideturtle()

    fruit.hideturtle()
    fruit_leaf.hideturtle()
    fruit_stem.hideturtle()
    fruit_glow.hideturtle()

    hide_bomb()
    hide_shield()

    ui.clear()
    popup.clear()
    menu_text.clear()

    menu_text.goto(0, 180)
    menu_text.color(LIGHT_GREEN)
    menu_text.write(
        "SNAKEX",
        align="center",
        font=("Arial", 48, "bold")
    )

    menu_text.goto(0, 130)
    menu_text.color(GOLD)
    menu_text.write(
        "EMERALD QUEST",
        align="center",
        font=("Arial", 20, "bold")
    )

    menu_text.goto(0, 65)
    menu_text.color(WHITE)
    menu_text.write(
        "A LITTLE SNAKE. A BIG ADVENTURE.",
        align="center",
        font=("Arial", 14, "italic")
    )

    menu_text.goto(0, 0)
    menu_text.color(MINT)
    menu_text.write(
        "SELECT DIFFICULTY",
        align="center",
        font=("Arial", 17, "bold")
    )

    menu_text.goto(0, -40)
    menu_text.color(WHITE)
    menu_text.write(
        "1 - EASY       2 - MEDIUM       3 - HARD",
        align="center",
        font=("Arial", 14, "normal")
    )

    menu_text.goto(0, -105)
    menu_text.color(GOLD)
    menu_text.write(
        "PRESS ENTER TO START",
        align="center",
        font=("Arial", 18, "bold")
    )

    menu_text.goto(0, -165)
    menu_text.color("#a4c6b4")
    menu_text.write(
        "Collect fruit | Build combos | Find shields | Escape bombs",
        align="center",
        font=("Arial", 12, "normal")
    )

    menu_text.goto(0, -205)
    menu_text.color("#a4c6b4")
    menu_text.write(
        "Arrow keys / WASD to move",
        align="center",
        font=("Arial", 11, "normal")
    )

    screen.update()

# ---------------- DIFFICULTY ----------------

def easy():
    global difficulty
    difficulty = "EASY"
    if state == "menu":
        show_menu()

def medium():
    global difficulty
    difficulty = "MEDIUM"
    if state == "menu":
        show_menu()

def hard():
    global difficulty
    difficulty = "HARD"
    if state == "menu":
        show_menu()

# ---------------- KEYBOARD ----------------

screen.listen()

screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

screen.onkey(move_up, "w")
screen.onkey(move_down, "s")
screen.onkey(move_left, "a")
screen.onkey(move_right, "d")

screen.onkey(reset_game, "Return")
screen.onkey(reset_game, "r")
screen.onkey(show_menu, "m")
screen.onkey(pause_game, "space")

screen.onkey(easy, "1")
screen.onkey(medium, "2")
screen.onkey(hard, "3")

# ---------------- RUN ----------------

show_menu()
screen.mainloop()
