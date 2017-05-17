""" Defines project structure """

import uuid


class Project(object):
    """ Project blueprint """

    def __init__(self, name, start_date, end_date, description):
        """ Initializes attributes """

        self.id = uuid.uuid4()
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

    def serialize(self):
        """ Creates dictionary representation of object """

        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
