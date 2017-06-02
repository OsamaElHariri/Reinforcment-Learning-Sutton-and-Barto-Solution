import random

import TrackUtils as tu
from collections import defaultdict
track_values = [[0, 2], [-1, 4, 2], [2, 3, 2]]


track = tu.Track.make_default_track()
track2 = tu.Track(track_values)
print(track)
car = tu.Car(track)
car.off_policy_monte_carlo(2000000)
print(car.optimal_trajectory())



