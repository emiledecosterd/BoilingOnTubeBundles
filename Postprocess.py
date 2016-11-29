
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_boiler(Th, Ph, Tc, Pc, xc, eps, n, Nt):
    '''
    This plots all matrixes on a wireframe 3d plot
    '''

    N_cell, N_rows=np.meshgrid(np.linspace(1,n,num=n),np.linspace(1,Nt,num=Nt))

    f=plt.figure(1)
    ax = f.gca(projection='3d')
    ax.plot_wireframe(N_rows, N_cell, Th[1:Nt+1,1:n+1])
    ax.set_xlabel('pipe')
    ax.set_ylabel('cell #')
    ax.set_zlabel('Th')
    ax.text(1.5,4,286,'flow of water ==>',zdir=(0,1,0))
    ax.text(1,4,300,'flow of coolant ==>',zdir=(1,0,0))
    f.show()

    g=plt.figure(2)
    ax1 = g.gca(projection='3d')
    ax1.plot_wireframe(N_rows, N_cell, Ph[1:Nt+1,1:n+1])
    ax1.set_xlabel('pipe')
    ax1.set_ylabel('cell #')
    ax1.set_zlabel('Ph')
    ax1.text(1.5,4,1e5,'flow of water ==>',zdir=(0,1,0))
    ax1.text(1,4,1e5,'flow of coolant ==>',zdir=(1,0,0))
    g.show()

    h=plt.figure(3)
    ax2 = h.gca(projection='3d')
    ax2.plot_wireframe(N_rows, N_cell, Tc[1:Nt+1,1:n+1])
    ax2.set_xlabel('pipe')
    ax2.set_ylabel('cell #')
    ax2.set_zlabel('Tc')
    ax2.text(1.5,4,274,'flow of water ==>',zdir=(0,1,0))
    ax2.text(1,4,272,'flow of coolant ==>',zdir=(1,0,0))
    h.show()

    i=plt.figure(4)
    ax3 = i.gca(projection='3d')
    ax3.plot_wireframe(N_rows, N_cell, Pc[1:Nt+1,1:n+1])
    ax3.set_xlabel('pipe')
    ax3.set_ylabel('cell #')
    ax3.set_zlabel('Pc')
    ax3.text(1.5,4,290000,'flow of water ==>',zdir=(0,1,0))
    ax3.text(1,4,288500,'flow of coolant ==>',zdir=(1,0,0))
    i.show()

    j=plt.figure(5)
    ax4 = j.gca(projection='3d')
    ax4.plot_wireframe(N_rows, N_cell, xc[1:Nt+1,1:n+1])
    ax4.set_xlabel('pipe')
    ax4.set_ylabel('cell #')
    ax4.set_zlabel('xc')
    ax4.text(1.5,4,0,'flow of water ==>',zdir=(0,1,0))
    ax4.text(1,4,1,'flow of coolant ==>',zdir=(1,0,0))
    j.show()

    k=plt.figure(6)
    ax5 = k.gca(projection='3d')
    ax5.plot_wireframe(N_rows, N_cell, eps[1:Nt+1,1:n+1])
    ax5.set_xlabel('pipe')
    ax5.set_ylabel('cell #')
    ax5.set_zlabel('eps')
    ax.text(1.5,4,0,'flow of water ==>',zdir=(0,1,0))
    ax.text(1,4,1,'flow of coolant ==>',zdir=(1,0,0))
    k.show()


def plot_xc_pipe(xc, n, Nt):
    '''
    This lots an average vapor quality per pipe
    '''

    x_pipe_avg=[0 for i in range(0,Nt)]
    x_pipe_max=[0 for i in range(0,Nt)]
    for i in range(1,Nt+1):
        x_pipe_avg[i-1] = 1/n*np.sum(xc[i-1,1:n+1])
        x_pipe_max[i-1] = np.max(xc[i-1,1:n+1])


    l=plt.figure(7)
    ax=l.gca()
    ax.bar(np.linspace(1,Nt,num=Nt)-0.3,x_pipe_avg,0.3,color='b',label='Average')
    ax.bar(np.linspace(1,Nt,num=Nt),x_pipe_max,0.3,color='r',label='Max')
    ax.set_xlabel('pipe #')
    ax.set_ylabel('average vapor quality')
    plt.legend()
    l.show()
