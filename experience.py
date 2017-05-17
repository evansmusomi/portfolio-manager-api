""" Defines experience structure """


class Experience(object):
    """ Experience blueprint """

    def __init__(self, domain, years, projects=[]):
        """ Initializes experience object """

        self.domain = domain
        self.years = years
        self.projects = projects

    def serialize(self):
        """ Creates dictionary representation of Experience object """

        return {
            "domain": self.domain,
            "years": self.years,
            "projects": [project.serialize() for project in self.projects]
        }
