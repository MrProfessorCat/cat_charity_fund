from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import ABCBase


class Donation(ABCBase):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'))
