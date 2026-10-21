# helloworld
my first gihub post 
------------------------------
halo 
import random
import time
import turtle

# Delay between screen updates (controls game speed)
delay = 0.1

# Score counter
score = 0
high_score = 0

# Set up the screen
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)  # Turns off automatic screen updates

# Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Body Segments
segments = []

# Score Display
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))


# Movement Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)


# Keyboard Controls
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# Main Game Loop
while True:
    screen.update()

    # Check for collision with wall
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # Hide body segments on reset
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        # Reset score
        score = 0
        pen.clear()
        pen.write(
            f"Score: {score}  High Score: {high_score}",
            align="center",
            font=("Courier", 24, "normal"),
        )

    # Check for collision with food
    if head.distance(food) < 20:
        # Move food to random position
        food.goto(
            random.randint(-14, 14) * 20,
            random.randint(-14, 14) * 20,
        )

        # Add new body segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("dark green")
        new_segment.penup()
        segments.append(new_segment)

        # Update score
        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write(
            f"Score: {score}  High Score: {high_score}",
            align="center",
            font=("Courier", 24, "normal"),
        )

    # Move body segments in reverse order
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    # Move segment 0 to head position
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Check for self-collision
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            score = 0
            pen.clear()
            pen.write(
                f"Score: {score}  High Score: {high_score}",
                align="center",
                font=("Courier", 24, "normal"),
            )

    time.sleep(delay)
