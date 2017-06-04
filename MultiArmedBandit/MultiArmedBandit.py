import numpy, operator,math
from msvcrt import getch


# This is the slot machine
class Bandit:
    banditCount = 0

    # Constructor, gives the bandit an actual value of mean zero and variance 1
    def __init__(self):
        Bandit.banditCount += 1
        self.id = Bandit.banditCount
        self.actualValue = numpy.random.normal(0, 1)

    # Re-picks a random number for the actual value
    def randomize_actual_value(self):
        self.actualValue = numpy.random.normal(0, 1)

    # Pull lever return a float (actualValue plus random number) which acts as a reward
    def pull_lever(self):
        return self.actualValue + numpy.random.normal(0, 1)


# This is the agent that pulls the levers and keeps track of the average of each bandit
class Agent:

    # Constructor, takes a list of bandits as param, creates a default avg values array with all zeroes
    # Also initialize list that keeps track of the number of pulls, in order to calculate the average
    def __init__(self, bandits):
        self.avgValues = [0] * len(bandits)
        self.totalPulls = [0] * len(bandits)
        self.bandits = bandits

    # Finds the next lever to pull by being greedy. AKA, pulls return the index of the maximum value
    def find_max_index(self):
        index, value = max(enumerate(self.avgValues))
        return index

    # pulls the lever using Epsilon greedy method
    def epsilon_greedy_pull(self, epsilon):
        index = numpy.random.randint(0, len(self.bandits)) if (numpy.random.random_sample() > (1 - epsilon)) else self.find_max_index()
        reward = bandits[index].pull_lever()
        self.totalPulls[index] += 1
        self.recency_weighted_avg_value_calculation(reward, index, 10)

    # Calculates estimated reward based on the incremental method. This just takes the average of all the previous pulls
    def incremental_value_calculation(self, reward, index):
        self.avgValues[index] = self.avgValues[index] + (reward - self.avgValues[index]) / self.totalPulls[index]

    def recency_weighted_avg_value_calculation(self, reward, index, alpha):
        self.avgValues[index] = self.avgValues[index] + (reward - self.avgValues[index]) / alpha

    def randomize_bandits(self):
        for b in self.bandits:
            b.randomize_actual_value()


# ---------------------------------------------------------------------------------------------------------#

# Prints the actual values of the bandits
def print_bandit_values(bandits):
    banditsValues = ""
    for bandit in bandits:
        banditsValues += "ID {0}, Actual Value {1}\n".format(bandit.id, bandit.actualValue)

    index, value = get_max(bandits)
    banditsValues += "\n[Maximum is {0}, value = {1}]\n".format(index, value)
    return banditsValues


# Finds maximum in a list of bandits
def get_max(bandit_list):
    maxi = float("-inf")
    ind = 0
    count = 0
    for b in bandit_list:
        count += 1
        if b.actualValue > maxi:
            maxi = b.actualValue
            ind = count
    return ind, maxi


# An array of 10 bandits
bandits = [Bandit(), Bandit(), Bandit(), Bandit(), Bandit(), Bandit(), Bandit(), Bandit(), Bandit(), Bandit()]

kronk = Agent(bandits)

for i in range(0, 30000):
    if i % 10000 == 0:
        kronk.randomize_bandits()
        print(print_bandit_values(kronk.bandits))

    if i % 1000 == 0:
        print(kronk.avgValues)
        index = kronk.avgValues.index(max(kronk.avgValues))
        print("Best one yet is bandit number {0} with a value of {1}\n".format(index+1, kronk.avgValues[index]))

    kronk.epsilon_greedy_pull(0.1)















