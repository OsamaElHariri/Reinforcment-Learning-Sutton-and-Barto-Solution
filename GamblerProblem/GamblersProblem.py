V = [0.0] * 101
policy = [0] * 101

prob_heads = 0.40


# Calculates the state-values for each state after one iteration of policy evaluation
def calculate_state_values_helper():
    diff = 0.0
    for i in range(1, len(V) - 1):
        temp = V[i]

        maximum = -200
        best_action = 0
        for a in range(1, min(i, len(V) - i - 1) + 1):
            rew = 1 if i + a == 100 else 0
            val = prob_heads * (rew + V[i + a]) + (1 - prob_heads) * (V[i - a])
            if val > maximum + 10**-16:
                best_action = a
                maximum = val

        policy[i] = best_action
        V[i] = maximum
        diff = max(diff, abs(temp - V[i]))

    return diff


# Calculates the state-values for all states
def calculate_state_values():
    theta = 1e-30
    while True:
        if calculate_state_values_helper() < theta:
            break

calculate_state_values()
print(V)
print(policy)
