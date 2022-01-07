import matplotlib.pyplot as plt
from const import GRAPH_MIN_TIME

class Grapher:
    
    def __init__(self, min_time = GRAPH_MIN_TIME):
        self.min_time = min_time
        self.mean_vel_return = {} # diccionario { time_step : mean_vel }
        self.mean_vel_leave = {} # diccionario { time_step : mean_vel }

    def add_mean_vel_leave(self, mean_vel, time_step):
        if time_step >= self.min_time: 
            self.mean_vel_leave[time_step] = mean_vel

    def add_mean_vel_return(self, mean_vel, time_step):
        if time_step >= self.min_time:
            self.mean_vel_return[time_step] = mean_vel

    def eval_mean_vel(self):
        mean_vel_leave = self.mean_vel_leave.values()
        mean_vel_return = self.mean_vel_return.values()
        time_steps = self.mean_vel_return.keys()

        # plotting the points
        plt.plot(time_steps, mean_vel_leave, label="Ants leaving")
        plt.plot(time_steps, mean_vel_return, label="Ants returning")

        # naming the x axis
        plt.xlabel('Time (s)')
        # naming the y axis
        plt.ylabel('Mean velocity of ants (cm/s)')
        # showing the legend
        plt.legend()
        
        # function to show the plot
        plt.show()