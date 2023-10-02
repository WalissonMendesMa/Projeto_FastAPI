from database import Base
from sqlalchemy import Column, Integer, String

from pydantic import BaseModel

class ToExpired(Base):
    """
    modelo ultilizado na tabela do banco de dados.
    """
    __tablename__ = 'toexpireds'

    id  = Column(Integer, primary_key=True, index=True)
    product_code = Column(String)
    name = Column(String)
    expired_in = Column(String)
    
