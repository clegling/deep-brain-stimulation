"""This file describes diffusion MRI head data"""
from nibabel_dmri_handler import NibabelDMRIHandler
import pandas as pd
from grey_matter_box import GreyMatterBox
import math

class HeadDMRI(object):
    """The class represents DMRI data for head."""
    def __init__(self, dmri_file, fbvals, fbvecs, output_file):
        """Constructor
            dmri_file - filename of the DMRI data
            mesh_file - filename of the file to write mesh+conductivities data to
        """
        self.output_file = output_file
        self.__init_iso_conductivities()
        self.dmri_handler = NibabelDMRIHandler(dmri_file, fbvals, fbvecs)
        self.gm_label = -1
        self.gm_box = GreyMatterBox()
        self.xscale_coef = None
        self.yscale_coef = None
        self.zscale_coef = None

    def calculate_conductivities(self, vertices, gm_label):
        """Calculates anisotropy conductivities for nodes
            vertices - filename of the vertices of the mesh
            gm_label - grey matter label
        """
        self.gm_label = gm_label
        data = pd.read_csv(vertices, sep=' ', header=None)

        self.__calculate_gm_bounds(data)
        self.dmri_handler.handle() #counts evals and evecs
        shape = self.dmri_handler.get_shape()

        self.xscale_coef = (self.gm_box.get_max_x() - self.gm_box.get_min_x()) / shape[0]
        self.yscale_coef = (self.gm_box.get_max_y() - self.gm_box.get_min_y()) / shape[1]
        self.zscale_coef = (self.gm_box.get_max_z() - self.gm_box.get_min_z()) / shape[2]

        self.__calculate_conductivities(data)
        data.to_csv(self.output_file, sep=' ')

    def __calculate_conductivities(self, data):
        #for 3-dim conductivity
        data[4] = ""
        data[5] = ""
        data[6] = ""
        for i in range (0, len(data)):
            xvalue = data.get_value(i, 0)
            yvalue = data.get_value(i, 1)
            zvalue = data.get_value(i, 2)
            if self.gm_box.is_inside(xvalue, yvalue, zvalue):
                xvoxel, yvoxel, zvoxel = self.__get_voxel_for_point(xvalue, yvalue, zvalue)
                #FIXME
                is_white_matter = True
                self.__add_conductivity(data, i, \
                    self.__get_conductivity(is_white_matter, xvoxel, yvoxel, zvoxel))

    def __add_conductivity(self, data, i, conductivity):
        #FIXME tensor sholud be here
        data.set_value(i, 4, conductivity[0])
        data.set_value(i, 5, conductivity[1])
        data.set_value(i, 6, conductivity[2])

    def __calculate_gm_bounds(self, data):
        gm_nodes = []
        for i in range(0, len(data)):
            if data.iloc[i][3] == self.gm_label:
                gm_nodes.append(data.iloc[i]) #points
        self.gm_box.calculate_bounds(gm_nodes)

    def __get_voxel_for_point(self, xvalue, yvalue, zvalue):
        xvoxel = int((xvalue - self.gm_box.get_min_x()) / self.xscale_coef)
        yvoxel = int((yvalue - self.gm_box.get_min_y()) / self.yscale_coef)
        zvoxel = int((zvalue - self.gm_box.get_min_z()) / self.zscale_coef)
        return xvoxel, yvoxel, zvoxel

    def __get_conductivity(self, is_white_matter, xvoxel, yvoxel, zvoxel):
        eigen_value = self.dmri_handler.get_eigen_values()[xvoxel][yvoxel][zvoxel]
        denom = math.sqrt(eigen_value[0] * eigen_value[1] * eigen_value[2])
        if is_white_matter:
            return eigen_value * self.wm_iso_conductivity / denom;
        return eigen_value * self.gm_iso_conductivity / denom;

    def __init_iso_conductivities(self):
        #4-Cole-Cole values
        self.wm_iso_conductivity = 0.06
        self.gm_iso_conductivity = 0.10
        self.encapsulation_tissue = 0.14
        self.cerebrospinal_fluid = 2.00