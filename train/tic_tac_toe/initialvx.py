import numpy as np

def initialV_x(state_winner_triples):
  # initialize state values as follows
  # if x wins, V(s) = 1
  # if x loses or draw, V(s) = 0
  # otherwise, V(s) = 0.5
  V = np.zeros(len(state_winner_triples))
  for state, ended, winner in state_winner_triples:
    if ended:
      if winner == 1:
        v = 1
      else:
        v = 0
    else:
      v = 0.5
    V[state] = v
  return V

V = initialV_x(huhu)

for i in hihi:
    if i != 0.5:
        print(i)