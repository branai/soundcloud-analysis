def percent_change(s):
    p_change = []
    for i in range(1, len(s)):
        p_change.append((s[i] - s[i - 1])/s[i - 1])
    return p_change

def actual_change(s):
    p_change = []
    for i in range(1, len(s)):
        p_change.append(s[i] - s[i - 1])
    return p_change
