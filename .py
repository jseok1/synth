import matplotlib.pyplot as plt
from math import log, exp

def expp(y, rate, target):
    return (y - target) * exp(rate) + target


x_ = []
atts = []
decs = []
rels = []

n = 44100
att = 0.0
dec = 1.0
rel = 0.5
for x in range(n * 2):
    x_.append(x / n)
    atts.append(att)
    att_rate = log((1.2 - 1) / 1.2) / (0.05 * 44100 * 10)
    att = expp(att - 1, att_rate, ) + 1
    decs.append(dec)
    dec = expp(dec - 0.5, 0.1 * 44100 * 10, -0.01) + 0.5
    rels.append(rel)
    rel = expp(rel, 0.1 * 44100 * 10, -0.01)

print(x)

plt.figure()
plt.plot(x_, atts)
plt.plot(x_, decs)
plt.plot(x_, rels)
plt.show()