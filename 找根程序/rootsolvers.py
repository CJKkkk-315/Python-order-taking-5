import numpy as np
import matplotlib.pyplot as plt


def fp_iteration(g, p0, Nmax):
    """
    Fixed point iterative function: Returns a numpy array of the
    results for each iteration.

    Parameters
    ----------
    g : function
        Input function for which to find a fixed point
    p0 : real number
        Start position.
    Nmax : integer
        Number of iterations to be performed.

    Returns
    -------
    p_array : numpy.ndarray, shape (Nmax,)
        Array of the results for each iteration.
    """
    p_array = np.zeros(Nmax)
    p = p0

    for i in range(Nmax):
        p = g(p)
        p_array[i] = p

    return p_array


def fp_iteration_stop(g, p0, Nmax, TOL):
    """
    Fixed point iterative function: Returns a numpy array of the
    results for each iteration.

    Parameters
    ----------
    g : function
        Input function for which to find a fixed point
    p0 : real number
        Start position.
    Nmax : integer
        Number of iterations to be performed.
    TOL : real number
        Accuracy requirements for stopping iteration
    Returns
    -------
    p_array : numpy.ndarray, shape (<=Nmax,)
        Array of the results for each iteration.
    pdiff_array : numpy.ndarray, shape (<=Nmax,)
        Array of differences between each iteration and the previous iteration
    """
    p_array = np.zeros(Nmax)
    pdiff_array = np.zeros(Nmax)
    p = p0

    for i in range(Nmax):
        new_p = g(p)
        p_array[i] = new_p
        pdiff_array[i] = np.abs(new_p - p)
        if pdiff_array[i] < TOL:
            return p_array[:i + 1], pdiff_array[:i + 1]
        p = new_p

    return p_array, pdiff_array


def newton_stop(f, dfdx, p0, Nmax, TOL):
    """
    Newton's iterative function: Returns a numpy array of the
    results for each iteration.

    Parameters
    ----------
    f : function
        Input function for which to find a fixed point
    dfdx : real number
        Derivative of input function.
    p0 : real number
        Start position.
    Nmax : integer
        Number of iterations to be performed.
    TOL : real number
        Accuracy requirements for stopping iteration
    Returns
    -------
    p_array : numpy.ndarray, shape (<=Nmax,)
        Array of the results for each iteration.
    """
    p_array = np.zeros(Nmax)
    p = p0
    for i in range(Nmax):
        p_new = p - f(p) / dfdx(p)
        p_array[i] = p_new

        if np.abs(f(p_new)) <= TOL:
            return p_array[:i+1]
        p = p_new
    return p_array


def plot_convergence(p, f, dfdx, g, p0, Nmax):
    p_array = fp_iteration(g, p0, Nmax)
    e_array = np.abs(p - p_array)
    n_array = 1 + np.arange(np.shape(p_array)[0])
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    ax.set_xlabel("n")
    ax.set_ylabel("|p-p_n|")
    ax.set_title("Convergence behaviour")
    ax.grid(True)
    ax.plot(n_array, e_array, "o", label="FP iteration ", linestyle="--")

    p_array = newton_stop(f, dfdx, p0, Nmax, 10**(-14))
    e_array = np.abs(p - p_array)
    n_array = 1 + np.arange(np.shape(p_array)[0])
    ax.plot(n_array, e_array, "*", label="Newton iteration ", linestyle="-.")
    ax.legend()
    plt.show()
    return fig, ax


def steffensen_stop(f, p0, Nmax, TOL):
    p_array = np.zeros(Nmax)
    p = p0

    for i in range(Nmax):
        q = lambda x: f(x + f(x))/f(x) - 1
        p_new = p - f(p) / q(p)
        p_array[i] = p_new
        if np.abs(f(p_new)) <= TOL:
            return p_array[:i+1]
        p = p_new

    return p_array


def plot_convergence3(p, f, dfdx, g, p0, Nmax):
    p_array = fp_iteration(g, p0, Nmax)
    e_array = np.abs(p - p_array)
    n_array = 1 + np.arange(np.shape(p_array)[0])
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    ax.set_xlabel("n")
    ax.set_ylabel("|p-p_n|")
    ax.set_title("Convergence behaviour")
    ax.grid(True)
    ax.plot(n_array, e_array, "o", label="FP iteration ", linestyle="--")

    p_array = newton_stop(f, dfdx, p0, Nmax, 10 ** (-14))
    e_array = np.abs(p - p_array)
    n_array = 1 + np.arange(np.shape(p_array)[0])
    ax.plot(n_array, e_array, "*", label="Newton iteration ", linestyle="-.")

    p_array = steffensen_stop(f, p0, Nmax, 10 ** (-14))

    e_array = np.abs(p - p_array)
    n_array = 1 + np.arange(np.shape(p_array)[0])
    ax.plot(n_array, e_array, ".", label="Steffensen iteration ", linestyle=":")


    ax.legend()
    plt.show()
    return fig, ax