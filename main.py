import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def q(x,x_steps,delta_x,h,q0):
    x_s = 0.2 * x_steps * delta_x
    x_max = x_steps * delta_x
    if x < x_s:
        q = q0
    elif h <= 0:
        q = 0
    else:
        #q = q0 - 2*q0*(x-x_s)/(x_f-x_s)
        q = q0 - 2*q0 * (x - x_s) / (x_max - x_s)
    return q

def f(h,m):
    return h ** (m+2)
    #return h

def method(h,f,xsteps,timesteps,delta_x,delta_t,q,lam,m):
    for n in range(timesteps-1):
        for j in range(1,xsteps-1):
            #h[n+1,j] = (-lam * delta_t / (2*delta_x)) * (f(h[n,j+1],m) - f(h[n,j-1],m)) + q(j*delta_x,xsteps,delta_x,h[n,j],1)*delta_t + h[n,j]
            a = lam * (m+2) * h[n,j]**(m+1)
            h[n+1,j] = h[n,j] - (delta_t / delta_x) * (max(a,0) * (h[n,j]-h[n,j-1]) + min(a,0) * (h[n,j+1]-h[n,j])) \
                       + q(j*delta_x,xsteps,delta_x,h[n,j],1)*delta_t

        # MIXED BIOUNDARIES??
        h[n+1,0] = h[n+1,1]
        h[n+1,-1] = h[n+1,-2]
    return h

def plotHeight(h,xsteps,delta_x):
    x = np.linspace(0,xsteps*delta_x,len(h[-1,:]))
    plt.plot(x,h[-1,:])
    plt.show()

def animate(i,x,h,line):
    line.set_data(x,h[i,:])
    return line,

def main():
    MasterFlag = {
        0: '0: Test'
    }[0]
    print(MasterFlag)
    if MasterFlag == '0: Test':
        xsteps = 100
        timesteps = 100
        delta_x = 1000
        delta_t = 0.1
        h = np.zeros((timesteps,xsteps))
        h[0,:] = 10
        h[0,:50] = 20
        h = method(h,f,xsteps,timesteps,delta_x,delta_t,q,lam=0.001,m=3)
        print(h[-1,:])
        #plotHeight(h,xsteps,delta_x)

        x = np.linspace(0, xsteps * delta_x, len(h[-1, :]))
        fig, ax = plt.subplots()
        ax.set_ylim(0,100)
        line, = ax.plot(x, h[0,:])
        ani = animation.FuncAnimation(fig, animate, len(x), fargs=[x,h,line],
                                      interval=25, blit=True)
        #ani.save('test.gif')
        plt.show()
        return 0
main()