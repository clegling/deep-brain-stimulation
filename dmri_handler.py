"""This file represents dmri handling"""
from abc import ABCMeta, abstractmethod

class DMRIHandler:
    """This class is an abstract class for dti manipulations"""
    __metaclass__ = ABCMeta
    def __init__(self, dmri_file, fbvals, fbvecs):
        self.dmri_file = dmri_file
        self.fbvals = fbvals
        self.fbvecs = fbvecs

    @abstractmethod
    def get_shape(self):
        """Returns number of voxels for each dmri dimension"""

    @abstractmethod
    def handle(self):
        """Abstract method which includes all processing and calculations"""
        pass

    @abstractmethod
    def get_eigen_vectors(self):
        """Abstract method which returns eigen vectors for each voxel of the DMRI"""
        pass

    @abstractmethod
    def get_eigen_values(self):
        """Abstract method which returns eigen values for each voxel of the DMRI"""
        pass
