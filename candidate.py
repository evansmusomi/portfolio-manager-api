""" Defines candidate structure """

import uuid


class Candidate(object):
    """ Candidate object blueprint """

    def __init__(self, first_name, last_name, experience=[]):
        """ Initializes candidate object """

        self.id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.experience = experience

    def serialize(self):
        """ Creates dictionary representation of object """

        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "id": self.id,
            "experience": [exp.serialize() for exp in self.experience]
        }

    def add_experience(self, experience):
        """ Adds experience to candidate """

        self.experience.append(experience)
