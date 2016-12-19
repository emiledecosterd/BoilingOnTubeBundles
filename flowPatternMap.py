##  @package    flowPatternMap
#   Contains the functions to plot the flow pattern map 

from CoolProp.CoolProp import PropsSI
import numpy as np
import math
import matplotlib.pyplot as plt
import error
import sys
import pickle

debug = False

##  plotFlowPatternMap
#   Plots the flow pattern map separation curves and if there are results, plots them
def plotFlowPatternMap(config, results, show):

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

    # Configure the plot to use latex interpreter

    plt.rc('font', family='serif')
    x_text = r'$\left(\frac{G_L}{G_G}\left[\frac{\rho_G}{1.2}\cdot\frac{\rho_L}{1000}\right]^{0.5} \right)\left[ \left( \mu_L(\frac{1000}{\rho_L})^2\right)^{\frac{1}{3}}\frac{0.073}{\sigma}\right]$'
    y_text = r'$\left(\frac{G_L}{G_G}\left[\frac{\rho_G}{1.2}\cdot\frac{\rho_L}{1000}\right]^{0.5}\right)$'


    # Plot the curves
    fig = plt.figure()
    rect = fig.patch
    rect.set_facecolor('white')
    plt.loglog(x1, y1, 'k')
    plt.loglog(x2, y2,'k')
    plt.loglog(x3, y3, 'k')
    plt.xlabel(x_text)
    plt.ylabel(x_text)
    plt.title('Flow pattern map')
    plt.grid(True, 'both')

    # Write infos
    ax = plt.gca()
    ax.text(10, 2, r'Slug flow', fontsize=12)
    ax.text(30, 40, r'Bubbly flow', fontsize=12)
    ax.text(0.3, 70, r'Spray flow', fontsize=12)

    # Plot the points
    if config is not None and results is not None:

        # Plot all the points
        xc = results['xc']
        Tc = results['Tc']
        n = config['geom']['n']
        Nt = config['geom']['Nt']

        N_cell = np.linspace(1,n, num=n)
        N_res_x = np.zeros(n)
        N_res_y = np.zeros(n)

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

            plt.plot(N_res_x, N_res_y, '-x')

    else:
        print('INFO: No config and results given.')
        print('INFO: Plotting only the map.')

    if show:  
        plt.show()

    # Save the figure
    try:
        with open(config['filename'] + 'mplt/plot_' + 'fpm', 'wb') as fid:
            pickle.dump(fig, fid)
        fig.savefig(config['filename'] + 'images/plot_' + 'fpm'+ '.png')
    except Exception as e:
        if debug is True:
            print(e)
        else:
            raise Error('plotFlowPatternMap', 'Error writing file')




