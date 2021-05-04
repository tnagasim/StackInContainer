# %%
from pulp import *
import random

# %%
W = 20
n = 5
w = [9, 4, 3, 7, 5]
h = [4, 10, 9, 9, 10]
UB = sum(h)

# %%
m = LpProblem(sense=LpMinimize)

# %%
x = [LpVariable("x%d" %i, lowBound=0) for i in range(n)]
# %%
y = [LpVariable("y%d" %i, lowBound=0) for i in range(n)]

# %%
u = [[LpVariable("u%d%d" %(i, j), cat=LpBinary)
    for j in range(n)] for i in range(n)]

# %%
v = [[LpVariable("v%d%d" %(i, j), cat=LpBinary)
    for j in range(n)] for i in range(n)]

# %%
H = LpVariable("H")
# %%
m += H
# %%
for i in range(n):
    for j in range(n):
        m += x[i] + w[i] <= x[j] + W * (1 - u[i][j])
        m += y[i] + h[i] <= y[j] + UB * (1 - v[i][j])
        if i < j:
            m += u[i][j] + u[j][i] + v[i][j] + v[j][i] >= 1
for i in range(n):
    m += x[i] <= W - w[i]
    m += y[i] <= H - h[i]
# %%
m.solve()

# %%
print(LpStatus[1])

# %%
print(value(m.objective))

# %%
print("x:", [value(e) for e in x])
print("y:", [value(e) for e in y])
print("u:", [[value(e2) for e2 in e1] for e1 in u])
print("v:", [[value(e2) for e2 in e1] for e1 in v])

# %%
import matplotlib.pyplot as plt
# %%
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.set_xlim([0, W])
ax.set_ylim([0, value(m.objective)])
for xi, yi, wi, hi in zip(x, y, w, h):
    rect = plt.Rectangle((value(xi), value(yi)), wi, hi,
        fc="burlywood", ec="black")
    ax.add_patch(rect)
# %%
