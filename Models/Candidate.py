""" Defines candidate structure """

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from pyld import jsonld
from .Model import Model


class Candidate(Model):
    """ Candidate object blueprint """

    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    birthday = Column(Date, nullable=True)
    phone = Column(String(30), nullable=True)
    languages = Column(String(500), default="")
    skills = Column(String(1000), default="")
    interviews = relationship("Interview")
    reviews = relationship("Review")

    def serialize(self):
        """ Creates dictionary representation of object """

        compacted_json = jsonld.compact({
            "http://schema.org/first_name": self.first_name,
            "http://schema.org/last_name": self.last_name,
            "http://schema.org/id": self.id,
            "http://schema.org/email": self.email,
            "http://schema.org/birthDate": self.birthday.isoformat() if self.birthday else "",
            "http://schema.org/telephone": self.phone,
            "http://schema.org/languages": self.languages,
            "http://schema.org/number_of_reviews": len(self.reviews),
            "http://schema.org/number_of_interviews": len(self.interviews)
        }, self.get_context())

        return compacted_json

    def get_context(self):
        """ Defines context schema for the candidate object """

        return {
            "@context": {
                "first_name": "http://schema.org/first_name",
                "last_name": "http://schema.org/last_name",
                "email": "http://schema.org/email",
                "birthday": "http://schema.org/birthDate",
                "phone": "http://schema.org/telephone",
                "languages": "http://schema.org/languages",
                "skills": "http://schema.org/skills",
                "number_of_reviews": "http://schema.org/number_of_reviews",
                "number_of_interviews": "http://schema.org/number_of_interviews",
                "id": "http://schema.org/id"
            }
        }
