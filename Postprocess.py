
import time
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

def makeFigure(Field, FieldName, n, Nt, show, k):

    N_cell = np.linspace(1,n,num=n)

    f=plt.figure(k)

    legendEntries=[]
    legendText=[]

    for i in range(Nt):
        plt.plot(N_cell, np.squeeze(np.asarray(Field[i+1,1:n+1])),'x-',label='Pipe '+str(i+1))

    plt.xlabel('cell #')
    plt.ylabel(FieldName)
    plt.grid(True)


    if Nt<=8:
        plt.legend().get_frame().set_alpha(0.5)
    if show==1:
        f.show()
    else:
        f.savefig('./figures/plot'+FieldName)


def plot_boiler(Th, Ph, Tc, Pc, xc, eps, n, Nt, show):
    '''
    This plots all matrixes on a wireframe 3d plot
    '''
    names=['T_w','T_w','T_wf','P_wf','x_wf', 'eps']
    k=0

    for i in Th, Ph, Tc, Pc, xc, eps:
        makeFigure(i, names[k], n, Nt, show, k)
        k+=1



def plot_xc_pipe(xc, n, Nt, show):
    '''
    This lots an average vapor quality per pipe
    '''

    x_pipe_avg=[0 for i in range(Nt)]
    x_pipe_max=[0 for i in range(Nt)]
    for i in range(Nt):
        x_pipe_avg[i] = 1/(n)*np.sum(xc[i+1,1:n+1])
        x_pipe_max[i] = np.max(xc[i+1,1:n+1])


    l=plt.figure(7)
    ax=l.gca()
    ax.bar(np.linspace(1,Nt,num=Nt)-0.3,x_pipe_avg,0.3,color='b',label='Average')
    ax.bar(np.linspace(1,Nt,num=Nt),x_pipe_max,0.3,color='r',label='Max')
    ax.set_xlabel('pipe #')
    ax.set_ylabel('Vapor quality')
    plt.legend(loc=2)

    if show==1:
        l.show()
    else:
        l.savefig('./figures/plot_avg_xc')

# def setSimName(plotName):
#     time = time.strftime("%Y%m%H%M")
#     self.simName = (time + "_" + plotName)

def PostProcess_calc(opCond, geom, Q, Pc, xc, Tc, Th, OtherData, configuration):
    q_avg = Q/(math.pi*geom['D']*geom['L']*geom['N'])

    alpha_a_tot = 0.0
    alpha_i_tot = 0.0
    U_tot = 0.0
    Delta_P_fric=0.0

    for i in range(1, geom['Nt']+1):
        for j in range(1, geom['n']+1):
            alpha_a_tot += OtherData[i,j]['alpha_a']
            alpha_i_tot += OtherData[i,j]['alpha_i']
            #U_tot += OtherData[i,j]['U']

        Delta_P_fric += OtherData[i,1]['deltaPc_f']
        Delta_P_hydro += OtherData[i,1]['deltaPc_h']

    alpha_a_avg = alpha_a_tot/(geom['n']*geom['Nt'])
    alpha_i_avg = alpha_i_tot/(geom['n']*geom['Nt'])
    #U_avg = U_tot/(geom['n']*geom['Nt'])
    #R_a = 1/alpha_a_avg
    #R_i = geom['D']/((geom['D']-2*geom['t'])*alpha_i_avg)
    #R_w = OtherData[1,1]['R_w']
    Pc_drop = Pc[ 1, 1]-Pc[ geom['Nt'], 1]
    xc_drop = xc[ geom['Nt'],1]-xc[ 0, 1]
    Th_drop = Th[1, 0] - Th[1, geom['n']]

    print('Heat transfer Q [kW] %.3f: ' %Q)
    print('Average heat flux q [kW/m^2] %.3f: ' %q_avg)
    print('Average outer heat transfer coefficient [W/m^2/K] %.3f: ' %alpha_a_avg)
    print('Average inner heat transfer coefficient [W/m^2/K] %.3f: ' %alpha_i_avg)
    #print('Average Overall heat transfer coefficient [W/m^2/K] %.3f: ' %U_avg)
    #print('Inner thermal resistance [W/m^2/K]^-1 %.10f: ' %R_i)
    #print('Outer thermal resistance [W/m^2/K]^-1 %.10f: ' %R_a)
    #print('Wall thermal resistance [W/m^2/K]^-1 %.10f: ' %R_w)

    f=open(configuration['filename'], 'a')

    f.write('Q[kW] = '+str(Q)+'\n')
    f.write('q[kW/m^2] = '+str(q_avg)+'\n')
    f.write('\alpha_a[W/m^2/K] = ' +str(alpha_a_avg)+'\n')
    f.write('\alpha_i[W/m^2/K] = ' +str(alpha_i_avg)+'\n')
    #f.write('U[W/m^2/K] = ' +str(U_avg)+'\n')
    f.write('\Delta\,P_{frictional}[Pa] = ' + str(Delta_P_fric)+'\n')
    f.write('\Delta\,P_{hydrostatic}[Pa] = ' + str(Delta_P_hydro)+'\n')
    f.write('\Delta\,P_{inlet}[Pa] = '+str(Pc_drop)+'\n')
    f.write('\Delta_x = '+str(xc_drop)+'\n')
    f.write('\Delta\,T{water} = '+str(Th_drop)+'\n')
    f.write('\n')
    #f.write('\n Inner thermal resistance [W/m^2/K]^-1: ' +str(R_a))
    #f.write('\n Outer thermal resistance [W/m^2/K]^-1: ' +str(R_i))
    #f.write('\n Wall thermal resistance [W/m^2/K]^-1: ' +str(R_w))


    f.close()
