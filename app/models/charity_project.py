from sqlalchemy import Column, String, Text

from app.core.db import ABCBase


class CharityProject(ABCBase):
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
