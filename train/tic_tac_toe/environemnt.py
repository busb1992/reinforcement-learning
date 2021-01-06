import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x_marker = 'x'
o_marker = 'o'
nothing_marker = '-'


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

class environment:

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
        
        self.marker_hash_value_X = 1
        self.marker_hash_value_O = 2
        
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
        
    def new_point(self, moove):
        pos_x, pos_y = self.state.__convert_2_xy__(moove)
        marker = self.state.get_marker()
        self.ax.plot(pos_x - 0.5, pos_y - 0.5,
                marker, markersize=30, color='black',
                linewidth=10,  mfc='none')
        self.state.set_env(pos_x, pos_y, marker)
    
    def set_env_pont(self, positnion_row, positnion_col, mark):
        self.state.set_env(positnion_row, positnion_col, mark)
        
    def get_env_status(self):
        return self.state.get_env()
    
    def is_game_over(self):
        return self.state.check_game_over()
    
    def get_env_status_as_hash(self):
        hash_code = 0
        vectorised_repr = self.get_env_status()
        for position in range(len(vectorised_repr)):
            value = 0
            if (vectorised_repr[position] == o_marker or
                vectorised_repr[position] == self.marker_hash_value_O):
                value = self.marker_hash_value_O
            elif (vectorised_repr[position] == x_marker or
                  vectorised_repr[position] == self.marker_hash_value_X):
                value = self.marker_hash_value_X

            hash_code += (3**position) * value

        return hash_code

    def get_symbol(self):
        return self.state.get_marker()
    
    def colapse(self):
        plt.close()

        
class state_of_env:
    
    def __init__(self):
        self.environment_list = [nothing_marker] * 9
        self.alternate = True
        
        self.nothing_repr_num = 0
        self.marker_hash_value_X = 1
        self.marker_hash_value_O = 2

        
    def set_env(self, positnion_row, positnion_col, mark):
        self.environment_list[self.__convert_2_pos__(positnion_row, positnion_col)] = mark
        
    def get_env(self):
        return self.environment_list
    
    def get_env_status_as_hash(self, vectorised_repr_of_state=[]):
        if len(vectorised_repr_of_state) == 0:
            vectorised_repr_of_state = self.environment_list
        hash_code = 0
        for position in range(len(vectorised_repr_of_state)):
            value = 0
            if (vectorised_repr_of_state[position] == o_marker or
                vectorised_repr_of_state[position] == self.marker_hash_value_O):
                value = self.marker_hash_value_O
            elif(vectorised_repr_of_state[position] == x_marker or
                  vectorised_repr_of_state[position] == self.marker_hash_value_X):
                value = self.marker_hash_value_X
                
            hash_code += (3**position) * value

        return hash_code
    
    def __convert_2_pos__(self, positnion_col, positnion_row):
        if(positnion_row  == 0):
            default_list = [0, 1, 2]
        elif (positnion_row  == 1):
            default_list = [3, 4, 5]
        elif (positnion_row  == 2):
            default_list = [6, 7, 8]
            
        return default_list[positnion_col]
    
    def __convert_2_xy__(self, pos):
        convert_table = {0 : [1, 1],
                         1 : [1, 2],
                         2 : [1, 3],
                         3 : [2, 1],
                         4 : [2, 2],
                         5 : [2, 3],
                         6 : [3, 1],
                         7 : [3, 2],
                         8 : [3, 3]}
        return convert_table[pos][1], convert_table[pos][0]
    
    def get_marker(self):
        if self.alternate:
            self.alternate = False
            return x_marker
        else:
            self.alternate = True
            return o_marker

    def check_game_ended(self, env_vec=[]):
        if len(env_vec) == 0:
            env_vec = self.environment_list
    
        if nothing_marker in env_vec or self.nothing_repr_num in env_vec:
            return False
        else:
            return True

    def check_winner(self, env_vec=[]):
        if len(env_vec) == 0:
            env_vec = self.environment_list
            
        game_finished = False

        # this is not that nice but can be effective
        winning_positions = [[0,1,2],
                             [3,4,5],
                             [6,7,8],
                             [0,3,6],
                             [1,4,7],
                             [2,5,8],
                             [0,4,8],
                             [2,4,6]]
       
        for current_win_pos in winning_positions:
            temp_list = [env_vec[i] for i in current_win_pos]
            if len(set(temp_list))==1:
                if (temp_list[0] != nothing_marker and
                    temp_list[0] != self.nothing_repr_num):
                    return temp_list[0]
        return game_finished

    def get_states_hash_and_winner(self, curr_position=0, curr_vec=[]):
        results = []
        if curr_position == len(curr_vec):
            return curr_vec[:]
        else:
            for value in range(3):
                curr_vec[curr_position] = value
                next_vec = self.get_states_hash_and_winner(curr_position+1, curr_vec)[:]
                if any(isinstance(el, list) for el in next_vec):
                    results.extend(next_vec)
                else:
                    results.append([self.get_env_status_as_hash(next_vec),
                                    self.check_game_ended(next_vec),
                                    self.check_winner(next_vec)])
                    
    
        return results
    


state = state_of_env()


state.get_env_status_as_hash([1,0,1])
huhu = state.get_states_hash_and_winner(0,['-','-','-','-','-','-','-','-','-'])

        
