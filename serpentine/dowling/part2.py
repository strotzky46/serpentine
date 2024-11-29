import numpy as np
import scipy.optimize as spopt

from serpentine import Serpent

# Note Dowling's coordinate system: z pointing down (used here for now) --> theta -> -theta
# default values:
# rho0 = 1025 kg/m^3 (seawater density)
# CT = 0.0025 tangential cylinder drag coefficient
# CN = 10*CT normal cylinder drag coefficient
# CD = 1.2
# g = 9.81


# Equilibrium properties
def backend_tension_from_nbarray(array_radius, array_length, tow_speed, CT=0.0025, rho0=1025):
    """ The tension at the back end of the tow cable due to a neutrally buoyant array.
    """
    U = tow_speed
    aA = array_radius
    lA = array_length

    return rho0 * np.pi * U**2 * CT * aA * lA

def towcable_critical_angle(specific_gravity, tow_speed, cable_radius, CN=0.025, CD=1.2):
    """
    Determines the equilibrium critical angle theta_c from Dowling-2's Eq. (2.11)
    """
    g = 9.81        # m/s^2
    U = tow_speed   # m/s
    aC = cable_radius # m
    sigma = specific_gravity # rel. to surrounding medium
    lhs = lambda theta_c: (sigma - 1) * aC*g/U**2 * np.cos(theta_c)
    rhs = lambda theta_c: (CN * CD/np.pi * np.sin(theta_c)) * np.sin(theta_c)
    res = spopt.minimize(lambda theta_c : (rhs(theta_c) - lhs(theta_c))**2, -0.1)
    return res.x[0]

def gravity_force(cyl_radius, water_density, cyl_specific_gravity, cyl_length=1, g=9.81):
    """_summary_
    """
    m = water_density*cyl_specific_gravity*np.pi*cyl_radius**2*cyl_length # mass of the cylinder segment
    return np.array([0, 0, m*g]) # z-direciton points down



def solve_mean_shape(N, cable_length, cable_radius, specific_gravity, tow_speed, backend_tension=0, CT=0.0025, CN=0.025, CD=1.2, rho0=1025, g=9.81):
    """ Solves for the mean shape of a negatively buoyant cable pulling a neutrally buoyant array by direct integration over N-1 intervals
    """
    lC = cable_length   # m
    aC = cable_radius   # m
    sigma = specific_gravity
    U = tow_speed       # m/s
    d = lC/(N-1)        # finite segment length

    theta = np.zeros(N)
    T = np.zeros(N)
    l = np.linspace(0,lC,N)
    if not hasattr(sigma, '__iter__'): sigma = sigma*np.ones(N)
    if not hasattr(aC, '__iter__'): aC = aC*np.ones(N)

    # boundary conditions at tail end
    theta[-1] = 0 # horizontal angle for neutrally buoyant array
    T[-1] = backend_tension

    # solve by direct integration
    for i in range(1,N):
        T[N-1-i] = T[N-i] - d*(-rho0*(sigma[N-i] - 1)*np.pi * aC[N-i]**2 * g * np.sin(theta[N-i]) - rho0 * U**2 * np.pi*aC[N-i]*CT*np.cos(theta[N-i]))
        # allowing a slight build of tension for numerical stability
        if T[N-i] < 1e-3:
            theta[N-1-i] = theta[N-i] - d*(-rho0*(sigma[N-i]-1) * np.pi * aC[N-i]**2 * g * np.cos(theta[N-i]) + rho0*aC[N-i]*U**2*(CD*np.sin(theta[N-i]) + np.pi*CN)*np.sin(theta[N-i]))
        else:
            theta[N-1-i] = theta[N-i] - d/T[N-i]*(-rho0*(sigma[N-i]-1) * np.pi * aC[N-i]**2 * g * np.cos(theta[N-i]) + rho0*aC[N-i]*U**2*(CD*np.sin(theta[N-i]) + np.pi*CN)*np.sin(theta[N-i]))

    # return result as serpent
    serp = Serpent(N, lC, theta=-theta, phi=0*theta+ np.pi/2)
    serp.tension = T

    return serp


if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    
    data = np.array([[2, -5.11], [1.5, -7.98], [1.0,-10.33], [0.5,-22.65], [1.0,-10.82]])
    plt.figure()


    
    knts = np.linspace(0.4,5, 101)
    for CN in [1]:
        depth = []
        for knt in knts:
            U = 0.5144 * knt # 2kts tow speed
            N = 4001
            l = np.linspace(0,30,N)
            sigma = np.where(l <= 29, 1.55, 5)            
            T_array = backend_tension_from_nbarray(0.022/2, 6, U)
            serp = solve_mean_shape(4001, 30, 0.0075/2, sigma, U, T_array, CN=0.01, CT=0.0025)
            depth.append([U, serp.points[-1][2]])

        depth = np.array(depth)
        plt.plot(depth[:,0], depth[:,1], label='model')
    plt.plot(data[:,0], data[:,1], '.', label='2024-09-19 (REPMUS)')
    plt.legend()
    plt.show()

    serp.plot_summary()
    plt.show()


    

    print(np.rad2deg(towcable_critical_angle(1.55, 0.25, 0.0075/2, 1)))

