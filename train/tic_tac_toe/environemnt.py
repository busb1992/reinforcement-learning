import matplotlib.pyplot as plt
import numpy as np

class MarkBuilder:
    def __init__(self, ax, state_obj):
        self.axes = ax
        self.state = state_obj
        self.cid = self.axes.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes!=self.axes.axes: return
        marker = self.state.get_marker()
        self.axes.plot(self.__round_to_fit_box__(event.xdata),
                       self.__round_to_fit_box__(event.ydata),
                       marker, markersize=30, color='black',
                       linewidth=10,  mfc='none')
        self.axes.figure.canvas.draw()
        self.state.set_env(int(self.__round_to_fit_box__(event.xdata) + 0.5 - 1),
                           int(self.__round_to_fit_box__(event.ydata) + 0.5 - 1),
                           marker)
        
    def __round_to_fit_box__(self, num):
        if num >= 0 and 1 > num:
            return 0.5
        elif num >= 1 and 2 > num:
            return 1.5
        elif num >= 2 and 3 > num:
            return 2.5
        else:
            return 66

class drawing_environment:

    def __init__(self, player1 = 'human', player2 = 'human'):
        self.state = state_of_env()

        if player1 == 'human':
            self.player_1 = True
        else:
            self.player_1 = False
        
        if player2 == 'human':
            self.player_2 = True
        else:
            self.player_2 = False

        self.__draw_env__()
        
    def __draw_env__(self):
        fig = plt.figure()
        self.ax = fig.add_subplot(111)
        self.ax.axis('off')
        self.ax.plot([1,1], [0,3], color='black', linewidth=5)
        self.ax.plot([2,2], [0,3], color='black', linewidth=5)
        
        self.ax.plot([0,3], [1,1], color='black', linewidth=5)
        self.ax.plot([0,3], [2,2], color='black', linewidth=5)
        
        if self.player_1 or self.player_2:
            mark_builder = MarkBuilder(self.ax, self.state)
        
        plt.show()
        
    def __convert_2_xy__(self, moove):
        convert_table = {0 : [1, 1],
                         1 : [1, 2],
                         2 : [1, 3],
                         3 : [2, 1],
                         4 : [2, 2],
                         5 : [2, 3],
                         6 : [3, 1],
                         7 : [3, 2],
                         8 : [3, 3]}
        return convert_table[moove][1], convert_table[moove][0]
        
    def new_point(self, moove):
        pos_x, pos_y = self.__convert_2_xy__(moove)
        marker = self.state.get_marker()
        self.ax.plot(pos_x - 0.5, pos_y - 0.5,
                marker, markersize=30, color='black',
                linewidth=10,  mfc='none')
        self.state.set_env(pos_x, pos_y, marker)
        
    def get_env_status(self):
        return self.state.get_env()
    
    def get_symbol(self):
        return self.state.get_marker()
    
    def colapse(self):
        plt.close()

        
class state_of_env:
    
    def __init__(self):
        self.environment_list = ['-'] * 9
        self.alternate = True

        
    def set_env(self, positnion_row, positnion_col, mark):
        self.environment_list[self.__convert_2_pos__(positnion_row, positnion_col)] = mark
        
    def get_env(self):
        return self.environment_list
    
    def __convert_2_pos__(self, positnion_col, positnion_row):
        if(positnion_row  == 0):
            default_list = [0, 1, 2]
        elif (positnion_row  == 1):
            default_list = [3, 4, 5]
        elif (positnion_row  == 2):
            default_list = [6, 7, 8]
            
        return default_list[positnion_col]
    
    def get_marker(self):
        if self.alternate:
            self.alternate = False
            return 'x'
        else:
            self.alternate = True
            return 'o'
  
'''
huhu = drawing_environment()  
'''