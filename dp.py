import numpy as np
from time import time


def get_new_state(i, j, a, GRID_SIZE):
    if a == 0:  # up
        return max(i - 1, 0), j
    elif a == 1:  # down
        return min(i + 1, GRID_SIZE - 1), j
    elif a == 2:  # left
        return i, max(j - 1, 0)
    elif a == 3:  # right
        return i, min(j + 1, GRID_SIZE - 1)
    raise ValueError(f'a={a} is illegal operation!')


def get_reward(i, j, GRID_SIZE):
    if (i, j) == (0, 0):
        return 0
    elif (i, j) == (GRID_SIZE - 1, GRID_SIZE - 1):
        return 0
    else:
        return 0


def get_value(V, pi, i, j, GAMMA, GRID_SIZE):
    if (i, j) == (0, 0):
        return 10
    elif (i, j) == (GRID_SIZE - 1, GRID_SIZE - 1):
        return 20
    else:
        result = 0
        # print(f'i,j={i},{j}')
        for a in range(len(pi)):
            new_i, new_j = get_new_state(i, j, a, GRID_SIZE)
            # print(new_i,new_j)
            result += pi[a] * (get_reward(new_i, new_j, GRID_SIZE) + GAMMA * V[new_i, new_j])
        # print(result)
        return result


def measure_time(total):
    hours = total / 3600
    minutes = (total % 3600) / 60
    seconds = total % 60
    if hours >= 1:
        return f'{int(hours*100)/100} hours'
    elif minutes >= 1:
        return f'{int(minutes*100)/100} minutes'
    else:
        return f'{int(seconds*100)/100} seconds'



def run_dp(theta=0.001, GRID_SIZE=4, GAMMA=1):

    V = np.zeros((GRID_SIZE, GRID_SIZE))
    pi = np.tile(0.25, 4)

    start = time()
    delta = 2 * theta
    loop = 0
    while delta > theta:
        delta = 0
        loop += 1
        #     if loop % 1000 == 0:
        #         print(loop)
        print(f'\nloop #{loop}')
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                v = V[i, j]
                V[i, j] = get_value(V, pi, i, j, GAMMA, GRID_SIZE)
                delta = max(delta, abs(v - V[i, j]))
        print(f'delta={delta}')

    end = time()
    print(f'\nTotal running time for {loop} loops is {measure_time(end - start)}')
    print(np.array(V))


if __name__ == '__main__':
    run_dp()







