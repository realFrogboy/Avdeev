import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data = []
with open("data.txt") as f:
    for line in f:
        data.append([float(x) for x in line.split()])

with open('settings1.txt') as f:
    time = f.read(26)
    period = f.read(27)

fig, ax = plt.subplots()
x = np.arange(0, 140, 1)
y = np.asarray(data)
ax.plot(x, y, color = 'r', label = 'V(t)', marker = '.')
ax.set_title("Процесс заряда и разряда конденсатора", fontsize = 15)

ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(2))
ax.set_xlabel('Время, с', fontsize = 15)

ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.set_ylabel('Напряжение, В', fontsize = 15)

ax.grid(which = 'major', color = 'k')
ax.minorticks_on()
ax.grid(which = 'minor', color = 'gray', linestyle = ':')

ax.legend()
ax.text(90, 2.5, time, color = 'r', fontsize = 15)
ax.text(90, 2.3, period, color = 'r', fontsize = 15)

fig.set_figwidth(12)
fig.set_figheight(8)

plt.xlim([0,140])
plt.ylim([0,3.2])

fig.savefig("plot.svg")
plt.show()