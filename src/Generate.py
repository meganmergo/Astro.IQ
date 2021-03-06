# Resources
from Trajectory import Point_Lander_Drag
from Optimisation import HSS
from PyGMO import *
from numpy import *
import multiprocessing

def main(n):

    ''' -------------------------------------------------
    Problem       : SpaceX Dragon 2 Martian Soft Landing
    Dynamics      : 2-Dimensional Variable Mass Point
    Transcription : Hermite Simpson Seperated (HSS)
    Produces      : Database of fuel-optimal trajectories
    >>> python Generate.py
    ------------------------------------------------- '''

    print("Beginning with dataset " + str(n))
    si_list = load('Data/Point_Lander_Mars_Initial_States_' + str(n) + '.npy')
    # Define the algorithms to use
    algo_local = algorithm.scipy_slsqp(max_iter=5000, screen_output=True)
    # Load initial guess
    print("Loading initial guess..")
    z = load('Data/HSS_10_Mars_Base.npy')
    # Alot space for solutions
    n_traj = len(si_list)
    sols   = zeros((0, len(z)))
    for i in range(n_traj):
        si      = si_list[i]
        print("Trajectory " + str(i))
        print("State: " + str(si))
        # Initialise the model at that state
        model   = Point_Lander_Drag(si)
        # Initialise the HSS problem
        prob    = HSS(model, nsegs=10)
        # Create empty population
        pop     = population(prob)
        # Guess the previous solution
        pop.push_back(z)
        # Optimise from that solution
        print("Beginning optimisation...")
        pop     = algo_local.evolve(pop)
        # Save the solution if succesfull
        if prob.feasibility_x(pop.champion.x):
            z = array(pop.champion.x)
	    # Update the solution array
	    sols = vstack((sols, z))
	    save("Data/Mars/HSS_10_Alpha_" + str(n), sols)


if __name__ == "__main__":
    jobs = [1,2,3,4]

    for n in jobs:
        p = multiprocessing.Process(target=main, args=(n,))
        p.start()
