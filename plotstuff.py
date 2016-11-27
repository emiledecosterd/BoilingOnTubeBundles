
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_boiler(Th, Ph, Tc, Pc, xc, eps, n, Nt):


    N_cell, N_rows=np.meshgrid(np.linspace(1,n,num=n),np.linspace(1,Nt,num=Nt))

    f=plt.figure(1)
    ax = f.add_subplot(111, projection='3d')
    ax.plot_wireframe(N_rows, N_cell, Th[1:Nt+1,1:n+1])
    ax.set_xlabel('pipe')
    ax.set_ylabel('cell #')
    ax.set_zlabel('Th')
    f.show()

    g=plt.figure(2)
    ax1 = g.add_subplot(111, projection='3d')
    ax1.plot_wireframe(N_rows, N_cell, Ph[1:Nt+1,1:n+1])
    ax1.set_xlabel('pipe')
    ax1.set_ylabel('cell #')
    ax1.set_zlabel('Ph')
    g.show()

    h=plt.figure(3)
    ax2 = h.add_subplot(111, projection='3d')
    ax2.plot_wireframe(N_rows, N_cell, Tc[1:Nt+1,1:n+1])
    ax2.set_xlabel('pipe')
    ax2.set_ylabel('cell #')
    ax2.set_zlabel('Tc')
    h.show()

    i=plt.figure(4)
    ax3 = i.add_subplot(111, projection='3d')
    ax3.plot_wireframe(N_rows, N_cell, Pc[1:Nt+1,1:n+1])
    ax3.set_xlabel('pipe')
    ax3.set_ylabel('cell #')
    ax3.set_zlabel('Pc')
    i.show()

    j=plt.figure(5)
    ax4 = j.add_subplot(111, projection='3d')
    ax4.plot_wireframe(N_rows, N_cell, xc[1:Nt+1,1:n+1])
    ax4.set_xlabel('pipe')
    ax4.set_ylabel('cell #')
    ax4.set_zlabel('xc')
    j.show()

    k=plt.figure(6)
    ax5 = k.add_subplot(111, projection='3d')
    ax5.plot_wireframe(N_rows, N_cell, eps[1:Nt+1,1:n+1])
    ax5.set_xlabel('pipe')
    ax5.set_ylabel('cell #')
    ax5.set_zlabel('eps')
    k.show()

    input()


#Th=np.matrix([[0,0,0,0,0],[0,1,1,1,1],[0,2,2,2,2]])
#plot_boiler(Th, 1, 1, 1, 1, 1, 4, 2)
