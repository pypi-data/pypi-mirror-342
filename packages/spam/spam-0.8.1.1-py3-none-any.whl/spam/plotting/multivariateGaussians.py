"""
Library of SPAM functions for plotting multivariate gaussians
Copyright (C) 2020 SPAM Contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import matplotlib.pyplot as plt
import numpy
from matplotlib import cm


def plotMultivariateGaussians(phi, mean, hessian, n=100):

    X = numpy.linspace(mean[0] - 0.1 * hessian[0][0], mean[0] + 0.1 * hessian[0][0], n)
    Y = numpy.linspace(mean[1] - 0.1 * hessian[1][1], mean[1] + 0.1 * hessian[1][1], n)

    X, Y = numpy.meshgrid(X, Y)
    gauss = numpy.zeros((n, n))

    print(X)
    print(Y)
    for ny in range(n):
        y = Y[ny, 0]
        for nx in range(n):
            x = X[0, nx]
            h = numpy.array([x, y])
            gauss[nx, ny] = float(phi) * numpy.exp(-0.5 * (numpy.dot(numpy.dot(h - mean, hessian), h - mean)))
            # print h, gauss[ nx, ny ]

    fig = plt.figure()
    ax = fig.gca(projection="3d")
    ax.plot_surface(X, Y, gauss, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    plt.show()
