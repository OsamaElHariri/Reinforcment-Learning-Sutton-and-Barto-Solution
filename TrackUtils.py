"""" The track is constructed as a 2d, square grid. The way to construct the track is by passing the constructor
 a list of lists. The sub-lists must be of the form [a, b, c] or [d, e], where a, b, c, d, e are integers, and each
 sub-list corresponds to one row in the track. If the sub-list is of length 2, then the third element is implicitly
 counted as 1. The first element in the sublist is the offset from the previous element. So, if the list passed to 
 the constructor is = [[0, 5], [-1, 4]], then the second sub-list corresponds to a row that is shifted once to the left.
 If the list is = [[0, 5], [-1, 4], [1, 3]], then the third sublist corresponds to a row that is sifted once to the
 right, relative to the second row, meaning it starts on the same vertical axis as the first row. 
    The second element in the sub-list is the length of the valid squares in the row, so a sub-list like [a, b, c] 
 will correspond to a row whose valid squares are of length b. 
    The third element in the sublist corresponds to how many consecutive duplicates of the row are present. So, a 
 sub-list like [a, b, 3] is equivalent to [[a, b], [0, b], [0, b]]. An absent third element means that there is only
 one copy of that row.
    Rows that do not span the whole square grid have None entries to fill the blanks
 """
import random


class Track:
    default_values1 = [[0, 6, 3], [-1, 7, 7], [-1, 8, 8], [-1, 9, 7], [0, 10],
                       [0, 17, 2], [1, 16], [1, 15, 2], [1, 14]]
    default_values2 = [[0, 23, 3], [1, 22], [1, 21], [1, 20], [1, 19], [1, 18],
                       [1, 17], [1, 16], [1, 15], [1, 14], [1, 13], [1, 12], [1, 11],
                       [1, 10], [1, 9], [0, 10], [0, 12], [0, 13],
                       [0, 16], [-1, 19], [-1, 20], [-1, 21, 4], [1, 20],
                       [1, 19], [3, 16]]

    # Constructor
    def __init__(self, segments=default_values1):
        self.track = None
        self.start = []
        self.finish = []
        self.track_height = 0
        self.track_width = 0
        self.offset = 0
        self.construct_track(segments)
        self.find_default_start()
        self.find_default_finish()
        self.start_finish_aesthetics()

    # Return a string representation of the 2d grid. None cells are represented by an X
    def __str__(self):
        if not self.track:
            return "Track not yet initialized"
        str = ""
        count = -1
        for row in self.track:
            count += 1
            row_str = ""
            for val in row:
                if isinstance(val, float) or isinstance(val, int):
                    row_str += "{0:^7.2f}".format(val)
                else:
                    row_str += "{0:^7}".format("X" if val is None else val)
            str = row_str + "| {}".format(count) + "\n" + str
        temp = "\n"
        for i in range(-self.offset, self.track_width - self.offset):
            temp = "{0:^7}{1}{2:^7}".format('-----', temp, i)
        str += temp
        str = "\n" + str + "\n"
        return str

    # Constructs the track as a grid, with the first entry being the bottom most row
    def construct_track(self, triplets):
        temp_offset = 0
        max_offset = 0
        for triplet in triplets:
            self.is_legal(triplet)
            temp_offset -= triplet[0]
            max_offset = max(max_offset, temp_offset)
            self.track_height += (1 if len(triplet) == 2 else triplet[2])

            # Calculating track_width: This line keeps track of the highest horizantal value. This does not take
            #  into account that it might have started before the 'origin'. This is why we must add the offset later
            self.track_width = max(self.track_width, triplet[1] - temp_offset)
        self.offset = 0 if max_offset <= 0 else max_offset
        self.track_width += self.offset

        rows = []
        temp_offset = 0
        for triplet in triplets:
            temp_offset += triplet[0]
            nones = [None] * (self.track_width + 1)
            nones[temp_offset + self.offset: temp_offset + self.offset + triplet[1] + 1] = [0.] * triplet[1]

            # This line adds the duplicate rows if the triplet is of length 3 (Meaning there are duplicate rows)
            rows += [nones * 1 for _ in range(1 if len(triplet) != 3 else triplet[2])]
        self.track = rows

    # Check if a list is of length 2 or 3 and if it contains only integers
    # Returns true if the tuple is legal, raises an error otherwise
    def is_legal(self, triplet):
        length = len(triplet)
        if length < 2 or length > 3:
            raise SyntaxError("The values in the list passed to the Track class must be of length 2 or 3")

        if not all(isinstance(item, int) for item in triplet):
            raise TypeError("The values in the list passed to the Track class must only contain integers")

        return True

    # Returns the value at the specified location.
    # Parameters: i is the horizontal coordinate, and j is the vertical
    # i is shifted by the offset in order for the point (0, 0) to correspond to the bottom-most, left-most valid cell
    def get(self, i, j):
        return self.track[j][i + self.offset]

    # Sets a track position to the specified value
    # Parameters: i is the horizontal coordinate, and j is the vertical
    # i is shifted by the offset in order for the point (0, 0) to correspond to the bottom-most, left-most valid cell
    def set(self, i, j, val):
        if self.get(i, j) is None:
            raise Exception("You are trying to set a value that is outside the Track")

        self.track[j][i + self.offset] = val

    # Returns false if the cell is off the track, true otherwise, coords is a tuple of the form (i, j)
    def valid_cell(self, coords):
        try:
            return self.get(coords[0], coords[1]) is not None
        except IndexError:
            # If we reached here, it means we are out of the track grid,
            # meaning we will get an IndexError because we are out of bounds, so it is not a valid cell
            return False

    # Sets the start cells as the valid cells in the bottom most row
    def find_default_start(self):
        for i in range(-self.offset, self.track_width - self.offset):
            if self.get(i, 0) is not None:
                self.start += [[i, 0]]

    # Sets the default finish cells as the right most, valid cells
    def find_default_finish(self):
        for j in range(self.track_height):
            if self.get(self.track_width - 1 - self.offset, j) is not None:
                self.finish += [[self.track_width - 1 - self.offset, j]]

    # Replaces the start and finish cells with the letters S and F respectively
    def start_finish_aesthetics(self):
        for coord in self.start:
            self.set(coord[0], coord[1], "Start")

        for coord in self.finish:
            self.set(coord[0], coord[1], "Finish")

    # Factory method that returns ready made tracks
    @staticmethod
    def make_default_track(choice=1):
        return Track(Track.default_values1 if choice == 1 else Track.default_values2)


# This acts as the agent.
class Car:
    max_speed = 3

    # Constructor
    def __init__(self, track):
        self.trajectory = []
        # The speeds and position are randomized through the call to random_start_position()
        self.vertical_speed = 0
        self.horizontal_speed = 0
        self.position = [0, 0]
        self.epsilon = 0.5

        self.track = track if isinstance(track, Track) else Track.make_default_track(1)
        self.random_start_position()

    # Returns a string representation of the car
    def __str__(self):
        return "Position = {}, Horizontal speed = {}, Vertical speed = {}".format(self.position, self.horizontal_speed,
                                                                                  self.vertical_speed)

    # Generates an episode by moving the car from the start to the finish, choosing different actions on each step
    def generate_episode(self):
        first_non_greedy_action = None
        while not self.check_finish(self.position):
            state = State.get_state((self.position[0], self.position[1], self.horizontal_speed, self.vertical_speed))
            action, greedy = self.epsilon_greedy_action(state)

            # Keeping track of the first time we did not take the optimal action
            if not greedy and first_non_greedy_action is None:
                first_non_greedy_action = len(self.trajectory)

            reward = self.check_reward(state, action)
            self.trajectory += [(state, action, reward)]
            self.apply_action(action)
            self.move()
        return first_non_greedy_action

    # Applies the Off-Policy Monte Carlo learning method to the model
    def off_policy_monte_carlo(self, iterations):
        for _ in range(-1, iterations):
            self.reset()
            nongreedy_action_index = self.generate_episode()

            # If nongreedy_action_index is None, the all the actions taken were greedy and optimal. Skip this trajectory
            if nongreedy_action_index is None:
                continue

            # Remove the trajectory entries where an optimal action is taken
            # See page 123 in the book http://people.inf.elte.hu/lorincz/Files/RL_2006/SuttonBook.pdf
            self.trajectory = self.trajectory[nongreedy_action_index:]
            W, G = 1., 0

            for step in self.trajectory:
                action_info = step[0].get_action_value(step[1])
                weight_denominator = self.epsilon / len(step[0].action_dictionary)
                W = W * (1 / weight_denominator) if step[1] == step[0].get_best_action() else (1 / (1 - self.epsilon + weight_denominator))
                """ TODO THE REWARD DOESNT WORK LIKE THIS!!! The current state's returns is this reward
                plus the discounted reward of the next state. The next states reward is its rewards plus the
                discounted reward of its next state. WE ARE CURRENTLY DOING THIS BACKWARDS!!!"""

                G = 0.90 * G + step[2]
                N = action_info[1] + (W * G)
                D = action_info[2] + W
                step[0].set_action_value(step[1], (N / D, N, D))

    # Applies an action to the speeds of the car
    def apply_action(self, a):
        self.horizontal_speed += a[0]
        self.vertical_speed += a[1]

    # Returns a random starting position from the starting positions of the track
    def random_start_position(self):
        self.trajectory = []
        self.vertical_speed = random.randrange(0, Car.max_speed + 1)
        self.horizontal_speed = random.randrange(0, Car.max_speed + 1)
        if self.vertical_speed == 0 and self.horizontal_speed == 0:
            if random.random() > 0.5:
                self.vertical_speed += 1
            else:
                self.horizontal_speed += 1

        start = self.track.start
        self.position = start[random.randrange(0, len(start), 1)]

    # Moves the car by updating its position. If the car drives off the edge, or does not move at all,
    # the position is clipped(preventing the car from going off the edge) using the method move_slowly()
    # or moved once up or to the right if it remained stationary
    def move(self):
        new_pos = [self.position[0] + self.horizontal_speed, self.position[1] + self.vertical_speed]

        if self.track.valid_cell(new_pos):
            self.position = new_pos
        else:
            temp = [self.position[0], self.position[1]]
            self.move_slowly()
            # Checking if the agent moved. We do this because the agent must move after each step
            if temp == self.position:
                coords = [self.position[0] + 1, self.position[1]]
                coords2 = [self.position[0], self.position[1] + 1]
                # If the agent did not move, then either up or right are invalid. We take a step in the valid direction
                if self.track.valid_cell(coords):
                    self.position = coords
                elif self.track.valid_cell(coords2):
                    self.position = coords2

    # Moves the agent in an alternating fashion of up and right one step at a time(This is the clipping of the move)
    def move_slowly(self, remaining_x_moves=None, remaining_y_moves=None, moved=True, going_up=True):
        remaining_x_moves = self.horizontal_speed if remaining_x_moves is None else remaining_x_moves
        remaining_y_moves = self.vertical_speed if remaining_y_moves is None else remaining_y_moves

        remaining = remaining_y_moves if going_up else remaining_x_moves
        valid = False
        if remaining > 0:
            coords = [self.position[0] + (0 if going_up else 1),
                      self.position[1] + (1 if going_up else 0)]
            valid = self.track.valid_cell(coords)
        if valid:
            self.position = coords
            remaining_x_moves -= 0 if going_up else 1
            remaining_y_moves -= 1 if going_up else 0
        if valid or moved:
            self.move_slowly(remaining_x_moves, remaining_y_moves, valid, not going_up)

    # Chooses an action using the epsilon-greedy soft policy
    # Returns a tuple. First, the appropriate action. Second, returns True if the action chosen
    # is the best action, False otherwise
    def epsilon_greedy_action(self, state):
        if random.random() >= self.epsilon:
            return state.get_best_action(), True
        else:
            a = state.get_random_action()
            return a, (a == state.get_best_action())

    # Checks the reward of the next step, taking an action, a, into account. Reward of -1 if the car stays on
    # the track, -5 otherwise
    def check_reward(self, state, a):
        coords = (state.xpos + state.xspeed + a[0], state.ypos + state.yspeed + a[1])
        return -1 if self.track.valid_cell(coords) else -5

    # Checks if a cell is on a Finish cell. The pos is of the form [x, y]
    def check_finish(self, pos):
        return [pos[0], pos[1]] in self.track.finish

    # Return the optimal trajectories for all start positions and a random vertical and horizontal speeds
    def optimal_trajectory(self):
        temp_epsilon = self.epsilon
        self.epsilon = 0
        trajectories = ""
        for coords in self.track.start:
            self.reset()
            self.position = coords
            self.generate_episode()
            trajectories += "\n{}\n".format(self.trajectory)
        self.epsilon = temp_epsilon
        return trajectories

    # Conveniently named function
    def reset(self):
        self.random_start_position()


# This class stores all the states and all the possible actions from that state with their associated action values
class State:
    actions = [(1, 1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (-1, -1)]

    # The states are stored with keys being of the form (xpos, ypos, xspeed, yspeed)
    states_dictionary = {}

    def __init__(self, xpos, ypos, xspeed, yspeed):
        self.xpos = xpos
        self.ypos = ypos
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.action_dictionary = {}

        for pair in State.actions:
            # First, check if the conditions on the vertical and horizontal speeds are satisfied,
            # then add the action to the dictionary
            if 0 <= self.xspeed + pair[0] <= Car.max_speed and 0 <= self.yspeed + pair[1] <= Car.max_speed \
                    and (self.xspeed + pair[0] != 0 or self.yspeed + pair[1] != 0):
                # Every action in this state has 3 values associated with it, (Q(s, a), N(s, a), D(s, a)),
                # where Q is the action value, N is the numerator, and D the denominator
                # See page 123 in the book http://people.inf.elte.hu/lorincz/Files/RL_2006/SuttonBook.pdf
                self.action_dictionary[pair] = (-6., 0., 0.)

    # Returns a string representation of the state
    def __str__(self):
        return "xpos = {}, ypos = {}, xspeed = {}, yspeed = {}\nAction Dictionary:\n{}\n" \
            .format(self.xpos, self.ypos, self.xspeed, self.yspeed, self.action_dictionary.items())

    # Returns a string og the state as a tuple
    def __repr__(self):
        #return "({}, {}, {}, {})".format(self.xpos, self.ypos, self.xspeed, self.yspeed)
        return self.__str__()

    # Returns the action with the highest Q(s, a)
    def get_best_action(self):
        return max(self.action_dictionary, key=self.action_dictionary.get)

    # Returns a random valid action
    def get_random_action(self):
        return random.choice(list(self.action_dictionary.keys()))

    # Gets a state from the states_dictionary, makes a new State object if the desired state is not present
    # The state tuple is of the form (xpos, ypos, xspeed, yspeed)
    @staticmethod
    def get_state(state_tuple):
        # Make sure that a State is always returned
        if State.states_dictionary.get(state_tuple) is None:
            State.states_dictionary[state_tuple] = State(state_tuple[0], state_tuple[1], state_tuple[2], state_tuple[3])

        return State.states_dictionary.get(state_tuple)

    # Returns the action value of a certain action in this state
    def get_action_value(self, a):
        return self.action_dictionary[a]

    # Sets the action value of certain action in this state
    def set_action_value(self, a, val):
        self.action_dictionary[a] = val

    # Returns the state in tuple form
    def tuple_form(self):
        return self.xpos, self.ypos, self.xspeed, self.yspeed
