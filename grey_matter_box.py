"""This file describes gm box"""
class GreyMatterBox(object):
    """The class represents grey matter box for overlaying dti and mri data"""
    def __init__(self):
        """Constructor
            gm_nodes - list of gm nodes
        """
        value = 100000
        self.min_x = value
        self.min_y = value
        self.min_z = value

        self.max_x = -value
        self.max_y = -value
        self.max_z = -value

    def __update_min(self, xvalue, yvalue, zvalue):
        if xvalue < self.min_x:
            self.min_x = xvalue
        if yvalue < self.min_y:
            self.min_y = yvalue
        if zvalue < self.min_z:
            self.min_z = zvalue

    def __update_max(self, xvalue, yvalue, zvalue):
        if xvalue > self.max_x:
            self.max_x = xvalue
        if yvalue > self.max_y:
            self.max_y = yvalue
        if zvalue > self.max_z:
            self.max_z = zvalue

    def __find_bounds(self, gm_nodes):
        for node in gm_nodes:
            self.__update_min(node[0], node[1], node[2])
            self.__update_max(node[0], node[1], node[2])

    def calculate_bounds(self, gm_nodes):
        """Calculates the bounds of the gm nodes"""
        self.__find_bounds(gm_nodes)

    def is_inside(self, xvalue, yvalue, zvalue):
        """Checks if the point is inside the grey matter box
            x - x-coordinate
            y - y-coordinate
            z - z-coordinate
        """
        if (xvalue <= self.max_x) and (xvalue >= self.min_x) and (yvalue <= self.max_y) \
            and (yvalue >= self.min_y) and (zvalue <= self.max_z) and (zvalue >= self.min_z):
            return True
        return False

    def get_min_x(self):
        """Returns min x"""
        return self.min_x

    def get_max_x(self):
        """Returns max x"""
        return self.max_x

    def get_min_y(self):
        """Returns min y"""
        return self.min_y

    def get_max_y(self):
        """Returns max y"""
        return self.max_y

    def get_min_z(self):
        """Returns min z"""
        return self.min_z

    def get_max_z(self):
        """Returns max z"""
        return self.max_z
