from sqlalchemy import Column, String, Text

from app.core.config import settings
from app.core.db import ABCBase


class CharityProject(ABCBase):
    name = Column(String(settings.name_max_length), nullable=False)
    description = Column(Text, nullable=False)
