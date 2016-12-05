"""This file represents general dbs interface."""
class DBSLead(object):
    """Parent class for dbs leads.
    Each dbs lead is represented as a cylinder with the given diameter."""
    def __init__(self, diameter):
        """Constuctor
            diameter - the diameter of the lead
        """
        self.diam = diameter

    def set_diameter(self, diameter):
        """Sets dbs lead diameter"""
        self.diam = diameter

    def get_diameter(self):
        """Gets lead's diameter'"""
        return self.diam
