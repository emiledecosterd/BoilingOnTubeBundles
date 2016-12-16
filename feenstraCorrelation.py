'''
Void fraction in the cold fluid direction
'''

import sys
import math
import numpy as np
from CoolProp.CoolProp import PropsSI

# Global variable
g = 9.81


def cell_voidFraction(opCond, geom, xc_out, Tc_out, eps_in ):
    '''
    #### Void Fraction calculation ####
    This function calculate the void fraction in a vertical two-phase flows
    on tubes bundles. Following the Feenstra et al. method (cf chap17p25).

    Inputs :
        -> eps_in : Input value of the void fraction [-] (from the bottom)
        -> Operating conditions : opCond
            opCond["FluidType"] : Type of the fluid (according to the get_properties fct)
            opCond["mdot_c"] : Mass flow rate [kg/m²s]

        -> Geometrical parameters : geom
            geom["s"] : Tube pitch [m]
            geom["D"] : Tube diameter [m]

        -> Thermodynamic Variable
            xc_out : Vapor Quality (at the outlet of the cell)
            Tc_out : Cold Temperature at the outlet of the cell

    This method is an iterative method, you can change the following parameters
    at the begining of the function:
        -> kMax : Maximum numbers of iteration
        -> tol : Tolerance error

    The calculation is detailed in order to follow the Feenstra method, it could
    be simplified later.
    '''
    # General Parameter :
    g = 9.81

    ''
    # Nuemrical parameters :
    kMax = 1000
    tol = 1e-5

    k = 0
    eps = eps_in
    delta = 100

    # Get the Cold Flux properties values at the outlet of the cell :
    mu_L = PropsSI('V','T',Tc_out,'Q',0.0,opCond['FluidType'])
    mu_G = PropsSI('V','T',Tc_out,'Q',1.0,opCond['FluidType'])

    rho_L = PropsSI('D','T',Tc_out,'Q',0.0,opCond['FluidType'])
    rho_G = PropsSI('D','T',Tc_out,'Q',1.0,opCond['FluidType'])

    sigma = PropsSI('I','T',Tc_out,'Q',1.0,opCond['FluidType'])


    while (k < kMax and  delta > tol ):

        # Mean vapor velocity :
        ug = xc_out*opCond["mdot_c"]/(eps*rho_G)

        # Capillary number :
        Cap = mu_L*ug/sigma

        # Richardson number :
        Ri = (math.pow((rho_L-rho_G), 2)*g*(geom["s"]-geom["D"]))/math.pow(opCond["mdot_c"], 2)

        # Velocity ratio :
        S = 1 + 25.7*math.pow((Ri*Cap),0.5)*math.pow((geom["s"]/geom["D"]),-1)

        # Void fraction
        epsPrev = eps
        eps = math.pow((1+S*(rho_G/rho_L)*(1-xc_out)/xc_out), -1)

        delta = math.fabs(epsPrev-eps)

        k = k+1

    if (k == kMax):
        print('WARNING : Void Fraction correlation (eps) is not converged with %d iterations. \n' %kMax)
        print('You can increase the Number of iterations or change the initial value (epsInit) inside the function')
    else:
        print('Void fraction correlation converged in %d iterations. \n' %k)

    return (eps)

def ini_cell_voidFraction(opCond, geom, xc_in, Tc_in, eps_in ):
    '''
    #### Void Fraction calculation ####
    This function calculate the void fraction in a vertical two-phase flows
    on tubes bundles. Following the Feenstra et al. method (cf chap17p25).

    Inputs :
        -> eps_in : Input value of the void fraction [-] (from the bottom)
        -> Operating conditions : opCond
            opCond["FluidType"] : Type of the fluid (according to the get_properties fct)
            opCond["mdot_c"] : Mass flow rate [kg/m²s]

        -> Geometrical parameters : geom
            geom["s"] : Tube pitch [m]
            geom["D"] : Tube diameter [m]

        -> Thermodynamic Variable
            xc_in : Vapor Quality (at the inlet of the cell)
            Tc_in : Cold Temperature at the inlet of the cell

    This method is an iterative method, you can change the following parameters
    at the begining of the function:
        -> kMax : Maximum numbers of iteration
        -> tol : Tolerance error

    The calculation is detailed in order to follow the Feenstra method, it could
    be simplified later.
    '''
    # General Parameter :
    g = 9.81

    ''
    # Nuemrical parameters :
    kMax = 1000
    tol = 1e-5

    k = 0
    eps = eps_in
    delta = 100

    # Get the Cold Flux properties values at the inlet of the cell :
    mu_L = PropsSI('V','T',Tc_in,'Q',0.0,opCond['FluidType'])
    mu_G = PropsSI('V','T',Tc_in,'Q',1.0,opCond['FluidType'])

    rho_L = PropsSI('D','T',Tc_in,'Q',0.0,opCond['FluidType'])
    rho_G = PropsSI('D','T',Tc_in,'Q',1.0,opCond['FluidType'])

    sigma = PropsSI('I','T',Tc_in,'Q',1.0,opCond['FluidType'])


    while (k < kMax and  delta > tol ):

        # Mean vapor velocity :
        ug = xc_in*opCond["mdot_c"]/(eps*rho_G)

        # Capillary number :
        Cap = mu_L*ug/sigma

        # Richardson number :
        Ri = (math.pow((rho_L-rho_G), 2)*g*(geom["s"]-geom["D"]))/math.pow(opCond["mdot_c"], 2)

        # Velocity ratio :
        S = 1 + 25.7*math.pow((Ri*Cap),0.5)*math.pow((geom["s"]/geom["D"]),-1)

        # Void fraction
        epsPrev = eps
        eps = math.pow((1+S*(rho_G/rho_L)*(1-xc_in)/xc_in), -1)

        delta = math.fabs(epsPrev-eps)

        k = k+1

    if (k == kMax):
        print('WARNING : Void Fraction correlation (eps) is not converged with %d iterations. \n' %kMax)
        print('You can increase the Number of iterations or change the initial value (epsInit) inside the function')
    else:
        print('Void fraction correlation converged in %d iterations. \n' %k)

    return (eps)
# Function testing :

# ### VALIDATION OF THE FUCNTION ACCORDING TO THE EXAMPLE OF THE BOOK ###
# # Setting operating conditions and geometry
# opCond = {}
# geom ={}

# opCond['FluidType'] = 'R134a'
# xc_in = 0.2
# Tc_in = 4
# opCond["mdot_c"] = 30.0

# geom["s"] = 23.8125e-3
# geom["D"] = 19.05e-3

# epsInit = 0.5

# test = cell_voidFraction(opCond, geom, xc_in, Tc_in, epsInit )
# print(test)
