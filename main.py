""" Main module"""
from stimultation_lead import StimulationLead
from head_mri import HeadMRI
from head_dmri import HeadDMRI
from comsol_converter import ComsolConverter

def main(mri_name, dmri_name):
    """ Description here"""
    head_mri = HeadMRI(mri_name, "mesh.msh")
    head_mri.prepare_data(0.5) # resolution 0.5mm for voxels

    lead = StimulationLead(1.27, 4, 1.5, 1.5)
    head_mri.insert_lead(lead)
    head_mri.build_mesh(0.22) # resolution for mesh

    head_dmri = HeadDMRI(dmri_name, "bval", "bvec", "conductivities_nodes.msh")
    head_dmri.calculate_conductivities("vertices_file", 10)
    ComsolConverter.save_mesh_to_mphtxt(head_mri.get_mesh(), "head.mphtxt")

    print "Calculated!"

main("none", "none")
