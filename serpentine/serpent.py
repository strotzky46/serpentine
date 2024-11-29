#

import numpy as np
import matplotlib.pyplot as plt

class Serpent():
    """ 
    A class definiing a 1D segmentation of a towed, flexible cylinder with 
    local properties.
    """
    
    def __init__(self, num_segments, length=1, CN=None, CT=None, mass=None, theta=None, phi=None):
        """ """
        self.n = num_segments
        self.length = length
        self.step = self.length/(self.n)

        if theta is None: 
            self.theta = np.zeros(self.n)
        else:
            self.theta = theta

        if phi is None: 
            self.phi = np.zeros(self.n)
        else:
            self.phi = phi
        
        self.build()


    def build(self):
        """ """
        self.segments = self.step*np.array([[np.cos(th), np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph)] for (th, ph) in zip(self.theta, self.phi)])
        self.points = np.vstack((np.zeros(3), np.cumsum(self.segments, axis=0)))
        self.bbox = np.array([[np.min(self.points[:,i]), np.max(self.points[:,i])] for i in range(3)])
        self.center = np.mean(self.bbox, axis=1)
        L = np.max(np.diff(self.bbox, axis=1))
        self.bcube = np.reshape(self.center, (3,1)) + np.array([[-1.1*L/2, 1.1*L/2]])


    def plot(self, ax=None, xy=(0,1), scatter_kwargs={}, **plot_kwargs):
        """ """
        if ax is None:
            ax = plt.gca()
        
        scatter_kwargs.update(plot_kwargs)
        # ax.plot(self.points[:-1,xy[0]], self.points[:-1,xy[1]], '.C0', **scatter_kwargs)
        ax.plot(self.points[:,xy[0]], self.points[:,xy[1]], '-C0', **plot_kwargs)

        ax.set_aspect(1.0)
        ax.set_xlim(self.bcube[xy[0]])
        ax.set_ylim(self.bcube[xy[1]])
        ax.set_xlabel('XYZ'[xy[0]])
        ax.set_ylabel('XYZ'[xy[1]])

        return ax

    def plot3d(self, ax=None, scatter_kwargs={}, **plot_kwargs):
        """ """
        if ax is None:
            ax = plt.gca()
        if '3d' not in ax.name:
            raise ValueError('Cannot plot 3d into {} axes.'.format(ax.name))
        
        scatter_kwargs.update(plot_kwargs)
        # ax.plot(self.points[:-1,0], self.points[:-1,1], self.points[:-1,2], '.C0', **scatter_kwargs)
        ax.plot(self.points[:,0], self.points[:,1], self.points[:,2], '-C0', **plot_kwargs)
        ax.set_xlim(self.bcube[0])
        ax.set_ylim(self.bcube[1])
        ax.set_zlim(self.bcube[2])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        return ax
    
    def plot_summary(self, fig=None, scatter_kwargs={}, **plot_kwargs):
        """ """
        if fig is None:
            fig = plt.gcf()

        ax = plt.subplot(2,2,1)
        self.plot(ax=ax, xy=(0,1))
        ax = plt.subplot(2,2,2)
        self.plot(ax=ax, xy=(2,1))
        ax = plt.subplot(2,2,3)
        self.plot(ax=ax, xy=(0,2))
        ax = plt.subplot(2,2,4, projection='3d')
        self.plot3d(ax=ax)

        plt.tight_layout()   
