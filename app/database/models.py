from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class GenerationMix(Base):
    __tablename__ = "generation_mix"
    # follows energy industry standard, measurements recorded end of ISP
    # timestamp represents end of that ISP when measurement recorded starting 
    # from timestamp - interval 
    idx = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Integer, primary_key=False, index=False)
    interval = Column(Integer, primary_key=False, index=False)
    fuel = Column(String, primary_key=False, index=False)
    percentage = Column(Float, primary_key=False, index=False)
