"""This file describes API to convert meshes into comsol format."""
from enum import Enum
import numpy as np

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
    def fix_mesh_orientability(mesh_from, mesh_to):
        """Fixes faces orientability for mesh and saves new mesh
            mesh_from - filename for the input mesh
            mesh_to - filename for output mesh
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
        read_from_file.readline() #read name
        ComsolConverter._parse_type(read_from_file, faces, MeshElements.faces)
        read_from_file.readline() #read name
        ComsolConverter._parse_type(read_from_file, tetras, MeshElements.elements)
        file_to_write = open(mesh_to, 'w')
        ComsolConverter.__fix_mesh_orientability(nodes, faces, tetras, file_to_write)
        file_to_write.close()
        read_from_file.close()

    @staticmethod
    def __fix_mesh_orientability(nodes, faces, elems, out):
        """Fix mesh orientability logic
            nodes - nodes of the mesh with labels
            faces - faces with labels
            tetras - tetras with labels
        """
        out.write("MeshVersionFormatted 1\n")
        out.write("Dimension 3\n")
        out.write("Vertices\n")
        out.write(str(len(nodes)) + "\n")
        for i in range(0, len(nodes)):
            out.write(str(nodes[i][0]) + ' ' + str(nodes[i][1]) + ' ' + \
                str(nodes[i][2]) + ' ' + str(nodes[i][3]) + '\n')
        max_z_points = ComsolConverter.__calculate_internal_points(nodes, faces)
        for i in range(0, len(max_z_points)):
            max_z_points[i][2] = max_z_points[i][2] - 0.05 #z-delta

        out.write("Triangles\n")
        out.write(str(len(faces)) + "\n")
        invalid_oriented = 0
        for i in range(0, len(faces)):
            p1_idx = faces[i][0] - 1
            p2_idx = faces[i][1] - 1
            p3_idx = faces[i][2] - 1
            label = faces[i][3] - 1
            #print "p1 = %d, p2=%d, p3=%d, label = %d" % (p1_idx, p2_idx, p3_idx, label,)
            if label == -1 or label >= len(max_z_points):
                #print label
                continue
            if ComsolConverter.__is_triangle_orient_invalid(nodes[p1_idx], \
                nodes[p2_idx], nodes[p3_idx], max_z_points[label]):
                out.write(str(faces[i][2]) + ' ' + str(faces[i][1]) + \
                    ' ' + str(faces[i][0]) + ' ' + str(faces[i][3]) + "\n")
                invalid_oriented = invalid_oriented + 1
            else:
                out.write(str(faces[i][0]) + ' ' + str(faces[i][1]) + \
                    ' ' + str(faces[i][2]) + ' ' + str(faces[i][3]) + "\n")
        print "Invalid orientation was found for %d faces" % invalid_oriented
        out.write("Tetrahedras\n")
        out.write(str(len(elems)) + "\n")
        for i in range(0, len(elems)):
            out.write(str(elems[i][0]) + ' ' + str(elems[i][1]) + \
            ' ' + str(elems[i][2]) + ' ' + str(elems[i][3]) + ' ' + str(elems[i][4]) + '\n')

    @staticmethod
    def __is_triangle_orient_invalid(point1, point2, point3, internal_point):
        """Checks if the triagle orientation is correct"""
        #calculate cross product of vectors p1p2 and p1p3
        a = [i - j for i, j in zip(point2[:-1], point1[:-1])]
        b = [i - j for i, j in zip(point3[:-1], point1[:-1])]
        normal = np.cross(np.asarray(a), np.asarray(b))
        direction_outside = [i - j for i, j in zip(point1[:-1], internal_point)]
        if np.dot(normal, np.asarray(direction_outside)) >= 0:
            return True
        return False

    @staticmethod
    def __calculate_internal_points(nodes, faces):
        #count number of surfaces - labels
        #if zero is a label it's an error
        print "Calculate internal points started!"
        max_label = -1
        #zero_labels_num = 0
        for i in range(0, len(faces)):
            if faces[i][3] > max_label:
                max_label = faces[i][3]
            #if nodes[i][3] == 0:
                #nodes[i][3] = 1
                #zero_labels_num = zero_labels_num + 1
        print "Max label is %d" % max_label
        #print "Zero labeled nodes: %d" % zero_labels_num

        max_z_points = []
        for i in range(0, max_label):
            max_z_points.append([-100000, -100000, -100000])

        for i in range(0, len(faces)):
            label = faces[i][3]
            if label == 0:
                continue
            if nodes[faces[i][0] - 1][2] > max_z_points[label - 1][2]:
                max_z_points[label - 1] = nodes[faces[i][0] - 1][:-1]
            if nodes[faces[i][1] - 1][2] > max_z_points[label - 1][2]:
                max_z_points[label - 1] = nodes[faces[i][1] - 1][:-1]
            if nodes[faces[i][2] - 1][2] > max_z_points[label - 1][2]:
                max_z_points[label - 1] = nodes[faces[i][2] - 1][:-1]
        print "Calculate internal points finished!"
        print max_z_points
        return max_z_points

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
        read_from_file.readline() 
        ComsolConverter._parse_type(read_from_file, faces, MeshElements.faces)
        read_from_file.readline() 
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


ComsolConverter.fix_mesh_orientability("C:\\Users\\Sophia\\Desktop\\DBS\\out.mesh", "C:\\Users\\Sophia\\Desktop\\DBS\\out_fixed.mesh")
ComsolConverter.save_mesh_to_mphtxt("C:\\Users\\Sophia\\Desktop\\DBS\\out_fixed.mesh", "C:\\Users\\Sophia\\Desktop\\DBS\\out_fixed_comsol.mphtxt")
