import random
import sys


DEFAULT_STATE = '       | ###  -| # #  +| # ####|       '


class Action:

    def __init__(self, name, dx, dy):
        self.name = name
        self.dx = dx
        self.dy = dy


ACTIONS = [
    Action('UP', 0, -1),
    Action('RIGHT', +1, 0),
    Action('DOWN', 0, +1),
    Action('LEFT', -1, 0)
]


class State:

    def __init__(self, env, x, y):
        self.env = env
        self.x = x
        self.y = y

    def clone(self):
        return State(self.env, self.x, self.y)

    def is_legal(self, action):
        cell = self.env.get(self.x + action.dx, self.y + action.dy)
        return cell is not None and cell in ' +-'
    
    def legal_actions(self, actions):
        legal = []
        for action in actions:
            if self.is_legal(action):
                legal.append(action)
        return legal
    
    def reward(self):
        cell = self.env.get(self.x, self.y)
        if cell is None:
            return None
        elif cell == '+':
            return +10
        elif cell == '-':
            return -10
        else:
            return 0

    def at_end(self):
        return self.reward() != 0

    def execute(self, action):
        self.x += action.dx
        self.y += action.dy
        return self

    def __str__(self):
        tmp = self.env.get(self.x, self.y)
        self.env.put(self.x, self.y, 'A')
        s = ' ' + ('-' * self.env.x_size) + '\n'
        for y in range(self.env.y_size):
            s += '|' + ''.join(self.env.row(y)) + '|\n'
        s += ' ' + ('-' * self.env.x_size)
        self.env.put(self.x, self.y, tmp)
        return s


class Env:

    def __init__(self, string):
        self.grid = [list(line) for line in string.split('|')]
        self.x_size = len(self.grid[0])
        self.y_size = len(self.grid)

    def get(self, x, y):
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            return self.grid[y][x]
        else:
            return None

    def put(self, x, y, val):
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            self.grid[y][x] = val

    def row(self, y):
        return self.grid[y]

    def random_state(self):
        x = random.randrange(0, self.x_size)
        y = random.randrange(0, self.y_size)
        while self.get(x, y) != ' ':
            x = random.randrange(0, self.x_size)
            y = random.randrange(0, self.y_size)
        return State(self, x, y)


class QTable:


    def __init__(self, env,actions):
        self.qt = {}
        self.env = env
        self.actions = ACTIONS

    def get_q(self, state, action):
        value = self.qt.get((state.x, state.y, action.name), 0.0)
        return value

    def get_q_row(self, state):
        target = []
        for action in self.actions:
            target.append(self.get_q(state,action))
        return target


    def set_q(self, state, action, val):
        self.qt[(state.x, state.y, action.name)] = val

    def learn_episode(self, alpha=.10, gamma=.90):
        state = self.env.random_state()
        total_reward = 0
        max_int = sys.maxsize
        for i in range(max_int):
            move = random.choice(state.legal_actions(self.actions))
            formerCondition = state.clone()
            reward = state.execute(move).reward()
            q = self.get_q(formerCondition, move)
            q_row = self.get_q_row(state)
            self.set_q(formerCondition, move, (1-alpha) * q + alpha * (reward + gamma*max(q_row)))
            print(state)
            if state.at_end():
                break
        return total_reward

    
    def learn(self, episodes, alpha=.10, gamma=.90):
        total_reward = 0
        for i in range(episodes):
            self.learn_episode(alpha, gamma)
            print(self)
        return total_reward
    
    def __str__(self):
        QT = ''
        location = 0 
        for action in self.actions:
            QT += '\n' + action.name + '\n\n' 
            for y in range(self.env.y_size):
                QT += ''
                for x in range(self.env.x_size):
                    for a in range(len(self.actions)):
                        if self.actions[a] == action:
                            location = a
                            break
                    currentState = State(self.env,x,y)
                    q = self.get_q_row(currentState)[location]
                    if q == 0:
                        QT += '----'
                    else:
                        QT += '{:.2f}'.format(round(q,2))
                    QT += '\t'
                QT += '\n'
            
        return QT



if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        env = Env(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_STATE)
        if cmd == 'learn':
            qt = QTable(env, ACTIONS)
            qt.learn(100)
