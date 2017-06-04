# Solution adapted from http://lumiere.ens.fr/~dmarti01/software/jack.pdf

import numpy as np, math

ncar_states = 21
max_moves = 5
max_morning = ncar_states + max_moves
discount = 0.9
theta = 10**(-7)

lambda_1r = 3.0     # Request rate and Drop off rate at location 1 and 2
lambda_1d = 3.0
lambda_2r = 4.0
lambda_2d = 2.0

prob_1 = [[0.] * ncar_states for _ in range(max_morning)]
prob_2 = [[0.] * ncar_states for _ in range(max_morning)]
rew_1 = [0.] * max_morning
rew_2 = [0.] * max_morning

V = [[0.] * ncar_states for _ in range(ncar_states)]
policy = [[0] * ncar_states for _ in range(ncar_states)]


# Calculates the Poisson probability of some number x
# Parameters are the number x and the expected number l (l for lambda)
def poisson(x, l):
    return math.exp(-l) * (l ** x) / math.factorial(x)


# Initialize probs and rewards according to the request and drop off rates
def load_probs_rewards(probs, rewards, l_reqsts, l_drpffs):
    req = 0
    req_prob = poisson(req, l_reqsts)
    while req_prob > theta:

        # Filling the reward matrix
        for n in range(0, max_morning):
            # This min is taken into account because we do not get the reward if there were 20 requests but we only have
            # 10 cars, for example. If the requests exceed the number of available cars, we get a reward equal
            # to 10 * number of cars rented. Of course, this event is not guaranteed, since it is not 100% that
            # there will be 20 requests, there is a req_prob chance that there will be 20 requests, so we also
            # multiply the reward by the req_prob
            satisfied_req = min(req, n)
            rewards[n] += 10 * satisfied_req * req_prob

        drp = 0
        drp_prob = poisson(drp, l_drpffs)
        while drp_prob > theta:
            # Fill probability matrix probs
            for m in range(0, max_morning):
                satisfied_req = min(req, m)
                # We have m cars right now, new_n is a possible next state after the requests and drop offs
                new_n = m + drp - satisfied_req
                new_n = max(new_n, 0)
                new_n = min(ncar_states - 1, new_n)

                # We can get to state new_n from m in a lot of different request and drop off rates. For example,
                # we can start with 6 cars and we can end up with 5 cars if there were 1 request and 0 drop off,
                # or 2 requests and 1 drop off, or 3 requests and 2 drop offs, etc.
                # req_prob and drp_prob encapsulate the chances of getting 1, 2 or X requests or drop offs respectively
                probs[m][new_n] += req_prob * drp_prob

            drp += 1
            drp_prob = poisson(drp, l_drpffs)
        req += 1
        req_prob = poisson(req, l_reqsts)


# Calculates the rewards for the states given an action a
def backup_action(n1, n2, a):
    a = min(a, +n1)
    a = max(a, -n2)
    a = min(+max_moves, a)
    a = max(-max_moves, a)
    val = -2 * abs(a) if abs(a) > 2 else 0  # Since someone is will shuttle one car for free
    morning_n1 = int(n1 - a)
    val += -4 if morning_n1 > 10 else val   # If there are more than 10 cars, we must pay 4$
    morning_n2 = int(n2 + a)
    val += -4 if morning_n2 > 10 else val   # If there are more than 10 cars, we must pay 4$
    for new_n1 in range(0, ncar_states):
        for new_n2 in range(0, ncar_states):
            val += prob_1[morning_n1][new_n1] * prob_2[morning_n2][new_n2] *\
                   (rew_1[morning_n1] + rew_2[morning_n2] + discount * V[new_n1][new_n2])
    return val


# Evaluate the current policy
def policy_eval():
    while True:
        diff = 0.0
        for n1 in range(0, ncar_states):
            for n2 in range(0, ncar_states):
                val_tmp = V[n1][n2]
                a = policy[n1][n2]
                V[n1][n2] = backup_action(n1, n2, a)
                diff = max(diff, abs(V[n1][n2] - val_tmp))

        if diff <= theta:
            break


# Improve the current policy
def update_policy_t():
    has_changed = False
    for n1 in range(0, ncar_states):
        for n2 in range(0, ncar_states):
            b = policy[n1][n2]
            policy[n1][n2] = greedy_policy(n1, n2)
            if b != policy[n1][n2]:
                has_changed = True
    return has_changed


# Picks the policy while being greedy
def greedy_policy(n1, n2):
    # Sets the range of available actions, which is from -max_moves to +max_moves. We are bounding because we
    # cannot send 5 cars if we only have 3, for example
    a_min = max(-max_moves, -n2)
    a_max = min(+max_moves, +n1)

    # Here we are checking which move (AKA how many cars we are moving) yields the highest reward
    a = a_min
    best_action = a_min
    best_val = backup_action(n1, n2, a)
    for a in range(a_min + 1, a_max + 1):
        val = backup_action(n1, n2, a)
        if val > best_val + 10**(-9):
            best_val = val
            best_action = a

    return best_action


# Prints the policy
def print_policy():
    print("\nPolicy")
    for n1 in range(0, ncar_states):

        pol = ""
        for n2 in range(0, ncar_states):
            pol += " {0:2} ".format(policy[ncar_states - (n1+1)][n2])
        print(pol)


load_probs_rewards(prob_1, rew_1, lambda_1r, lambda_1d)
load_probs_rewards(prob_2, rew_2, lambda_2r, lambda_2d)


while True:
    policy_eval()
    changed = update_policy_t()
    if changed:
        break


print_policy()
print("\n\nDONE!!!!!")

