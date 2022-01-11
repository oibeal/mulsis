from Ant import Ant
from Grapher import Grapher
from const import *
from tkinter import *
from Board import Board
import time
import numpy as np
from utils import *
import random

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

        self.grapher = Grapher()

            
    def simulate(self):
        start_time = time.perf_counter()
        # gestionar elementos a dibujar en pantalla e iniciar el dibujo
        self.start()

        # actualizamos el modelo paso a paso
        # id_ant = 0
        # step = 0
        while self.time < T_MAX and not self.completed:
            # print(self.time)
            # añadimos una hormiga cada 8 pasos hasta MAX
            # if id_ant < self.num_ants and step % 20  == 0:
            #     id_ant += 1
            #     self.add_new_ant(id_ant)

            self.step()
            self.save_metrics()
            time.sleep(self.delay) # se utiliza para poder controla la velocidad a la que se actualiza el sistema
            self.time += T_STEP
            # step += 1
        
        # finalizamos la simulación
        if self.mode == VISUAL:
            # al terminar cerramos la ventana
            self.window.destroy()

        print("Simulation finished. Time:", round((time.perf_counter() - start_time)), "seconds")

    def add_new_ant(self, id):
        ant = Ant(id)
        self.ant_list.append(ant)
        pref = PREF_LEAVE
        if id % 2 == 0:
            pref = PREF_LEAVE
            # x = self.nest[0] + self.radious*0.8
            # y = self.nest[1]
        else:
            pref = PREF_RETURN
            # x = self.prey[0] - self.radious*0.8
            # y = self.prey[1]

        ant.update_preference(pref)
        # ant.pos_v = [x, y]
        border = self.border
        width = self.max_width-border
        height = self.max_height/2 - border
        px = random.randint(border, width)
        py = random.randint(-height, height)
        ant.pos_v = [px, py]
        max_angle = 360
        ant.dir_v = rotate_vector(ant.dir_v, random.randint(0, max_angle))
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

            # añadimos las hormigas
            for ant_id in range(self.num_ants):
                self.add_new_ant(ant_id+1)

            # dibujamos el board en el Tk
            self.board.draw()

    def finish(self):
        self.completed = True

    def step(self):
        # actualizamos el movimeinto de cada hormiga
        for ant_i in self.ant_list:
            # NOTE: para los debug, luego se quita
            # if self.mode == VISUAL:
            #     self.board.change_ant_color(ant_i.id, "blue")
                
            # buscamos el movimiento que hara la hormiga
            # actualizamos el vector direccional
            # aceleramos/frenamos la hormiga
        
            # is there any ant_j in ant_i's local area?
            near_ants = self.search_near_ants(ant_i)
            if len(near_ants) > 0:
                # if self.mode == VISUAL:
                #     for ant_j in near_ants:
                #         self.board.change_ant_color(ant_j.id, "yellow")
                    
                #     self.board.step()

                ant_i.avoid_ants(near_ants)
                acceleration = -ACELERACION*T_STEP
            else:
                ant_i.search_pheromone()
                acceleration = ACELERACION*T_STEP

            ant_i.accelerate(acceleration)

            # actualizamos ls posicion de la hormiga con su velocidad y vector direccional
            old_pos = ant_i.pos_v
            new_pos = ant_i.update_pos(T_STEP, self.border, 
                self.max_width - self.border, self.max_height/2 - self.border)
            
            # si ha llegado a un punto de inicio, actualizar la preferencia
            if coords_within_circle(self.nest, new_pos, self.radious):
                ant_i.update_preference(PREF_LEAVE)
            elif coords_within_circle(self.prey, new_pos, self.radious):
                ant_i.update_preference(PREF_RETURN)

            if self.mode == VISUAL:
                move_v = np.array(new_pos) - np.array(old_pos) # el movimiento a relizar en la pantalla
                self.board.update_ant(ant_i, move_v)

                # if self.mode == VISUAL:
                #     self.reset_ant(ant_i)
                #     for ant_j in near_ants:
                #         self.reset_ant(ant_j)

        if self.mode == VISUAL:
            self.board.step()

    def reset_ant(self, ant: Ant):
        if ant.preference == PREF_LEAVE:
            self.board.change_ant_color(ant.id, "black")
        else:
            self.board.change_ant_color(ant.id, "red")

    def save_metrics(self):
        vel_sum_return = 0
        vel_sum_leave = 0
        distance_from_centre_leave = 0
        distance_from_centre_return = 0
        ants_return = 0
        ants_leave = 0
        for ant in self.ant_list:
            if ant.preference == PREF_LEAVE:
                ants_leave += 1
                vel_sum_leave += ant.vel
                distance_from_centre_leave += ant.get_distance_from_centre()
            else:
                ants_return += 1
                vel_sum_return += ant.vel
                distance_from_centre_return += ant.get_distance_from_centre()

        if ants_leave > 0:
            mean_vel_leave = vel_sum_leave/ants_leave
            mean_dist_leave = distance_from_centre_leave/ants_leave
        else:
            mean_vel_leave = 0
            mean_dist_leave = 0

        if ants_return > 0:
            mean_vel_return = vel_sum_return/ants_return
            mean_dist_return = distance_from_centre_return/ants_return
        else:
            mean_vel_return = 0
            mean_dist_return = 0

        self.grapher.add_mean_vel_leave(mean_vel_leave, self.time)
        self.grapher.add_mean_vel_return(mean_vel_return, self.time)
        self.grapher.add_mean_dist_leave(mean_dist_leave, self.time)
        self.grapher.add_mean_dist_return(mean_dist_return, self.time)


    def search_near_ants(self, ant_i: Ant):
        near_ants = []
        for ant_j in self.ant_list:
            if ant_i.id != ant_j.id:
                near = ant_i.is_near(ant_j)
                if near:
                    near_ants.append(ant_j)

        return near_ants

    def eval(self):
        self.grapher.eval_mean_vel()
        self.grapher.eval_mean_dist()
        
       
if __name__ == "__main__":
    ants_flow = AntsFlow()

    # simulation
    ants_flow.simulate()
    # evaluation
    ants_flow.eval()