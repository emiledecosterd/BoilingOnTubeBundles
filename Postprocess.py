
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

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
    a = Arrow3D([Nt/2.0,Nt/2.0],[1,n],[np.max(Th),np.max(Th)], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
    ax.add_artist(a)
    b = Arrow3D([1,Nt],[n/2.0,n/2.0],[np.max(Th),np.max(Th)], mutation_scale=20, lw=1, arrowstyle="-|>", color="b")
    ax.add_artist(b)
    ax.view_init(elev=40, azim=-145)
    f.show()

    g=plt.figure(2)
    ax1 = g.gca(projection='3d')
    ax1.plot_wireframe(N_rows, N_cell, Ph[1:Nt+1,1:n+1])
    ax1.set_xlabel('pipe')
    ax1.set_ylabel('cell #')
    ax1.set_zlabel('Ph')
    a = Arrow3D([Nt/2.0,Nt/2.0],[1,n],[np.max(Ph),np.max(Ph)], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
    ax1.add_artist(a)
    b = Arrow3D([1,Nt],[n/2.0,n/2.0],[np.max(Ph),np.max(Ph)], mutation_scale=20, lw=1, arrowstyle="-|>", color="b")
    ax1.add_artist(b)
    ax1.view_init(elev=40, azim=-145)
    g.show()

    h=plt.figure(3)
    ax2 = h.gca(projection='3d')
    ax2.plot_wireframe(N_rows, N_cell, Tc[1:Nt+1,1:n+1])
    ax2.set_xlabel('pipe')
    ax2.set_ylabel('cell #')
    ax2.set_zlabel('Tc')
    a = Arrow3D([Nt/2.0,Nt/2.0],[1,n],[Tc[1,1],Tc[1,1]], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
    ax2.add_artist(a)
    b = Arrow3D([1,Nt],[n/2.0,n/2.0],[Tc[1,1],Tc[1,1]], mutation_scale=20, lw=1, arrowstyle="-|>", color="b")
    ax2.add_artist(b)
    ax2.view_init(elev=40, azim=-55)
    h.show()

    i=plt.figure(4)
    ax3 = i.gca(projection='3d')
    ax3.plot_wireframe(N_rows, N_cell, Pc[1:Nt+1,1:n+1])
    ax3.set_xlabel('pipe')
    ax3.set_ylabel('cell #')
    ax3.set_zlabel('Pc')
    a = Arrow3D([Nt/2.0,Nt/2.0],[1,n],[Pc[1,1],Pc[1,1]], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
    ax3.add_artist(a)
    b = Arrow3D([1,Nt],[n/2.0,n/2.0],[Pc[1,1],Pc[1,1]], mutation_scale=20, lw=1, arrowstyle="-|>", color="b")
    ax3.add_artist(b)
    ax3.view_init(elev=40, azim=-55)
    i.show()

    j=plt.figure(5)
    ax4 = j.gca(projection='3d')
    ax4.plot_wireframe(N_rows, N_cell, xc[1:Nt+1,1:n+1])
    ax4.set_xlabel('pipe')
    ax4.set_ylabel('cell #')
    ax4.set_zlabel('xc')
    a = Arrow3D([Nt/2.0,Nt/2.0],[1,n],[np.max(xc),np.max(xc)], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
    ax4.add_artist(a)
    b = Arrow3D([1,Nt],[n/2.0,n/2.0],[np.max(xc),np.max(xc)], mutation_scale=20, lw=1, arrowstyle="-|>", color="b")
    ax4.add_artist(b)
    ax4.view_init(elev=40, azim=-145)
    j.show()

    k=plt.figure(6)
    ax5 = k.gca(projection='3d')
    ax5.plot_wireframe(N_rows, N_cell, eps[1:Nt+1,1:n+1])
    ax5.set_xlabel('pipe')
    ax5.set_ylabel('cell #')
    ax5.set_zlabel('eps')
    a = Arrow3D([Nt/2.0,Nt/2.0],[1,n],[eps[Nt,n],eps[Nt,n]], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
    ax5.add_artist(a)
    b = Arrow3D([1,Nt],[n/2.0,n/2.0],[eps[Nt,n],eps[Nt,n]], mutation_scale=20, lw=1, arrowstyle="-|>", color="b")
    ax5.add_artist(b)
    ax5.view_init(elev=40, azim=-145)
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
    ax.set_ylabel('Vapor quality')
    plt.legend(loc=2)
    l.show()


def PostProcess_calc(opCond, geom, Q, OtherData):
    q_avg = Q/(math.pi*0.25*geom['D']**2*geom['L']*geom['N']*geom['Nt_col'])

    alpha_a_tot = 0
    for i in range(1, geom['Nt']+1):
        for j in range(1, geom['n']+1):
            alpha_a_tot += OtherData[i,j]['alpha_a']

    alpha_a_avg = alpha_a_tot/(geom['n']*geom['Nt'])


    print('Heat transfer Q [kW] %.3f: ' %Q)
    print('Average heat flux q [kW/m^2] %.3f: ' %q_avg)
    print('Average heat transfer coefficient [W/m^2/K] %.3f: ' %alpha_a_avg)
