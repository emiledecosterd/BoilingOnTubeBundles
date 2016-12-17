import math
import numpy as np
from properties import get_properties
from CoolProp.CoolProp import PropsSI

Tc_out = 273 + 0
opCond = {}
opCond['FluidType'] = 'R134a'


prop = get_properties(Tc_out, opCond['FluidType'])
print(prop['mu_L'])

muL = PropsSI('V', 'T', Tc_out, 'Q', 0, opCond['FluidType'])
print(muL)