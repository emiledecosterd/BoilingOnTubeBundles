
from CoolProp.CoolProp import PropsSI
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

import pickle


def plotFlowPattern(config, results, current_plot):

    xc = results['xc']
    Tc = results['Tc']
    n = config['geom']['n']
    Nt = config['geom']['Nt']

    N_cell = np.linspace(1,n, num=n)
    N_res_x = np.empty( n)
    N_res_y = np.empty(n)

    # Loop through all cells
    for i in range(1, Nt+1):
        for j in range(1, n+1):

            # Get the properties needed to calculate coefficients for the map
            xc_temp = xc[i, j]
            Tc_temp = Tc[i, j]

            rho_L = PropsSI('D', 'T', Tc_temp, 'Q', 0.0, config['opCond']['FluidType'])
            rho_G = PropsSI('D', 'T', Tc_temp, 'Q', 1.0, config['opCond']['FluidType'])
            mu_L = PropsSI('viscosity', 'T', Tc_temp, 'Q', 0.0, config['opCond']['FluidType'])
            GL_GG = 1/xc_temp-1
            G_G = config['opCond']['mdot_c']*xc_temp
            sigma = PropsSI('surface_tension', 'T', Tc_temp, 'Q', 0.0, config['opCond']['FluidType'])

            # Calculate the coefficients
            abscisse = GL_GG*np.power(rho_G*rho_L/1200, 1/3)*(np.power(mu_L*(1000/rho_L)**2, 1/3)*0.073/sigma)
            ordonnee = G_G*np.power(rho_G*rho_L/1200, -1/2)

            # Save value to be plotted
            N_res_x[j-1] = abscisse
            N_res_y[j-1] = ordonnee

        current_plot.plot(N_res_x, N_res_y)





def plotFlowPatternMap(config, results, show):

    # show = True

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

    # Plot the points
    plotFlowPattern(config, results, plt)

    # Configure the plot to use latex interpreter
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    x_text = (r'$\left(\frac{G_L}{G_G}\left[\frac{\rho_G}{1.2}\cdot\frac{\rho_L}{1000}\right]^{0.5} \right)\left[ \left( \mu_L(\frac{1000}{\rho_L})^2\right)^{\frac{1}{3}}\frac{0.073}{\sigma}\right]$')
    y_text = (r'$\left(\frac{G_L}{G_G}\left[\frac{\rho_G}{1.2}\cdot\frac{\rho_L}{1000}\right]^{0.5}\right)$')
    fig = plt.figure(100)
    plt.xlabel(x_text)
    plt.xlim(0.1,1000)
    plt.ylim(1,100)
    plt.ylabel(x_text)
    plt.title('Flow pattern map')
    plt.grid(True, 'both')

    if show:  
        plt.show()

    # Save the figure
    with open(config['filename'] + 'mplt/plot_' + 'fpm', 'wb') as fid:
        pickle.dump(fig, fid)
        fig.savefig(config['filename'] + 'images/plot_' + 'fpm'+ '.png')

    plt.rc('text', usetex=False)


def makeFigure(Field, FieldName, latexName, config, show, k):
    n = config['geom']['n']
    Nt = config['geom']['Nt']

    N_cell = np.linspace(1,n,num=n)

    f = plt.figure()

    f.set_figheight(11)
    f.set_figwidth(8.5)

    rect = f.patch
    rect.set_facecolor('white')

    plt.rc('font', family='serif')

    legendEntries=[]
    legendText=[]

    for i in range(Nt):
        plt.plot(N_cell, np.squeeze(np.asarray(Field[i+1,1:n+1])),'x-',label=r'$Pipe '+ str(i+1)+'$')

        plt.xlabel(r'$Cell \quad \#$')
        plt.ylabel(latexName)
        plt.grid(True)


    if Nt<=8:
        plt.legend().get_frame().set_alpha(0.5)

    if show :
        f.show()
    else:
        with open(config['filename'] + 'mplt/plot_'+ FieldName, 'wb') as fid:
            pickle.dump(f, fid)
        f.savefig(config['filename'] + 'images/plot_'+ FieldName +'.png')




def plot_boiler(config, results, show):
    '''
    This plots all matrixes on a wireframe 3d plot
    '''

    names=['T_w','P_w','T_wf','P_wf','x_wf', 'eps']
    latexNames=[r'$T_{w}$',r'$P_{w}$',r'$T_{wf}$',r'$P_{wf}$',r'$x_{wf}$',r'$\varepsilon$']
    resultsNames = ['Th','Ph','Tc','Pc','xc','eps']
    k=0

    for key in resultsNames :
        name = names[resultsNames.index(key)]
        latexName = latexNames[resultsNames.index(key)]
        field = results[key]
        makeFigure(field, name, latexName, config, show, k)
        k+=1



def plot_xc_pipe(config, results, show):

    '''
    This lots an average vapor quality per pipe
    '''
    n = config['geom']['n']
    Nt = config['geom']['Nt']
    xc = results['xc']

    x_pipe_avg=[0 for i in range(Nt)]
    x_pipe_max=[0 for i in range(Nt)]
    for i in range(Nt):
        x_pipe_avg[i] = 1/(n)*np.sum(xc[i+1,1:n+1])
        x_pipe_max[i] = np.max(xc[i+1,1:n+1])


    l=plt.figure()
    l.set_figheight(11)
    l.set_figwidth(8.5)

    rect = l.patch
    rect.set_facecolor('white')

    ax=l.gca()
    ax.set_aspect('auto')
    ax.bar(np.linspace(1,Nt,num=Nt)-0.3,x_pipe_avg,0.3,color='b',label='Average')
    ax.bar(np.linspace(1,Nt,num=Nt),x_pipe_max,0.3,color='r',label='Max')
    ax.set_xlabel('pipe #')
    ax.set_ylabel('Vapor quality')
    plt.legend(loc=2)

    if show==1:
        l.show()
    else:
        with open(config['filename'] + 'mplt/plot_avg_xc', 'wb') as fid:
            pickle.dump(l, fid)
        l.savefig(config['filename'] + 'images/plot_avg_xc'+'.png')


def PostProcess_calc(config, results):
    geom = config['geom']
    Q = results['Q']
    OtherData = results['OtherData']
    Pc = results['Pc']
    xc = results['xc']
    Tc = results['Tc']
    Th = results['Th']

    q_avg = Q/(math.pi*geom['D']*geom['L']*geom['N'])

    alpha_a_tot = 0.0
    alpha_i_tot = 0.0
    U_tot = 0.0

    Delta_P_fric=0.0
    Delta_P_hydro=0.0

    for i in range(1, geom['Nt']+1):
        for j in range(1, geom['n']+1):
            alpha_a_tot += OtherData[i,j]['alpha_a']
            alpha_i_tot += OtherData[i,j]['alpha_i']

        Delta_P_fric += OtherData[i,1]['deltaPc_f']
        Delta_P_hydro += OtherData[i,1]['deltaPc_h']

    alpha_a_avg = alpha_a_tot/(geom['n']*geom['Nt'])
    alpha_i_avg = alpha_i_tot/(geom['n']*geom['Nt'])

    Pc_drop = Pc[ 0, 1]-Pc[ geom['Nt'], 1]
    xc_drop = xc[ geom['Nt'],1]-xc[ 0, 1]
    Th_drop = Th[1, 0] - Th[1, geom['n']]

    print('Heat transfer Q [kW] %.3f: ' %Q)
    print('Average heat flux q [kW/m^2] %.3f: ' %q_avg)
    print('Average outer heat transfer coefficient [W/m^2/K] %.3f: ' %alpha_a_avg)
    print('Average inner heat transfer coefficient [W/m^2/K] %.3f: ' %alpha_i_avg)

    newFilename = config['filename'] + '_res.txt'
    f=open(newFilename, 'a')

    f.write('Q[kW] = '+str(Q)+'\n')
    f.write('q[kW/m^2] = '+str(q_avg)+'\n')
    f.write('\\alpha_a[W/m^2/K] = ' +str(alpha_a_avg)+'\n')
    f.write('\\alpha_i[W/m^2/K] = ' +str(alpha_i_avg)+'\n')
    f.write('\Delta\,P_{frictional}[Pa] = ' + str(Delta_P_fric)+'\n')
    f.write('\Delta\,P_{hydrostatic}[Pa] = ' + str(Delta_P_hydro)+'\n')
    f.write('\Delta\,P_{inlet}[Pa] = '+str(Pc_drop)+'\n')
    f.write('\Delta\,x[-] = '+str(xc_drop)+'\n')
    f.write('\Delta\,T_{water}[K] = '+str(Th_drop)+'\n')
    f.write('\n')

    f.close()

    results['q_avg'] = q_avg
    results['alpha_a_avg'] = alpha_a_avg
    results['alpha_i_avg'] = alpha_i_avg

    return(results)
