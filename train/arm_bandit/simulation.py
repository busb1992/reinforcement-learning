from arm_bandit import arm_bandit
import numpy as np
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
from scipy.stats import beta


class simulate_arm_bandit():

    def __init__(self,
                 list_of_probabilityes,
                 num_of_iterations_=1000,
                 epsilon_level_=5,
                 with_plot_=False,
                 initial_value_=0,
                 UCB1_=False,
                 TS_=False):

        self.num_of_iterations = num_of_iterations_
        self.epsilon_level = epsilon_level_
        self.initial_value = initial_value_
        self.UCB1 = UCB1_
        self.TS = TS_
        self.with_plot = with_plot_

        # define choosing dictionary
        # first col is given probability
        # secon is calculated one
        # third row is the num of played that bandit
        self.arr_of_arm_bandits = np.array([list_of_probabilityes,
                                            [self.initial_value] * len(list_of_probabilityes),
                                            [0] * len(list_of_probabilityes)])
        self.c_map = cm.get_cmap('prism')

        # seth alpha and betha for byesian
        self.a, self.b = 20.5, 20.5

    def exec_simulation(self):
        # itarate
        for curr_iteration in tqdm(range(1, self.num_of_iterations+1)):

            highest_calculated_prob, highest_val_place = self.__search_highest_values__(self.arr_of_arm_bandits[1, :])

            # chose arm bandit to pull
            if self.epsilon_level > random.randint(0, 100):
                # chose randomly
                self.num_of_arm_bandit = random.randint(0,
                                                        self.arr_of_arm_bandits.shape[1]-1)
            elif len(highest_val_place) > 1:
                # if at least two probab is the same at the top chose randomly
                # chose randomly from the top
                self.num_of_arm_bandit = random.choice(highest_val_place)
            else:
                # use the top
                self.num_of_arm_bandit = highest_val_place[0]

            # pull the arm
            new_arm_bandit = arm_bandit(self.arr_of_arm_bandits[0,
                                                                self.num_of_arm_bandit])
            self.result_of_arm_pull = new_arm_bandit.pull_arm()

            # refresh table
            self.arr_of_arm_bandits[2, self.num_of_arm_bandit] += 1
            self.__update_sample_mean__(curr_iteration)

            if self.with_plot:
                self.__plot_iteration_result__(curr_iteration)

        self.__print_results__()
        return self.arr_of_arm_bandits

    def __plot_iteration_result__(self, curr_iteration):
        if curr_iteration == 1:
            self.fig2, self.ax2 = plt.subplots(1, 1)
            plt.xscale('log')
        for curr_col in range(self.arr_of_arm_bandits.shape[1]):
            self.ax2.plot(curr_iteration,
                          self.arr_of_arm_bandits[1, curr_col], 'x',
                          color=self.c_map(curr_iteration))

    def __print_results__(self):
        # print results
        for curr_element in range(self.arr_of_arm_bandits.shape[1]):
            print(str(curr_element + 1) + 'th element original: '
                  + str(self.arr_of_arm_bandits[0, curr_element])
                  + ' calculated: '
                  + str(self.arr_of_arm_bandits[1, curr_element])
                  + ' played: ' + str(self.arr_of_arm_bandits[2,
                                                              curr_element]))

    def __update_sample_mean__(self, iteration_num):

        if self.UCB1:
            self.arr_of_arm_bandits[1, self.num_of_arm_bandit] = ((((1 - (1 / iteration_num))*self.arr_of_arm_bandits[0, self.num_of_arm_bandit]) + ((1 / iteration_num) * self.result_of_arm_pull)) + math.sqrt(2 * np.log(iteration_num)) / self.arr_of_arm_bandits[2, self.num_of_arm_bandit])
            return
        elif self.TS:
            if iteration_num == 1 and self.with_plot:
                self.fig, self.ax = plt.subplots(1, 1)

            # refresh alpha nad beta
            self.a, self.b = self.a + self.result_of_arm_pull, self.b + 1 - self.result_of_arm_pull

            # calc mean
            mean, _, _, _ = beta.stats(self.a, self.b, moments='mvsk')

            if self.with_plot:
                x = np.linspace(beta.ppf(0.01, self.a, self.b),
                                beta.ppf(0.99, self.a, self.b),
                                100)
                self.ax.plot(x, beta.pdf(x, self.a, self.b),
                             color=self.c_map(iteration_num),
                             lw=1)

            # refresh calculated mean
            self.arr_of_arm_bandits[1, self.num_of_arm_bandit] = mean
            return
        else:
            self.arr_of_arm_bandits[1, self.num_of_arm_bandit] = (((1 - (1 / iteration_num))*self.arr_of_arm_bandits[0, self.num_of_arm_bandit]) + ((1 / iteration_num) * self.result_of_arm_pull))
            return

    # function to get unique values
    def __search_highest_values__(self, list_):
        highest_val = 0.0
        repetitions_place = []

        for curr_element_num in range(len(list_)):
            if list_[curr_element_num] > highest_val:
                highest_val = list_[curr_element_num]
                repetitions_place = []
                repetitions_place.append(curr_element_num)
            elif list_[curr_element_num] == highest_val:
                repetitions_place.append(curr_element_num)

        return highest_val, repetitions_place


# #############################################################################
# compare different epsiolnes
# #############################################################################

list_of_probabilityes = [0.1, 0.3]
list_of_epsilones = [0.1]

for curr_eps in list_of_epsilones:
    print('results for epsilone: ' + str(curr_eps))
    sim_of_diff_eps = simulate_arm_bandit(list_of_probabilityes,
                                          num_of_iterations_=1000,
                                          epsilon_level_=curr_eps,
                                          with_plot_=True)
    result = sim_of_diff_eps.exec_simulation()

# #############################################################################
# optimistic initial value
# #############################################################################

list_of_probabilityes = [0.1]
# by setting epsilon to -1  we will always chose the highest avarage on
sim_of_optimistic = simulate_arm_bandit(list_of_probabilityes,
                                        num_of_iterations_=1000,
                                        epsilon_level_=-1,
                                        initial_value_=100,
                                        with_plot_=True)
result = sim_of_optimistic.exec_simulation()

# #############################################################################
# UCB1
# #############################################################################

list_of_probabilityes = [0.1]
# by setting epsilon to -1  we will always chose the highest avarage on
sim_of_ucb1 = simulate_arm_bandit(list_of_probabilityes,
                                  num_of_iterations_=1000,
                                  epsilon_level_=-1,
                                  with_plot_=True,
                                  UCB1_=True)
result = sim_of_ucb1.exec_simulation()

# #############################################################################
# Thomson sampling
# #############################################################################

list_of_probabilityes = [0.1]
# by setting epsilon to -1  we will always chose the highest avarage on
sim_of_bayes = simulate_arm_bandit(list_of_probabilityes,
                                   num_of_iterations_=1000,
                                   epsilon_level_=-1,
                                   with_plot_=True,
                                   TS_=True)
result = sim_of_bayes.exec_simulation()
