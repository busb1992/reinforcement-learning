import random

class agent():
    def __init__(self, epsilon=0.1, alpha=0.5, symbol):
        self.eps = epsilon
        self.alpha = alpha
        self.symbol = symbol
        
        self. verbose = True
        
        self.play_ground_size = 3
        
    def set_verbose(self, verboity):
        self.verbose = verboity
        
    def __get_possible_mooves__(self, environment):
        free_place = []
        for place in range(len(environment)):
            if environment[place] == '-':
                free_place.append(place)
                
        return place
    
    def take_action(self, environment):
        
        possible_mooves = self.__get_possible_mooves__(environmnet)
        random_decision = random.random()
        
        # epsilon
        if self.eps >= random_decision:
            moove = environment[random.choice(possible_mooves)]
        # greedy
        else:
            for place in possible_mooves