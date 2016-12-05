"""Stimulation lead's description file.'"""
from dbs_lead import DBSLead

class StimulationLead(DBSLead):
    """The class represents the cylindric lead with usual ring electrodes"""
    def __init__(self, diameter, num_contacts, contact_height, space_btwn_contacts):
        """ Constructor:
            diameter - diamter of the lead
            num_contacts - number of electrode on the lead
            contact_height - height of the electrode
            space_btwn_contacts - insulating space between electrodes
        """
        DBSLead.__init__(self, diameter)
        self.contact_height = contact_height
        self.space_btwn_contacts = space_btwn_contacts
        self.num_contacts = num_contacts

    def set_contact_height(self, contact_height):
        """Sets electrode's height for the lead'"""
        self.contact_height = contact_height

    def set_space_between_contacts(self, space):
        """Sets space between electrodes on the lead"""
        self.space_btwn_contacts = space

    def set_number_of_contacts(self, num_contacts):
        """Sets number of electrodes on the lead"""
        self.num_contacts = num_contacts

    def get_number_of_contacts(self):
        """Gets the number of contacts"""
        return self.num_contacts

    def get_contact_height(self):
        """Gets contact's height"""
        return self.contact_height

    def get_space_between_contacts(self):
        """Gets the space between contacts"""
        return self.space_btwn_contacts
