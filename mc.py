import numpy as np
from random import randint
import dp

GAMMA = 1

def get_new_state(s, a, GRID_SIZE):
    i, j = s
    if a == 0:  # up
        return max(i - 1, 0), j
    elif a == 1:  # down
        return min(i + 1, GRID_SIZE - 1), j
    elif a == 2:  # left
        return i, max(j - 1, 0)
    elif a == 3:  # right
        return i, min(j + 1, GRID_SIZE - 1)
    raise ValueError(f'a={a} is illegal operation!')


def get_reward(s, GRID_SIZE):
    if s == (0, 0):
        return 10
    elif s == (GRID_SIZE - 1, GRID_SIZE - 1):
        return 20
    else:
        return 0


def get_value(s, GRID_SIZE):
    if s == (0, 0):
        return 10
    elif s == (GRID_SIZE - 1, GRID_SIZE - 1):
        return 20
    else:
        raise ValueError(f'{s} is not a terminal state!')


def get_episode(terminals, GRID_SIZE):
    state = get_random_state(GRID_SIZE)
    while state in terminals:
        state = get_random_state(GRID_SIZE)

    states = [state]
    actions = []
    rewards = []
    while states[-1] not in terminals:
        actions.append(randint(0, 3))  # 0 is left; 1 is right; 2 is up; 3 is down
        states.append(get_new_state(states[-1], actions[-1], GRID_SIZE))
        rewards.append(get_reward(states[-1], GRID_SIZE))

    return states, actions, rewards


def get_random_state(GRID_SIZE):
    return randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - 1)


def test_episode(GRID_SIZE):
    terminals = {(0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)}
    s, a, r = get_episode(terminals, GRID_SIZE)
    print(len(s), s, len(a), a, len(r), r, sep='\n')
    d={0: 'up', 1: 'down', 2: 'left', 3: 'right'}
    grid = [['.']*GRID_SIZE for i in range(GRID_SIZE)]
    grid[s[0][0]][s[0][1]] = 'X'
    for line in grid:
        print(line)
    print()
    print([d[i] for i in a])


def run_mc(num_of_chains, GRID_SIZE=4):
    V = np.zeros((GRID_SIZE, GRID_SIZE))
    terminals = {(0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)}
    returns = {(i, j): [0, 0] for i in range(GRID_SIZE) for j in range(GRID_SIZE)}
    V[0, 0] = 10
    V[GRID_SIZE - 1, GRID_SIZE - 1] = 20
    from time import time
    start = time()
    for i in range(num_of_chains):
        if i % 5000 == 0:
            print(f'loop #{i}')
        s, a, r = get_episode(terminals, GRID_SIZE)
        s.pop(-1)  # remove terminal state
        s.reverse()
        a.reverse()
        r.reverse()
        g = 0
        for i in range(len(r)):
            g = GAMMA * g + r[i]
            if s[i] not in s[i + 1:]:
                returns[s[i]][0] += g
                returns[s[i]][1] += 1
                V[s[i]] = returns[s[i]][0] / returns[s[i]][1]
    end = time()
    print(f'\nTotal running time for {num_of_chains} episodes is {dp.measure_time(end - start)}')
    print(np.array(V))


if __name__ == '__main__':
    # run_mc(1_000_000)
    run_mc(100_000, 4)
    run_mc(1_000, 4)


