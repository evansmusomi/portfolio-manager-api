""" Defines recruiter structure """
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from .Model import Model


class Recruiter(Model):
    """ Recruiter blueprint """

    __tablename__ = 'recruiters'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    phone = Column(String(30))
    interviews = relationship("Interview")
    positions = relationship("Position")
