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

# Additional equations
def potential_energy(mass, height, g=9.8):
    return mass * g * height

def work_done(force, distance, angle=0):
    import math
    return force * distance * math.cos(math.radians(angle))

def power_work_time(work, time):
    return work / time

def power_voltage_current(voltage, current):
    return voltage * current

def momentum(mass, velocity):
    return mass * velocity

def impulse(force, time):
    return force * time

def centripetal_force(mass, velocity, radius):
    return mass * velocity**2 / radius

def pressure(force, area):
    return force / area

def density(mass, volume):
    return mass / volume

def buoyant_force(density_fluid, volume_displaced, g=9.8):
    return density_fluid * volume_displaced * g

def hookes_law(spring_constant, displacement):
    return spring_constant * displacement

def wave_speed(frequency, wavelength):
    return frequency * wavelength

def refractive_index(speed_light, speed_medium):
    return speed_light / speed_medium

def thermal_expansion(initial_length, coefficient, temperature_change):
    return initial_length * coefficient * temperature_change

def ideal_gas_law(pressure, volume, moles, R=8.314, temperature=None):
    if temperature is None:
        return (pressure * volume) / (moles * R)
    return pressure * volume / (R * temperature)

def coulombs_law(q1, q2, r, k=8.98755e9):
    return k * q1 * q2 / r**2

def electric_field(force, charge):
    return force / charge

def magnetic_force(charge, velocity, magnetic_field, angle=0):
    import math
    return charge * velocity * magnetic_field * math.sin(math.radians(angle))

def thermal_energy(mass, specific_heat, temperature_change):
    return mass * specific_heat * temperature_change

def efficiency(work_output, work_input):
    return (work_output / work_input) * 100

def torque(force, distance, angle=0):
    import math
    return force * distance * math.sin(math.radians(angle))

def angular_momentum(moment_of_inertia, angular_velocity):
    return moment_of_inertia * angular_velocity

def relativistic_mass(rest_mass, velocity, c=3e8):
    import math
    return rest_mass / math.sqrt(1 - (velocity**2 / c**2))