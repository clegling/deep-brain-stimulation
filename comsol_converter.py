"""This file describes API to convert meshes into comsol format."""
from enum import Enum

class MeshElements(Enum):
    """Mesh elements enumeration"""
    nodes = 1
    faces = 2
    elements = 3

class ComsolConverter(object):
    """The class represents API to create COMSOL files from ordinary meshes"""

    @staticmethod
    def _parse_type(file_obj, elems, mesh_element):
        """Parses types blocks from the mesh
            fileObj - file to read data from
            elems - container to put parsed elements to
        """
        line_read = file_obj.readline() # read elems num
        line_read = line_read [:-1] # remove last \n
        n_elems = int(line_read)
        for _ in range(0, n_elems):
            line_read = file_obj.readline()
            line_read = line_read[:-1]
            values = line_read.split(' ')
            elems.append(list())
            if mesh_element == MeshElements.nodes:
                elems[-1].append(float(values[0]))
                elems[-1].append(float(values[1]))
                elems[-1].append(float(values[2]))
            else:
                elems[-1].append(int(values[0]))
                elems[-1].append(int(values[1]))
                elems[-1].append(int(values[2]))
            elems[-1].append(int(values[3]))
            if mesh_element == MeshElements.elements:
                elems[-1].append(int(values[4]))

    @staticmethod
    def save_mesh_to_mphtxt(mesh_from, mesh_to):
        """Converts from .msh format to .mphtxt
            mesh_from - filename of the mesh to convert
            mesh_to - filename of the mesh to write to
        """
        if (mesh_from is None) or (mesh_to is None):
            return
        read_from_file = open(mesh_from, 'r')
        read_line = ''
        while read_line != 'Vertices\n':
            read_line = read_from_file.readline()
        nodes = []
        faces = []
        tetras = []
        ComsolConverter._parse_type(read_from_file, nodes, MeshElements.nodes)
        ComsolConverter._parse_type(read_from_file, faces, MeshElements.faces)
        ComsolConverter._parse_type(read_from_file, tetras, MeshElements.elements)
        file_to_write = open(mesh_to, 'w')
        ComsolConverter.__convert_mesh(nodes, faces, tetras, file_to_write)
        file_to_write.close()
        read_from_file.close()

    @staticmethod
    def __convert_mesh(nodes, faces, elems, out):
        """Creates COMSOL file from components
            nodes - nodes of the mesh: 3d-vector of floats
            faces - labeled triangles of the mesh
            elems - labeled tetrahedras of the mesh
            out - filename for output
        """
        out.write('#Created by the COMSOLTranslator\n')
        out.write('0 1\n1\n5 mesh1\n1\n3 obj\n\n')
        out.write('0 0 1\n4 Mesh\n4\n3\n'+str(len(nodes))+'\n1\n')
        #write nodes
        for i in range(0, len(nodes)):
            out.write(str(nodes[i][0]) + ' ' + str(nodes[i][1]) + ' ' + str(nodes[i][2]) + '\n')
        out.write('\n2\n\n3 tri\n')

        #write triangles
        out.write('\n3\n')
        out.write(str(len(faces))+'\n\n')
        for i in range(0, len(faces)):
            out.write(str(faces[i][0]) + ' ' + str(faces[i][1]) + ' ' + str(faces[i][2])+'\n')
        out.write('\n' + str(len(faces)) + '\n')
        for i in range(0, len(faces)):
            out.write(str(faces[i][3]) + '\n')
        #write tetrahedra info
        out.write('\n\n3 tet\n4\n\n' + str(len(elems)) + '\n')
        for i in range(0, len(elems)):
            out.write(str(elems[i][0]) + ' ' + str(elems[i][1]) + \
            ' ' + str(elems[i][2]) + ' ' + str(elems[i][3]) + '\n')
        out.write('\n' + str(len(elems)) + '\n')
        for i in range(0, len(elems)):
            out.write(str(elems[i][4]) + '\n')
