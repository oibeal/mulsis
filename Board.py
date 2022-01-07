from tkinter import *
from Ant import Ant
import math
from const import *
from utils import create_circle

class Board:
    
    def __init__(self, master, width = 1200, height = 700, scale = 9):
        self.width = width
        self.height = height
        self.scale = scale # escala de pixeles a cms -> 9 pixels = 1 cm
        self.background_color = "lightgrey"

        self.canvas = Canvas(master, width=self.width, height=self.height, bg=self.background_color)
        
        x0 = self.width*0.03
        y0 = self.height/2
        x1 = self.width - x0
        y1 = y0
        self.feromone_line = self.canvas.create_line(x0, y0, x1, y1, fill="darkgrey") # feromone line

        self.nest = None
        self.prey = None

        self.ant_list = {}

    def draw(self):
        self.canvas.pack()

    def step(self):
        self.canvas.update()

    def add_ant(self, ant: Ant):
        id_ant = ant.id
        
        x0, y0, x1, y1 = self.get_ant_pixels(ant)

        ant_draw = self.canvas.create_oval(x0, y0, x1, y1, fill="black")
        self.ant_list[id_ant] = ant_draw

    def update_ant(self, ant: Ant, new_v):
        id_ant = ant.id
        x0 = new_v[0] * self.scale
        y0 = new_v[1] * self.scale
        ant_draw = self.ant_list[id_ant]
        if ant.preference == PREF_LEAVE:
            color = "black"
        else:
            color = "red"

        self.change_ant_color(id_ant, color) # change color
        self.canvas.move(ant_draw, x0, -y0)

    def change_ant_color(self, ant_id, color):
        ant_draw = self.ant_list[ant_id]
        self.canvas.itemconfig(ant_draw, fill=color)

    def get_ant_pixels(self, ant: Ant):
        centre = ant.pos_v
        antennae_len = ant.antennae_len
        antennae_grad = math.radians(ant.antennae_grad)

        # TODO: cambiar la forma por un rectangulo que se pueda rotar
        x0 = (centre[0] - ant.r_body) * self.scale
        y0 = self.height/2 - (centre[1] + ant.r_body) * self.scale
        x1 = (centre[0] + ant.r_body + antennae_len*math.cos(antennae_grad)) * self.scale
        y1 = self.height/2 - (centre[1] - ant.r_body) * self.scale
        
        return x0, y0, x1, y1

    def draw_nest(self, coords, rad):
        y_nest = self.height/2 - coords[1]*self.scale
        x_nest = coords[0]*self.scale
        self.nest = create_circle(x_nest, y_nest, rad*self.scale, self.canvas, "black")

    def draw_prey(self, coords, rad):
        y_prey = self.height/2 - coords[1]*self.scale
        x_prey = coords[0]*self.scale
        self.prey = create_circle(x_prey, y_prey, rad*self.scale, self.canvas, "red")