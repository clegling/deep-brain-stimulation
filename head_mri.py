"""This file describes MRI data of the head"""
class HeadMRI(object):
    """Represents head MRI data. Makes all preprocessing for mesh building."""
    def __init__(self, filename, file_for_mesh):
        """Constructor
        filename - name of the file with MRI data, given in .nii format
        file_for_mesh - name of the file to create mesh in
        """
        self.mri_file = filename
        self.mesh_file = file_for_mesh

    def prepare_data(self, resolution):
        """Preprocesses MRI data to set the voxel resolution to the given resolution, if needed
            resolution - the resolution of the voxel needed
        """
        pass

    def insert_lead(self, lead):
        """Inserts dbs lead to the head mri and creates new label for the lead"""
        pass

    def build_mesh(self, resolution):
        """Builds mesh from MRI
            resolution - the resolution of the mesh
        """
        pass
        #mesh_builder.create_mesh()

    def get_mesh(self):
        """Returns mesh file builded earlier"""
        return self.mesh_file
