'''
Pressure drop calculations
'''
import math
import numpy as np
from CoolProp.CoolProp import PropsSI


def cell_pressureDrop(opCond, geom, Th_out, Tc_out, Pc_in, Ph_in, eps_in, eps_out, xc_out):
    '''
    This function compute the pressure drop through the cell.
    - Ph : single-phase pressure drop inside the tubes
    - Pc : two-phase pressure drop using the void fraction computed

    Inputs :
        -> Operating conditions : opCond
            opCond["FluidType"] : Type of the fluid (according to the get_properties fct)
            opCond["mdot_h"] : Mass flow rate [kg/m²s]

        -> Geometrical parameters : geom
            geom['s'] : Tube pitch [m] (distance between the tubes axes)
            geom["L"] : Length of the tubes [m]
            geom["e"] : Surface Roughness [m]
            geom['n'] : Number of discretized cells in tube direction [-]

        -> Thermodynamic Variable
            Tc_out : Cold Temperature at the outlet of the cell
            eps_in : Void fraction at the inlet of the cell [-]
            eps_out : Void fraction at the outlet of the cell [-]

    Taking into account hydrostatic pressure and frictionnal inside the shell :
    deltaPc = deltaPc_s + deltaPc_f
    '''

    ##################################
    #### Shell pressure drop (Pc) ####
    ##################################
    g = 9.81

    # Properties
    prop = {}
    prop['mu_L'] = PropsSI('V', 'T', Tc_out, 'Q', 0.0, opCond['FluidType'])
    prop['mu_G'] = PropsSI('V', 'T', Tc_out, 'Q', 1.0, opCond['FluidType'])
    prop['rho_L'] = PropsSI('D', 'T', Tc_out, 'Q', 0.0, opCond['FluidType'])
    prop['rho_G'] = PropsSI('D', 'T', Tc_out, 'Q', 1.0, opCond['FluidType'])

    propWall = prop;


    #### Hydrostatic pressure drop ####
    deltaZ =  geom['s'] # Height of the cell (not only the diameter D)
    deltaPc_s = (prop['rho_L']*(1-(eps_in+eps_out)/2)+prop['rho_G']*(eps_in+eps_out)/2)*g*deltaZ

    #### Frictionnal pressure drop ####

    # Calculating frictionnal pressure drop in function of the geometry. There is two correlation
    # implemented for the single phase pressure drop (Zukauskas et al. and Gaddis et al.). Note that
    # the two-phase multiplier is the same for both (see Consolini et al.)

    # Compute equivalent single-phase density and viscosity
    rho_eq = prop['rho_L']*(1-eps_out)+prop['rho_G']*eps_out
    mu_eq = prop['mu_L']*(1-eps_out)+prop['mu_G']*eps_out

    # Equivalent Reynolds number
    Re = opCond['mdot_c']*geom['D']/mu_eq

    if geom['corrPD'] == 'Zukauskas':
        ## Zukauskas and Ulinska for single-phase pressure drop :

        if Re < 1000:
            Eu = 0.795 + 0.247e3/Re + 0.335e3/math.pow(Re,2) - 0.155e4/math.pow(Re,3) + 0.241e4/math.pow(Re,4)
        else:
            Eu = 0.245 + 0.339e4/Re - 0.984e7/math.pow(Re,2) + 0.132e11/math.pow(Re,3) - 0.559e13/math.pow(Re,4)

        f1 = Eu/4  # Single-Phase friction factor

    elif geom['corrPD'] == 'Gaddis':
        ## Gaddis and Gnielinski for single pressure drop

        # Geometry parameters
        a = geom['sh']/geom['D']
        b = geom['s']/geom['D']
        c = math.sqrt((a/2)**2+b**2)

        # Compute the viscosity correction factor for laminar and turbulent flow
        mu_eq_wall = propWall['mu_L']*(1-eps_out)+propWall['mu_G']*eps_out
        fzl = (mu_eq_wall/mu_eq)**(0.57/(((4*a*b/math.pi)-1)*Re)**0.25)
        fzt = (mu_eq_wall/mu_eq)**(0.14)

        if geom['layout'] == 'InLine':
            # Laminar flow in line pressure drop coefficient
            flf = (280*math.pi*(b**0.5-0.6)**2+0.75)/((4*a*b-math.pi)*a**1.6)
            zeta_lf = flf/Re

            # Turbulent flow in line pressure drop coefficient
            ftf = (0.22+1.2*((1-0.94/b)**0.6)/((a-0.85)**1.3))*10**(0.47*(b/a-1.5))+ \
                (0.03*(a-1)*(b-1))
            zeta_tf = ftf/(Re**(0.1*b/a))

            # Inlet/Outlet pressure losses influence
            if (geom['Nt'] >= 5) and (geom['Nt'] <= 10):
                fnt = (1/a**2)*(1/geom['Nt']-1/10)
            else:
                fnt = 0.;

            # Pressure drop coefficient
            zeta = zeta_lf*fzl + (zeta_tf*fzt + fnt)*(1-math.exp(-(Re+1000)/2000))

        elif geom['layout'] == 'Staggered':
            # Staggered perpendicular
            if (b >= 0.5*math.sqrt(a+1)):
                # Laminar flow staggered type pressure drop coefficient
                flv = (280*math.pi*(b**0.5-0.6)**2+0.75)/((4*a*b-math.pi)*a**1.6)

                # Inlet/Outlet pressure losses influence
                if (geom['Nt'] >= 5) and (geom['Nt'] <= 10):
                    fnt = (1/a**2)*(1/geom['Nt']-1/10)
                else:
                    fnt = 0.;

            # Stagerred diagonal
            elif (b < 0.5*math.sqrt(a+1)):
                # Laminar flow staggered type pressure drop coefficient
                flv = (280*math.pi*(b**0.5-0.6)**2+0.75)/((4*a*b-math.pi)*c**1.6)

                # Inlet/Outlet pressure losses influence
                if (geom['Nt'] >= 5) and (geom['Nt'] <= 10):
                    fnt = (2*(c-1)/(a*(a-1)))**2*(1/geom['Nt']-1/10)
                else:
                    fnt = 0.;

            # Laminar flow staggered type pressure drop coefficient
            zeta_lv = flv/Re

            # Turbulent flow staggered type pressure drop coefficient
            ftv = 2.5+1.2/((a-0.85)**1.08)+0.4*(b/a-1)**3-0.01*(a/b-1)**3
            zeta_tv = ftv/(Re**0.25)

            # Pressure drop coefficient
            zeta = zeta_lv*fzl + (zeta_tv*fzt + fnt)*(1-math.exp(-(Re+200)/1000))

        # Single-Phase friction coefficient
        f1 = zeta

    ## Consolini et al. Two-phase friction multiplier

    G0 = 400 # Reference mass flow [kg/m²s]
    Lambda = math.pow(opCond['mdot_c']/G0, -1.5)
    lmbd = Lambda + (1-Lambda)*math.pow((2*xc_out-1),2)

    f2 = lmbd * f1  # Two-Phase equivalent friction factor

    deltaPc_f = 2*f2*opCond['mdot_c']**2/rho_eq

    # Relative pressure at the output of the cell
    Pc_out = Pc_in - deltaPc_s - deltaPc_f


    ##################################
    #### Tubes pressure drop (Ph) ####
    ##################################

    # Frictional pressure drop
    deltaX = geom['L']/geom['n']
    rho = PropsSI("D", "T", Th_out, "Q", 0, "Water")
    mu = PropsSI("V", "T", Th_out, "Q", 0, "Water")

    Re_D = (opCond['mdot_h']*(geom['D']-2*geom['t']))/mu
    f = (1.8*math.log10((6.9/Re_D)+(geom['e_i']/((geom['D']-2.0*geom['t'])*3.7))**1.11))**-2.0 # [-] friction factor for rough pipes
    Re_e = Re_D*(geom['e_i']/(geom['D']-2.0*geom['t']))*(f/8.0)**0.5 # [-] Roughness Reynolds number

    if Re_D < 2000:
        f = 64/Re_D
    else:
        if Re_e < 35 :
    		# Hydrodynamically Smooth model
            f = (0.79*math.log(Re_D)-1.64)**-2.0 # [-] friction factor for smooth pipes
        else:
            f = (1.8*math.log10((6.9/Re_D)+(geom['e_i']/((geom['D']-2.0*geom['t'])*3.7))**1.11))**-2.0 # [-] friction factor for rough pipes
    deltaPh_f = f*math.pow(opCond['mdot_h'],2)*deltaX/(2*rho*geom['D'])

    # Relative pressure at the output of the cell
    Ph_out = Ph_in - deltaPh_f


    P={}
    P['Ph_out'] = Ph_out
    P['Pc_out'] = Pc_out
    P['deltaPc_f'] = deltaPc_f
    P['deltaPc_h'] = deltaPc_s
    return(P)
