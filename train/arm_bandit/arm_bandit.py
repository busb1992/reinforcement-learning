import random

class arm_bandit():
    
    def __init__(self, win_probability):
        self.percent_on_ones = int(win_probability * 100)
        self.population = self.__generate_distribution__()

    def pull_arm(self):
        return self.population[random.randint(0, len(self.population)-1)]
        
    def __generate_distribution__(self):
        
        distribuition = ([0] * (100 - self.percent_on_ones))
        distribuition.extend([1] * self.percent_on_ones)
        random.shuffle(distribuition)          
        return distribuition
    
