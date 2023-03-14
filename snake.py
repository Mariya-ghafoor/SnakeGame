# Import the Turtle Graphics module
import turtle
import random
from playsound import playsound
from threading import Thread
from tkinter import PhotoImage
from turtle import Shape, Turtle

# Define program constants
WIDTH = 500
HEIGHT = 500
DELAY = 400
FOOD_SIZE = 10

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)

}


def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("right"), "Right")
    screen.onkey(lambda: set_snake_direction("left"), "Left")


def set_snake_direction(direction):
    global snake_direction
    if direction == 'up':
        if snake_direction != "down":  # no self collision simply by pressing wrong key
            snake_direction = "up"

    elif direction == 'down':
        if snake_direction != "up":
            snake_direction = "down"

    elif direction == 'left':
        if snake_direction != "right":
            snake_direction = "left"

    elif direction == 'right':
        if snake_direction != "left":
            snake_direction = "right"


def playy():
    # Play sound when snake catches food
    path_sound = '/Users/mariyakashif/PycharmProjects/SnakeGame/food.mp3'
    playsound(path_sound, block=False)


def game_loop():
    stamper.clearstamps()

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check collisions
    if new_head in snake or new_head[0] < - WIDTH / 2 or new_head[0] > WIDTH / 2 \
            or new_head[1] < -HEIGHT / 2 or new_head[1] > HEIGHT / 2:
        reset()

    else:
        snake.append(new_head)
        print("--------", snake)
        # Check food collision

        if not food_collision():
            snake.pop(0)  # Keep the snake same length unless fed
        print(snake)

        # direction for snake head
        snake_head_x, snake_head_y = snake[-1]
        print('snake head x ',snake_head_x, 'snake head y ',snake_head_y)
        snake_head.goto(snake_head_x, snake_head_y)
        snake_head.stamp()
        snake_head.clearstamps()

        for segment in snake[:-1]:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        # Refresh screen
        screen.title(f"Snake Game. Score:  {score}")
        screen.update()

        turtle.ontimer(game_loop, DELAY)


def food_collision():
    global food_pos, score
    if get_distance(snake[-1], food_pos) < 20:

        # New thread to play sound in parallel when snake catches food
        T = Thread(target=playy)  # create thread
        T.start()  # Launch created thread

        score += 1
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False


def get_random_food_pos():
    x = random.randint(-WIDTH / 2 + FOOD_SIZE, WIDTH / 2 - FOOD_SIZE)
    y = random.randint(-HEIGHT / 2 + FOOD_SIZE, HEIGHT / 2 - FOOD_SIZE)
    return (x, y)


# Find the distance between the head of the snake and the target using Pythagoras theoram
def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance


def reset():
    global score, snake, snake_direction, food_pos
    score = 0
    # Create snake as a list of coordinate pairs
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    game_loop()


# Create a window where we will do our drawing.
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)  # Set the dimensions of the Turtle Graphics window.
screen.title("Stamping")
screen.bgcolor("pink")
screen.tracer(0)

# Event handlers
screen.listen()
bind_direction_keys()

# Create snake head
snake_head = turtle.Turtle(visible=False)
larger = PhotoImage(file="snake_head.gif").subsample(7, 7)
screen.addshape("larger", Shape("image", larger))
snake_head = Turtle("larger")
snake_head.penup()


# Create snake body
stamper = turtle.Turtle()
stamper.shape("circle")
stamper.color('green')
stamper.penup()

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(FOOD_SIZE / 20)
food.penup()

reset()
# This statement (or an equivalent) is needed at the end of all your turtle programs.
turtle.done()
