
import time
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

def plotFlowPatternMap(k):

    # Draw the fixed lines, fitted from the image
    p1 = np.array([0.001, 0.0211, 123.596])
    p2 = np.array([2.2689, -330.1467])
    p3 = np.array([-0.7492, 347.6838])

    # The point where the curves meet
    xcenter = 225
    ycenter = 90

    # The points to display
    x1 = np.linspace(30,xcenter,1000)
    x2 = np.linspace(xcenter, 255, 150) 
    x3 = np.linspace(xcenter,350, 400) 
    y1 = np.polyval(p1, x1) 
    y2 = np.polyval(p2, x2)
    y3 = np.polyval(p3, x3)

    # Turn them into logscale
    y1 = 1.0052*np.exp(0.0184*y1)
    y2 = 1.0052*np.exp(0.0184*y2)
    y3 = 1.0052*np.exp(0.0184*y3)
    x1 = 0.1155*np.exp(0.0183*x1)
    x2 = 0.1155*np.exp(0.0183*x2)
    x3 = 0.1155*np.exp(0.0183*x3)


    # Plot the curves
    plt.loglog(x1, y1, 'k')
    plt.loglog(x2, y2,'k')
    plt.loglog(x3, y3, 'k')

    # Configure the plot to use latex interpreter
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    x_text = r'$\left(\frac{G_L}{G_G}\left[\frac{\rho_G}{1.2}\cdot\frac{\rho_L}{1000}\right]^{0.5} \right)\left[ \left( \mu_L(\frac{1000}{\rho_L})^2\right)^{\frac{1}{3}}\frac{0.073}{\sigma}\right]$'
    y_text = r'$\left(\frac{G_L}{G_G}\left[\frac{\rho_G}{1.2}\cdot\frac{\rho_L}{1000}\right]^{0.5}\right)$'
    plt.figure(k)
    plt.xlabel(x_text)
    plt.xlim(0.1,1000)
    plt.ylim(1,100)
    plt.ylabel(x_text)
    plt.title('Flow pattern map')
    plt.grid(True, 'both')



    plt.show()

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

def PostProcess_calc(opCond, geom, Q, OtherData):
    q_avg = Q/(math.pi*geom['D']*geom['L']*geom['N'])

    alpha_a_tot = 0.0
    alpha_i_tot = 0.0
    U_tot = 0.0
    for i in range(1, geom['Nt']+1):
        for j in range(1, geom['n']+1):
            alpha_a_tot += OtherData[i,j]['alpha_a']
            alpha_i_tot += OtherData[i,j]['alpha_i']
            U_tot += OtherData[i,j]['U']
    alpha_a_avg = alpha_a_tot/(geom['n']*geom['Nt'])
    alpha_i_avg = alpha_i_tot/(geom['n']*geom['Nt'])
    U_avg = U_tot/(geom['n']*geom['Nt'])
    R_a = 1/alpha_a_avg
    R_i = geom['D']/((geom['D']-2*geom['t'])*alpha_i_avg)
    R_w = OtherData[1,1]['R_w']

    print('Heat transfer Q [kW] %.3f: ' %Q)
    print('Average heat flux q [kW/m^2] %.3f: ' %q_avg)
    print('Average outer heat transfer coefficient [W/m^2/K] %.3f: ' %alpha_a_avg)
    print('Average inner heat transfer coefficient [W/m^2/K] %.3f: ' %alpha_i_avg)
    print('Average Overall heat transfer coefficient [W/m^2/K] %.3f: ' %U_avg)
    print('Inner thermal resistance [W/m^2/K]^-1 %.10f: ' %R_i)
    print('Outer thermal resistance [W/m^2/K]^-1 %.10f: ' %R_a)
    print('Wall thermal resistance [W/m^2/K]^-1 %.10f: ' %R_w)

    f=open('./Param/Results_Parametric.txt', 'a')

    f.write('\n Heat transfer Q [kW] : '+str(Q))
    f.write('\n Average heat flux q [kW/m^2] : '+str(q_avg))
    f.write('\n Average outer heat transfer coefficient [W/m^2/K]: ' +str(alpha_a_avg))
    f.write('\n Average inner heat transfer coefficient [W/m^2/K]: ' +str(alpha_i_avg))
    f.write('\n Average Overall heat transfer coefficient [W/m^2/K]: ' +str(U_avg))
    f.write('\n Inner thermal resistance [W/m^2/K]^-1: ' +str(R_a))
    f.write('\n Outer thermal resistance [W/m^2/K]^-1: ' +str(R_i))
    f.write('\n Wall thermal resistance [W/m^2/K]^-1: ' +str(R_w))


    f.close()
