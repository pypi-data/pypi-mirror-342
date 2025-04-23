"""
A collection of useful functions for controls.

| Artem Basalaev <artem[dot]basalaev[at]pm.me>
| Nils Leander Weickhardt <leander[dot]weickhardt[at]physikDOTuni-hamburg.de>

"""

from warnings import warn
import numpy as np
from scipy.signal import zpk2tf, ellip
from control import tf, frequency_response


def pairQ(f0, Q):
    """
    Parameters
    ----------
    f0  :   int/float
        Resonance Frequency
    Q   :   int/float
        Quality factor at f0

    Returns
    -------
    r1, r2  :   list of float
        List of two roots
    """

    # Check for correct input types
    if not isinstance(f0, (int, float)):
        raise ValueError("f0 has to be int or float")

    if not isinstance(Q, (int, float)):
        raise ValueError("Q has to be int or float")

    Q += 0j

    # resonant freq in rads/sec
    r0 = 2 * np.pi * f0

    res = np.sqrt(1 - 4 * Q**2)
    mag = r0 / (2 * Q)

    r1 = mag * (1 + res) / (2 * np.pi)
    r2 = mag * (1 - res) / (2 * np.pi)

    return [r1, r2]


def zpkgf(zeroes, poles, gain, gfreq):
    """Generate Virgo-style zpk system

    Parameters
    ----------
    zeroes  :   list of int/float/complex
        List of zeroes
    poles   :   list of int/float/complex
        List of poles
    gain    :   int/float
        System gain
    gfreq   :   int/float
        frequency at previously defined gain

    Returns
    -------
    control.TransferFunction
        Transfer function of the zpk system
    """

    # Check for correct input types
    if not isinstance(zeroes, list):
        raise ValueError("zeroes has to be a list")

    if not isinstance(poles, list):
        raise ValueError("poles has to be a list")

    if not isinstance(gain, (int, float)):
        raise ValueError("gain has to be int or float")

    if not isinstance(gfreq, (int, float)):
        raise ValueError("gfreq has to be int or float")

    # recast to numpy arrays
    zeroes = np.array(zeroes)
    poles = np.array(poles)

    pp = -2 * np.pi * poles
    zz = -2 * np.pi * zeroes

    sys = tf(*zpk2tf(zz, pp, 1))
    gain_init, _, _ = frequency_response(sys, 2 * np.pi * gfreq)
    kk = gain / np.abs(gain_init)

    return tf(*zpk2tf(zz, pp, kk))


def ellip_sus(freq, order, ripple, stopDB):
    """creates a low-pass elliptic filter with useful input parameters
    Parameters
    ----------
    freq    :   int/float
        frequency of 'knee'
    order   :   int/float
        number of poles
    ripple  :   int/float
        ripple DBs of ripple in the passband
    stopDB  :   int/float
        stopband which is stopDB DBs down

    Returns
    -------
    control.TransferFunction
        Transfer function of the elliptical filter
    """

    # Check for correct input types
    if not isinstance(freq, (int, float)):
        raise ValueError("freq has to be int or float")

    if not isinstance(order, (int, float)):
        raise ValueError("order has to be int or float")

    if not isinstance(ripple, (int, float)):
        raise ValueError("ripple has to be int or float")

    if not isinstance(stopDB, (int, float)):
        raise ValueError("stopDB has to be int or float")

    ellZ, ellP, K = ellip(order, ripple, stopDB, 1, "low", output="zpk", analog=True)
    ellZsc = 2 * np.pi * freq * ellZ
    ellPsc = 2 * np.pi * freq * ellP
    diff = len(ellP) - len(ellZ)
    Gain = (2 * np.pi * freq) ** diff

    return tf(
        *zpk2tf(ellZsc, ellPsc, K * Gain)
    )  # , ellZsc / (-2 * np.pi), ellPsc / (-2 * np.pi), K * Gain


def ellip_sus_z(freq, order, ripple, stopDB, zQ):
    """creates a derated low-pass elliptic filter with useful input parameters
    Parameters
    ----------
    freq    :   int/float
        frequency of 'knee'
    order   :   int/float
        number of poles
    ripple  :   int/float
        ripple DBs of ripple in the passband
    stopDB  :   int/float
        stopband which is stopDB DBs down
    zQ      :   int/float
        except the zeros are lower Q

    Returns
    -------
    control.TransferFunction
        Transfer function of the derated elliptical filter
    """

    # Check for correct input types
    if not isinstance(freq, (int, float)):
        raise ValueError("freq has to be int or float")

    if not isinstance(order, (int, float)):
        raise ValueError("order has to be int or float")

    if not isinstance(ripple, (int, float)):
        raise ValueError("ripple has to be int or float")

    if not isinstance(stopDB, (int, float)):
        raise ValueError("stopDB has to be int or float")

    if not isinstance(zQ, (int, float)):
        raise ValueError("zQ has to be int or float")

    if order < 2 or order > 3:
        warn("ellip_z only works for order 2 and 3")
        return ellip_sus(freq, order, ripple, stopDB)
    else:
        ellZ, ellP, K = ellip(
            order, ripple, stopDB, 1, "low", output="zpk", analog=True
        )
        Zsc = -abs(2 * np.pi * freq * ellZ[0])  # freq of the zero
        ellZsc = Zsc * np.array([1 + zQ * 1j, 1 - zQ * 1j]) / np.sqrt(1 + zQ**2)
        ellPsc = 2 * np.pi * freq * ellP
        diff = len(ellP) - len(ellZ)
        Gain = (2 * np.pi * freq) ** diff
        return tf(
            *zpk2tf(ellZsc, ellPsc, K * Gain)
        )  # , ellZsc / (-2 * np.pi), ellPsc / (-2 * np.pi), K * Gain
