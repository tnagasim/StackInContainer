# %%
from pulp import *

# %%
L = 3
W = 2
H = 2
n = 6
l = [1, 1, 2, 2, 2, 2, ]
w = [1, 1, 1, 1, 1, 1, ]
h = [2, 2, 1, 1, 1, 1, ]
M = max([L, W, H])

# %%
m = LpProblem(sense=LpMinimize)

# %%
x = [
    LpVariable("x%d" %i, lowBound=0, upBound=L, cat=LpInteger) for i in range(n)
]
y = [
    LpVariable("y%d" %i, lowBound=0, upBound=M, cat=LpInteger) for i in range(n)
]
z = [
    LpVariable("z%d" %i, lowBound=0, upBound=H, cat=LpInteger) for i in range(n)
]

# %%
a = [[LpVariable("a%d%d" %(i, j), cat=LpBinary)
    for j in range(n)] for i in range(n)]
b = [[LpVariable("b%d%d" %(i, j), cat=LpBinary)
    for j in range(n)] for i in range(n)]
c = [[LpVariable("c%d%d" %(i, j), cat=LpBinary)
    for j in range(n)] for i in range(n)]

# %%
L = LpVariable("L")
# %%
m += L
# %%
for i in range(n):
    for j in range(n):
        m += x[i] + l[i] <= x[j] + M * (1 - a[i][j])
        m += y[i] + w[i] <= y[j] + M * (1 - b[i][j])
        m += z[i] + h[i] <= z[j] + M * (1 - c[i][j])
        if i < j:
            m += a[i][j] + a[j][i] + b[i][j] + b[j][i] + c[i][j] + c[j][i] == 1
for i in range(n):
    m += x[i] <= L - l[i]
    m += y[i] <= W - w[i]
    m += z[i] <= H - h[i]

# %%
m.solve()

# %%
print(LpStatus[1])

# %%
print(value(m.objective))

# %%
print("x:", [value(e) for e in x])
print("y:", [value(e) for e in y])
print("z:", [value(e) for e in z])
print("a:", [[value(e2) for e2 in e1] for e1 in a])
print("b:", [[value(e2) for e2 in e1] for e1 in b])
print("c:", [[value(e2) for e2 in e1] for e1 in c])

# %%
import matplotlib.pyplot as plt
# %%
fig = plt.figure()
ax = fig.add_subplot(3, 1, 1, aspect='equal')
ax.set_title('y=0')
ax.set_xlim([0, value(m.objective)])
ax.set_ylim([0, H])
for i, (xi, yi, zi, li, wi, hi) in enumerate(zip(x, y, z, l, w, h)):
    if value(yi) > 0:
        continue
    rect = plt.Rectangle((value(xi), value(zi)), li, hi,
        fc="burlywood", ec="black"
        )
    ax.add_patch(rect)
ax = fig.add_subplot(3, 1, 3, aspect='equal')
ax.set_title('y=W')
ax.set_xlim([0, value(m.objective)])
ax.set_ylim([0, H])
for xi, yi, zi, li, wi, hi in zip(x, y, z, l, w, h):
    if value(yi) + wi < W:
        continue
    rect = plt.Rectangle((value(xi), value(zi)), li, hi,
        fc="burlywood", ec="black")
    ax.add_patch(rect)
# %%
