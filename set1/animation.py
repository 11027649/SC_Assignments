import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
fig.set_dpi(100)
ax1 = fig.add_subplot(1,1,1)

c = 1
x0 = np.linspace(0,1,1000)
t0 = 0
dt = 0.01

def u(x,t):
    return 0.5*(np.sin(2*np.pi*(x+c*t)) + np.sin(2 * np.pi *(x-c*t)))

a = []

for i in range(500):
    value = u(x0,t0)
    t0 = t0 + dt
    a.append(value)

k = 0
def animate(i):
    global k
    x = a[k]
    k += 1
    ax1.clear()
    plt.plot(x0,x)
    plt.grid(True)
    plt.ylim([-1,1])
    plt.xlim([0,1])

anim = animation.FuncAnimation(fig,animate,frames=360,interval=20)
plt.show()

if __name__ == '__main__':
    main()
