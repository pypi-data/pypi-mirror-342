def newton_second_law(mass, acceleration):
    return mass * acceleration

def einstein_energy(mass, c=3e8):
    return mass * c**2

def ohms_law(voltage=None, current=None, resistance=None):
    if voltage is None:
        return current * resistance
    elif current is None:
        return voltage / resistance
    elif resistance is None:
        return voltage / current

def kinetic_energy(mass, velocity):
    return 0.5 * mass * velocity**2

def gravity_force(m1, m2, r, G=6.67430e-11):
    return G * m1 * m2 / r**2
