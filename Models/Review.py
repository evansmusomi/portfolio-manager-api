""" Defines review structure """
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from .Model import Model


class Review(Model):
    """ Review blue print """

    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    reviewer_1 = Column(String(400))
    reviewer_2 = Column(String(400))
    review_date = Column(Date)
    content = Column(String(2000))

    # user reference
    candidate = Column(Integer, ForeignKey('candidates.id'))
