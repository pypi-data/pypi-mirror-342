# Library of SPAM random field generation functions based on R.
# Copyright (C) 2020 SPAM Contributors
# 
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
"""
This module is a wrapper around the `python library gstools <https://github.com/GeoStat-Framework/GSTools>`_ made to intuitively generate realisations of correlated Random Fields on a regular grid with a given size, discretisation and characteristic length.

"""
import numpy
import gstools
import spam.helpers
import time

def simulateRandomField(
        lengths=1.0,
        nNodes=100,
        covarianceModel='Gaussian',
        covarianceParameters={},
        dim=3,
        nRea=1,
        seed=None,
        vtkFile=None,
):
    """Generates realisations of Correlated Random Field based on the `python library gstools <https://github.com/GeoStat-Framework/GSTools>`_.
    
    Parameters
    ----------
    lengths: float | list of floats, default=1.0
        Length of the definition domain in every directions (should be size of dim). If a single float is given it will be used in each directions.
    nNodes: int | list of int, default=100
        Number of nodes in every directions. If a single float is given it will be used in each directions.
    covarianceModel: string, default="Gaussian"
        The name of the covariance model used by gstools.
        To be chosen among `this list of models <https://geostat-framework.readthedocs.io/projects/gstools/en/stable/api/gstools.covmodel.html>`_.
    covarianceParameters: dict, default={}
        A dictionnary of the keyword arguments of the covariance model used (see gstools documentation).
    dim: int default=3
        Spatial dimention
    nRea: int, default=1
        number of realisations
    seed: int, default=None
        Defines the seed for the random numbers generator. Setting a seed to a certain integer yields the same realisations.
    vtkFile: string, default=None
        If not None, the base name of the vtk files saved.

    Returns
    -------
        List of `nRea` numpy arrays if shape nNodes:
            The realisations of the random fields.

    Example
    -------
        >>> from spam.excursions import simulateRandomField
        >>>
        >>> # generation of two realisations of a Gaussian Correlated Random field
        >>> realisations = simulateRandomField(
        >>>     lengths=25,
        >>>     nNodes=100,
        >>>     dim=3,
        >>>     nRea=2,
        >>>     covarianceModel="Gaussian",
        >>>     covarianceParameters={"len_scale": 10},
        >>>     vtkFile="gaussian_randomfield"
        >>> )
        >>>
        >>> for realisation in realisations:
        >>>     print(realisation.shape)
        >>>
        >>> # generation of one realisation of a Matern Correlated Random field
        >>> realisations = simulateRandomField(
        >>>     lengths=25,
        >>>     nNodes=100,
        >>>     dim=3,
        >>>     covarianceModel="Matern",
        >>>     covarianceParameters={"len_scale": 10, "nu": 0.2},
        >>>     vtkFile="matern_randomfield"
        >>> )

    Warning
    -------
        If no rescaling factors are given in the covariance parameters it is set to 1 which deviates from gstools default behavior.
    
    """

    def _castToList(v, d, types):
        return [v] * dim if isinstance(v, types) else v        
    
    # cast lengths into a list
    lengths = _castToList(lengths, dim, (int, float))
    nNodes = _castToList(nNodes, dim, int)

    if len(lengths) != dim:
        raise ValueError(f"lengths doesn't have the good size with regards to dim {len(lengths)} != {dim}.")

    # Parameters
    # print("Random fields parameters")
    # print(f'\tLengths {lengths}')
    # print(f'\tNumber of nodes {nNodes}')
    # print(f'\tNumber of realisations {nRea}')

    # model
    if "rescale" not in covarianceParameters:
        covarianceParameters["rescale"] = 1.0
    model = getattr(gstools.covmodel, covarianceModel)(dim=dim, **covarianceParameters)
    # print(f'Covariance model ({covarianceModel})')
    # print(f'\t{model}')

    # generator
    srf = gstools.SRF(model)
    pos = [numpy.linspace(0, l, n) for n, l in zip(nNodes, lengths)]
    srf.set_pos(pos, "structured")
    seed = gstools.random.MasterRNG(seed)

    for i in range(nRea):
        tic = time.perf_counter()
        name = f'{vtkFile if vtkFile else "Field"}_{i:04d}'
        print(f"Generating {name}...", end=" ")
        srf(seed=seed(), store=name)
        print(f"{time.perf_counter() - tic:.2f} seconds")
        if vtkFile is not None:
            srf.vtk_export(name, name)

    return srf.all_fields


def parametersLogToGauss(muLog, stdLog, lcLog=1):
    """ Gives the underlying Gaussian standard deviation and mean value
    of the log normal distribution of standard deviation and mean value.

    Parameters
    ----------
        muLog: float
            Mean value of the log normal distribution.
        stdLog: float
            Standard deviation of the log normal distribution.
        lcLog: float, default=1
            Correlation length of the underlying log normal correlated Random Field.

    Returns
    -------
        muGauss: float
            Mean value of the Gaussian distribution.
        stdGauss: float
            Standard deviation of the Gaussian distribution.
        lcGauss: float
            Correlation length of the underlying Gaussian correlated Random Field.


    """
    stdGauss = numpy.sqrt(numpy.log(1.0 + stdLog**2 / muLog**2))
    muGauss = numpy.log(muLog) - 0.5 * stdGauss**2
    lcGauss = (-1.0 / numpy.log(numpy.log(1 + stdLog**2 * numpy.exp(-1.0 / lcLog) / muLog**2) / stdLog**2))**(0.5)

    return muGauss, stdGauss, lcGauss


def fieldGaussToUniform(g, a=0.0, b=1.0):
    """Transforms a Gaussian Random Field into a uniform Random Field.

    Parameters
    ----------
        g: array
            The values of the Gaussian Random Fields.
        a: float, default=0.0
            The minimum borne of the uniform distribution.
        b: float, default=1.0
            The maximum borne of the uniform distribution.

    Return
    ------
        array:
            The uniform Random Field.
    """
    from scipy.special import erf
    return float(a) + 0.5 * float(b) * (1.0 + erf(g / 2.0**0.5))


def fieldUniformToGauss(g, a=0.0, b=1.0):
    """Transforms a uniform Random Field into a Gaussian Random Field.

    Parameters
    ----------
        g: array
            The values of the uniform Random Fields.
        a: float, default=0.0
            The minimum borne of the uniform distribution.
        b: float, default=1.0
            The maximum borne of the uniform distribution.

    Return
    ------
        array:
            The Gaussian Random Field.
    """
    from scipy.special import erfinv
    return 2.0**0.5 * erfinv(2.0 * (g - float(a)) / float(b) - 1.0)
