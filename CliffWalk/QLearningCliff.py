# This class acts exists to represent a grid
import random


class Grid:
    def __init__(self, width, height):
        self.grid = [['|_|'] * width for _ in range(height)]
        self.grid[0][0] = 'S'
        self.grid[0][len(self.grid[0]) - 1] = 'G'

        for x in range(1, len(self.grid[0]) - 1):
            self.grid[0][x] = 'C'

    # Prints the grid, with (0, 0) being in the bottom left
    def __str__(self):
        grid_string = ""
        for row in self.grid:
            row_string = ""
            for cell in row:
                row_string += "{:^5}".format(cell)
            grid_string = row_string + "\n" + grid_string

        return grid_string

    def __repr__(self):
        return self.__str__()

    # Gets the grid cell
    def get(self, x, y):
        try:
            return self.grid[y][x]
        except IndexError:
            print("You are trying to access a value that is out of the boundaries of the grid")

    # Checks if a cell is in the grid
    def in_range(self, x, y):
        try:
            self.grid[y][x]
            return True
        except:
            return False

    # Checks if a state is a cliff
    def is_cliff(self, x, y):
        return self.get(x, y) == 'C'

    # Checks if a state is a goal
    def is_goal(self, x, y):
        return self.get(x, y) == 'G'


# This class stores all the states and all the possible actions from that state with their associated action values
class State:
    UP = (0, 1)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    # The states are stored with keys being of the form (x, y)
    states_dictionary = {}

    gr = None

    # Initializing the state with its (x, y) coords and its action dictionary
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.action_dictionary = {}

        for d in State.DIRECTIONS:
            if State.gr.in_range(self.x + d[0], self.y + d[1]) and self.x + d[0] >= 0 and self.y + d[1] >= 0:
                self.action_dictionary[d] = 0.

    # Returns a string representation of the State
    def __str__(self):
        return "({}, {}, Best Action Value: {})".format(self.x, self.y, self.get_best_action_value())

    def __repr__(self):
        return self.__str__()

    # Returns the action with the highest Q(s, a)
    def get_best_action(self):
        return max(self.action_dictionary, key=self.action_dictionary.get)

    # Gets the maximum action value
    def get_best_action_value(self):
        return max(self.action_dictionary.values())

    # Gets a state from the states_dictionary, makes a new State object if the desired state is not present
    # The state tuple is of the form (x, y)
    @staticmethod
    def get_state(state_tuple):
        # Make sure that a State is always returned
        if State.states_dictionary.get(state_tuple) is None:
            State.states_dictionary[state_tuple] = State(state_tuple[0], state_tuple[1])

        return State.states_dictionary.get(state_tuple)

    # Sets the static grid attribute
    @staticmethod
    def set_grid(grid):
        State.gr = grid

    # Returns a random valid action
    def get_random_action(self):
        return random.choice(list(self.action_dictionary.keys()))

    # Returns the action value of a certain action in this state
    def get_action_value(self, a):
        return self.action_dictionary[a]

    # Sets the action value of certain action in this state
    def set_action_value(self, a, val):
        self.action_dictionary[a] = val


# This is the agent
class Agent:
    def __init__(self, grid):
        State.set_grid(grid)
        self.position = (0, 0)
        self.grid = grid
        self.epsilon = 0.05

    # Moves the agent given an action of the form (a, b)
    def move(self, a):
        self.position = (self.position[0] + a[0], self.position[1] + a[1])

    # Chooses an action using the epsilon-greedy soft policy
    def epsilon_greedy_action(self, state):
        if random.random() >= self.epsilon:
            return state.get_best_action()
        else:
            return state.get_random_action()

    # Generates an episode starting from the start to the goal
    # Using Q-Learning, the action values are updated on the go
    def generate_episode(self, print_this_episode=False):
        self.position = (0, 0)
        tr = []
        while not self.grid.is_goal(self.position[0], self.position[1]):
            tr += [self.position]
            state = State.get_state(self.position)
            action = self.epsilon_greedy_action(state)
            self.move(action)
            fell_in_cliff = self.grid.is_cliff(self.position[0], self.position[1])
            reward = -100 if fell_in_cliff else -1
            next_state = State.get_state(self.position)
            q = state.get_action_value(action) + 0.9 * (reward + 0.9 * next_state.get_best_action_value() -
                                                        state.action_dictionary.get(action))

            state.set_action_value(action, q)

            if fell_in_cliff:
                self.position = (0, 0)
        if print_this_episode:
            print(tr)

    # Generates x number of episodes and prints the last one
    def generate_episodes(self, x):
        for i in range(0, x):
            self.generate_episode()

        temp = self.epsilon
        self.epsilon = 0
        self.generate_episode(True)
        self.epsilon = temp

# ----------------------------------------------------------------------------------------------------

g = Grid(12, 4)
agent = Agent(g)

# The final episode is printed to console
agent.generate_episodes(5000)


