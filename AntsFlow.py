from Ant import Ant
from const import *
from tkinter import *
from Board import Board
import time
import numpy as np
from utils import coords_within_circle

class AntsFlow:

    def __init__(self, mode=VISUAL):
        self.window = None # la simulacion comienza vacia
        self.board = None
        self.completed = False
        self.max_width = 75 # cms
        self.max_height = 30 # cms (par para que encajen mejor los pixeles)
        self.scale = 9 # escala de pixeles a cms -> 9 pixels = 1 cm
        self.border = BORDER
        self.mode = mode

        self.num_ants = N_HORMIGAS
        self.time = 0
        self.delay = T_STEP * 0 # numero entre 0 y 1, 0 -> max vel. 1 -> velocidad real
        
        self.nest = [1.5, 0]
        self.prey = [self.max_width-1.5, 0]
        self.radious = 2

        self.ant_list = []
            
    def simulate(self):
        start_time = time.perf_counter()
        # gestionar elementos a dibujar en pantalla e iniciar el dibujo
        self.start()

        # actualizamos el modelo paso a paso
        id_ant = 0
        step = 0
        while self.time < T_MAX and not self.completed:
            # print(self.time)
            # añadimos una hormiga cada 8 pasos hasta MAX
            if id_ant < self.num_ants and step % 20  == 0:
                id_ant += 1
                self.add_new_ant(id_ant)

            self.step()
            time.sleep(self.delay) # se utiliza para poder controla la velocidad a la que se actualiza el sistema
            self.time += T_STEP
            step += 1
        
        # finalizamos la simulación
        if self.mode == VISUAL:
            # al terminar cerramos la ventana
            self.window.destroy()

        # self.window.mainloop() # este comando mantiene activa la ventana hasta que se destruya self.window.destroy()
                               # los avances se van dando en cada step 
        print("Simulation finished. Time:", round((time.perf_counter() - start_time)), "seconds")

    def add_new_ant(self, id):
        ant = Ant(id)
        self.ant_list.append(ant)
        pref = PREF_LEAVE
        if id % 2 == 0:
            pref = PREF_LEAVE
            x = self.nest[0] + self.radious*0.8
            y = self.nest[1]
        else:
            pref = PREF_RETURN
            x = self.prey[0] - self.radious*0.8
            y = self.prey[1]

        ant.update_preference(pref)
        ant.pos_v = [x, y]
        if self.mode == VISUAL:
            self.board.add_ant(ant)


    def start(self):
        if self.mode == VISUAL:
            # iniciamos la ventana
            self.window = Tk()
            self.window.bind("<q>", lambda e: self.finish())
            width = self.max_width*self.scale
            height = self.max_height*self.scale
            self.board = Board(self.window, width=width, height=height, scale=self.scale)
            self.board.draw_nest(self.nest, self.radious)
            self.board.draw_prey(self.prey, self.radious)

            # dibujamos el board en el Tk
            self.board.draw()

    def finish(self):
        self.completed = True

    def step(self):
        # actualizamos el movimeinto de cada hormiga
        for ant_i in self.ant_list:
            # NOTE: para los debug, luego se quita
            # if self.mode == VISUAL:
            #    self.board.change_ant_color(ant_i.id, "blue")
            #    self.board.step()

            # is there any ant_j in ant_i's local area?
            near_ants = self.search_near_ants(ant_i)
            if len(near_ants) > 0:
                ant_i.avoid_ants(near_ants)
                acceleration = -ACELERACION*T_STEP
            else:
                ant_i.search_pheromone()
                acceleration = ACELERACION*T_STEP

            ant_i.accelerate(acceleration)
            old_pos = ant_i.pos_v
            new_pos = ant_i.update_pos(T_STEP, self.border, 
                self.max_width - self.border, self.max_height/2 - self.border)
            move_v = np.array(new_pos) - np.array(old_pos)

            # si ha llegado a un punto de inicio, actualizar la preferencia
            if coords_within_circle(self.nest, new_pos, self.radious):
                ant_i.update_preference(PREF_LEAVE)
            elif coords_within_circle(self.prey, new_pos, self.radious):
                ant_i.update_preference(PREF_RETURN)

            if self.mode == VISUAL:
                self.board.update_ant(ant_i, move_v)
                # self.board.change_ant_color(ant_i.id, "black")

        if self.mode == VISUAL:
            self.board.step()

    def search_near_ants(self, ant_i: Ant):
        near_ants = []
        for ant_j in self.ant_list:
            if ant_i.id != ant_j.id:
                near = ant_i.is_near(ant_j)
                if near:
                    near_ants.append(ant_j)

        return near_ants

    def eval(self):
        # TODO
        pass
        
       
if __name__ == "__main__":
    ants_flow = AntsFlow()

    # adding ants to simulation
    ants_flow.simulate()
    ants_flow.eval()