"""This file describes diffusion MRI head data"""
class HeadDMRI(object):
    """The class represents DMRI data for head."""
    def __init__(self, dmri_file, output_mesh):
        """Constructor
            dmri_file - filename of the DMRI data
            mesh_file - filename of the file to write mesh+conductivities data to
        """
        self.dmri_file = dmri_file
        self.output_mesh = output_mesh

    def calculate_conductivities(self, is_anisotropic, mesh):
        """Calculates anisotropy conductivities for nodes
            is_anisotropic - if conductivities should be anisotropic
            mesh - filename of the mesh created from head with lead inserted.
        """
        #output_mesh = calculate_from(mesh)
        pass

    
