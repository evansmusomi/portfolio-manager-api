""" Defines position structure """

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from .Model import Model


class Position(Model):
    """ Position blue print """

    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(200))
    description = Column(String(1000))
    tech_skills = Column(String(800))
    years_of_experience = Column(Integer)
    salary = Column(Integer)
    interviews = relationship("Interview")

    # client reference
    client = Column(Integer, ForeignKey('clients.id'))

    # recruiter reference
    recruiter = Column(Integer, ForeignKey('recruiters.id'))
