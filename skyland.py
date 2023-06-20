# cse30
# pa5
# skyland.py - a one-level platform video game
# author: Vincent Fu
# date: June 8, 2023

from tkinter import *
import tkinter.font as font
from random import random, randint  # optional
from math import sin, cos, pi  # optional
import math


WIDTH, HEIGHT = 600, 400  # global variables (constants) go here
CLOCK_RATE = 15
START_X, START_Y = 20, 350
END_X, END_Y = 400, 350

class Skyland:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.bind_all('<KeyPress-space>', self.pause)
        self.canvas.bind_all('<KeyPress-Alt_L>', self.restart)

        self.score = 0
        self.land = Land(canvas)
        self.trophy = Trophy(canvas)
        self.add_random_trophies()
        self.avatar = Avatar(canvas)
        self.text = canvas.create_text(
            150,
            370,
            text='Score ?  Time ? ',
            font=font.Font(family='Helveca', size='15', weight='bold')
        )

        self.spiders = [
            AI(canvas, 200, 250),
            AI(canvas, 400, 200),
            AI(canvas, 500, 300)
        ]
        # Start the game update loop
        self.update()

    def restart(self, event=None):
        self.avatar.replace()
        self.trophy.replace()

        self.update()

    def pause(self, event=None):
        pass

    def add_random_trophies(self):
        for _ in range(5):
            self.trophy.get_trophy()


    def update(self):
        self.avatar.update(self.land, self.trophy)
        for spider in self.spiders:
            spider.update(self.avatar)
        self.canvas.after(CLOCK_RATE, self.update)


class Land:
    def __init__(self, canvas):
        self.canvas = canvas

        # Draw the sky and valley background
        self.canvas.create_rectangle(0, 0, WIDTH, START_Y - 100, fill='lightblue')
        
        self.canvas.create_rectangle(0, START_Y - 120, WIDTH, START_Y, fill='limegreen')
        # Generate hills and clouds
        self.make_hill(50, 230, 250, 230, height=100, delta=3)
        self.make_hill(150, 300, 350, 300, height=100, delta=3)
        self.make_hill(250, 250, 450, 250, height=100, delta=3)
        self.make_hill(350, 300, 550, 300, height=100, delta=3)

        cloud1 = self.make_cloud(100, 120)
        cloud2 = self.make_cloud(200, 140)
        cloud3 = self.make_cloud(300, 80)
        self.clouds = [cloud1, cloud2, cloud3]
        # Create and store the obstacle objects
        self.obstacles = self.get_obstacles()  # Store the obstacle objects in the 'obstacles' attribute

    def make_hill(self, x1, y1, x2, y2, height=100, delta=3):
        # Generate a hill shape using polygon
        points = []
        points.append((x1, y1))

        num_steps = int((x2 - x1) / delta)
        height_step = height / num_steps

        for i in range(num_steps + 1):
            x = x1 + i * delta
            y = y1 - height_step * i
            points.append((x, y))

        points.append((x2, y2))

        self.canvas.create_polygon(points, fill='brown', outline='brown')

    def make_cloud(self, x, y):
        # Generate a cloud shape using oval
        cloud_width = 80
        cloud_height = 40
        return self.canvas.create_oval(
            x, y, x + cloud_width, y + cloud_height, fill='white', outline='black'
        )

    def get_obstacles(self):
        # Create and return the obstacle objects
        obstacle1 = self.canvas.create_rectangle(0, 0, 10, 600, outline="black", fill="orange", width=2)
        #obstacle2 = self.canvas.create_rectangle(0, 340, 600, 350, outline="black", fill="orange", width=2)
        obstacle3 = self.canvas.create_rectangle(590, 0, 600, 600, outline="black", fill="orange", width=2)
        obstacle4 = self.canvas.create_rectangle(0, 0, 600, 10, outline="black", fill="orange", width=2)
        return [obstacle1, obstacle3, obstacle4]

    def update(self):
        pass


class Trophy:
    def __init__(self, canvas):
        self.canvas = canvas
        purple_egg = self.canvas.create_oval(0, 0, 20, 10, fill='orchid')
        pink_egg = self.canvas.create_oval(0, 0, 20, 10, fill='pink')

        self.trophies = [purple_egg, pink_egg]

    # Create a trophy object with a random position
    def get_trophy(self):
        # Create a new trophy object with a random position
        x = randint(50, WIDTH - 50)
        y = randint(50, HEIGHT - 50)
        trophy = self.canvas.create_oval(x, y, x + 20, y + 10, fill='orchid')
        self.trophies.append(trophy)
    


    def replace(self):
        for trophy in self.trophies:
            self.canvas.delete(trophy)
        self.trophies = []


class AI:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.spider = self.make_spider(x, y)
        self.legs = self.make_legs(x, y)
        self.x, self.y = 0, 0.5

    def make_spider(self, x, y):
        color1 = 'black'
        head = self.canvas.create_oval(5, 5, 15, 13, fill=color1)
        torso = self.canvas.create_oval(0, 10, 20, 40, fill=color1)
        spider = [head, torso]
        for part in spider:
            self.canvas.move(part, x, y)
        return spider

    def make_legs(self, x, y):
        color1 = 'black'
        legs = [
            self.canvas.create_line(-5 - i * 5, 10 * i + 5, 5, 10 * i + 15,
                                    fill=color1, width=4) for i in range(2)] + \
               [
                   self.canvas.create_line(15, 10 * i + 15, 25 + i * 5, 10 * i + 5,
                                           fill=color1, width=4) for i in range(2)] + \
               [
                   self.canvas.create_line(-10 + i * 5, 10 * i + 35, 5, 10 * i + 25,
                                           fill=color1, width=4) for i in range(2)] + \
               [
                   self.canvas.create_line(15, 10 * i + 25, 30 - i * 5, 10 * i + 35,
                                           fill=color1, width=4) for i in range(2)]
        for leg in legs:
            self.canvas.move(leg, x, y)
        return legs

    def update(self, eatable):
        spider_coords = self.canvas.coords(self.spider[0])
        if spider_coords[0] < 10 or spider_coords[2] > 590:
            self.x *= -1  # Reverse horizontal movement at the boundaries
        if spider_coords[1] < 10 or spider_coords[3] > 390:
            self.y *= -1  # Reverse vertical movement at the boundaries
        self.canvas.move(self.spider[0], self.x, self.y)
        self.canvas.move(self.spider[1], self.x, self.y)
        for leg in self.legs:
            self.canvas.move(leg, self.x, self.y)
        self.check_collision(eatable)


    def check_collision(self, avatar):
        spider_coords = self.canvas.coords(self.spider[0])
        avatar_coords = self.canvas.coords(avatar.torso)
        if self.detect_collision(spider_coords, avatar_coords):
            avatar.x = 0
            avatar.y = 0

    def detect_collision(self, coords1, coords2):
        x1, y1, x2, y2 = coords1
        x3, y3, x4, y4 = coords2
        if (x1 < x4 and x2 > x3) and (y1 < y4 and y2 > y3):
            return True
        return False



class Avatar:
    def __init__(self, canvas):
        color1 = 'lime'
        color2 = 'sandybrown'
        self.canvas = canvas
        self.head = self.canvas.create_oval(0, 0, 10, 10, fill=color2)
        self.torso = self.canvas.create_rectangle(0, 10, 10, 20, fill=color1)
        self.canvas.move(self.head, START_X, START_Y - 100)
        self.canvas.move(self.torso, START_X, START_Y - 100)
        self.canvas.bind_all('<KeyPress-Left>', self.move)
        self.canvas.bind_all('<KeyPress-Right>', self.move)
        self.canvas.bind_all('<KeyPress-Up>', self.jump)
        self.canvas.bind_all('<KeyPress-Down>', self.move)
        self.x = 1
        self.y = 0
        self.is_jumping = False
        self.jump_count = 0
        self.gravity = 1  # Gravity value

    def update(self, land, trophy):
        if self.is_jumping:
            self.jump_count -= 1
            self.y = -2
            if self.jump_count <= 0:
                self.is_jumping = False
                self.jump_count = 10
        else:
            self.y += self.gravity  # Apply gravity to y-axis movement
        self.canvas.move(self.head, self.x, self.y)
        self.canvas.move(self.torso, self.x, self.y)
        self.check_collision(land)
        self.find_trophy(trophy)

    def move(self, event=None):
        if event.keysym == 'Left':
            self.x = -1
        elif event.keysym == 'Right':
            self.x = 1
        elif event.keysym == 'Down':
            self.y = 1

    def jump(self, event=None):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = 20  # Adjust the jump duration as needed

    def check_collision(self, land):
        avatar_coords = self.canvas.coords(self.torso)
        if avatar_coords[3] >= HEIGHT:  # Check collision with the ground
            self.y = 0
            self.canvas.move(self.head, 0, HEIGHT - avatar_coords[3])
            self.canvas.move(self.torso, 0, HEIGHT - avatar_coords[3])
        for obstacle in land.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if self.detect_collision(avatar_coords, obstacle_coords):
                self.x = 0
                self.y = 0
                break

    def detect_collision(self, coords1, coords2):
        x1, y1, x2, y2 = coords1
        x3, y3, x4, y4 = coords2
        if (x1 < x4 and x2 > x3) and (y1 < y4 and y2 > y3):
            return True
        return False

    def find_trophy(self, trophy):
        avatar_coords = self.canvas.coords(self.torso)
        trophies_to_remove = []

        for t in trophy.trophies:
            trophy_coords = self.canvas.coords(t)
            if self.detect_collision(avatar_coords, trophy_coords):
                trophies_to_remove.append(t)

        for t in trophies_to_remove:
            trophy.trophies.remove(t)
            self.canvas.delete(t)

    def replace(self):
        self.canvas.move(self.head, START_X, START_Y - 100 - self.canvas.coords(self.head)[3])
        self.canvas.move(self.torso, START_X, START_Y - 100 - self.canvas.coords(self.torso)[3])


root = Tk()
root.title('Skyland')

canvas = Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

skyland = Skyland(canvas)

root.mainloop()