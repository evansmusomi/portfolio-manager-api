""" Defines interview structure """

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from .Model import Model


class Interview(Model):
    """ Interview blue print """

    __tablename__ = 'interviews'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date = Column(Date)
    feedback = Column(String(2000))

    # position reference
    position = Column(Integer, ForeignKey('positions.id'))

    # recruiter reference
    recruiter_id = Column(Integer, ForeignKey('recruiters.id'))
    recruiter = relationship("Recruiter")

    # candidate reference
    candidate = Column(Integer, ForeignKey('candidates.id'))
