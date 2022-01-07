
import math
from const import *
import numpy as np
from utils import *


class Ant:
    
    def __init__(self, id, antenale_l = L_ANTENA, ant_l = L_HORMIGA):
        self._id = id

        self.pos_v = [] # coordenadas donde se encuentra la hormiga
        self.dir_v = [] # coordenadas de direccion (cuanto queremos que avance por ud. tiempo y velocidad)
        self.pref_v = []
        self.pref_weighting = PESO_PREFERENCIA

        self._antennae_len = antenale_l
        self._antennae_grad = GRADOS_ANTENA
        self.ant_l = ant_l
        self._r_body = RADIO_HORMIGA
        self.r_visual = RADIO_VISUAL
        self.vel = V_MIN
        self._preference = None
        self.turn_rate_avoid = GIRO_EVITAR
        self.turn_rate_pheromone = GIRO_FEROMONA

    # devuelve las coordenadas en las que se encuentra la cabeza de la hormiga
    def get_head_pos(self):
        return np.array(self.pos_v) + 1/2*self.ant_l*np.array(self.dir_v)

    @property
    def id(self):
        return self._id

    @property
    def r_body(self):
        return self._r_body

    @property
    def antennae_len(self):
        return self._antennae_len
    
    @property
    def antennae_grad(self):
        return self._antennae_grad

    @property
    def preference(self):
        return self._preference

    def update_preference(self, pref):
        self._preference = pref
        if pref == PREF_LEAVE:
            self.dir_v = [1, 0]
            self.pref_v = [1, 0]
            self.turn_rate_avoid = GIRO_EVITAR
        else:
            self.dir_v = [-1, 0]
            self.pref_v = [-1, 0]
            self.turn_rate_avoid = GIRO_EVITAR_RETURN

    def is_near(self, ant):
        angle_head = angle_btw_2_points(self.pos_v, self.dir_v)
        anglemax = angle_head + GRADOS_ANTENA
        anglemin = angle_head - GRADOS_ANTENA
        return (
            coords_within_circle(self.pos_v, ant.pos_v, self.r_body)
            or coords_within_arc(self.pos_v, ant.pos_v, self.r_visual, anglemax, anglemin)
        )
    
    def search_pheromone(self):
        head_pos = self.get_head_pos()
        pos_antennae_l = self.get_antennae_pos(self.antennae_grad, head_pos)
        pos_antennae_r = self.get_antennae_pos(-self.antennae_grad, head_pos)

        c_antennae_l = self.get_pheromone_concentration(pos_antennae_l)
        c_antennae_r = self.get_pheromone_concentration(pos_antennae_r)

        saturation_l = self.get_saturation(c_antennae_l)
        saturation_r = self.get_saturation(c_antennae_r)

        if saturation_l > saturation_r:
            angle = self.calculate_saturarion_turn(pos_antennae_l, head_pos)
        elif saturation_l < saturation_r:
            angle = self.calculate_saturarion_turn(pos_antennae_r, head_pos)
        else: 
            angle = 0

        error = np.random.normal(MEDIA_GIROS, DESVIACION_GIROS)
        angle += math.degrees(error)
        self.dir_v = rotate_vector(self.dir_v, angle)

    def calculate_saturarion_turn(self, pos_antennae, head_pos):
        if pos_antennae[1] > 0:
            if pos_antennae[0] < head_pos[0]:
                angle = self.turn_rate_pheromone*T_STEP
            else:
                angle = -self.turn_rate_pheromone*T_STEP
        else:
            if pos_antennae[0] < head_pos[0]:
                angle = -self.turn_rate_pheromone*T_STEP
            else:
                angle = self.turn_rate_pheromone*T_STEP
        
        return angle

    def get_pheromone_concentration(self, pos_antennae, diffusion_t = T_DIFUSION):
        trail_radious = abs(pos_antennae[1])
        return (CANT_FEROMONA/(2*math.pi*COEF_DIFUSION*diffusion_t))*math.exp(-(trail_radious**2)/4*COEF_DIFUSION*diffusion_t)

    def get_saturation(self, c_antennae):
        saturation = math.atan(VEL_APROX_C_MAX*(c_antennae/CONCENTRACION_MAX))/(math.pi/2)
        # sensory_error = np.random.normal(MEDIA_ERROR_SATURACION, DESVIACION_ERROR_SATURACION)
        sensory_error = 0
        return saturation + sensory_error

    def update_pos(self, t_step, border_x1, border_x2, border_y):
        self.pos_v = np.array(self.pos_v) + np.array(self.dir_v)*self.vel*t_step
        # comprobamos que no salga del eje x
        if self.pos_v[0] < border_x1:
            self.pos_v[0] = border_x1
        elif self.pos_v[0] > border_x2:
            self.pos_v[0] = border_x2

        # comprobamos que no salga del eje y
        if self.pos_v[1] > border_y:
            self.pos_v[1] = border_y
        elif self.pos_v[1] < -border_y:
            self.pos_v[1] = -border_y

        return self.pos_v

    def get_antennae_pos(self, grad, head_pos):
        head_pos = np.array(head_pos)
        dir_v = np.array(self.dir_v)
        antennae_v = self._antennae_len * dir_v
        antennae_v = rotate_vector(antennae_v, grad)

        return head_pos + np.array(antennae_v)

    def accelerate(self, acc):
        self.vel += acc
        if self.vel > V_DESEADA:
            self.vel = V_DESEADA
        elif self.vel < V_MIN:
            self.vel = V_MIN

    def avoid_ants(self, near_ants):
        desired_v = np.array([0, 0])
        pos_ant_i = np.array(self.pos_v)
        pref_v = np.array(self.pref_v)
        dir_v = self.dir_v
        for ant_j in near_ants:
            pos_ant_j = np.array(ant_j.pos_v)
            diff = pos_ant_i - pos_ant_j
            if diff.all() != 0:
                desired_v = desired_v + diff/abs(diff)

        # tener en cuenta la preferencia direccional
        pref = desired_v + self.pref_weighting*pref_v
        if pref.all() != 0:
            desired_v = pref/abs(pref)

        equal_arrays = (desired_v == dir_v).all()
        if not equal_arrays:
            # rotar hacia el v deseado para evitar a las hormigas
            angle = angle_btw_2_points(dir_v, desired_v)
            turn_per_time = self.turn_rate_avoid*T_STEP
            if angle > 0:
                if dir_v[0] >= 0:
                    turn_angle = min(turn_per_time, angle)
                else:
                    turn_angle = max(-turn_per_time, -angle)
            elif angle < 0:
                if dir_v[0] >= 0:
                    turn_angle = max(-turn_per_time, -angle)
                else:
                    turn_angle = min(turn_per_time, angle)
            else:
                turn_angle = 0

            # error = np.random.normal(MEDIA_GIROS, DESVIACION_GIROS)
            # turn_angle += math.degrees(error)
            new_dir_v = rotate_vector(self.dir_v, turn_angle)
            self.dir_v = new_dir_v
