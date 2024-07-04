from enum import Enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class InteractionType(str, Enum):
    INPUT = 'input'
    OUTPUT = 'output'


class AlertType(str, Enum):
    THRESHOLD = 'threshold'
    OUTLIER = 'outlier'


class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    input_text = Column(String, nullable=False)
    output_text = Column(String, nullable=False)
    metrics = relationship('Metric', back_populates='interaction')
    alerts = relationship('Alert', back_populates='interaction')


class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    interaction_id = Column(Integer, ForeignKey('interactions.id'), nullable=False)
    metric_name = Column(String, nullable=False)
    input_metric_value = Column(Float, nullable=False)
    output_metric_value = Column(Float, nullable=False)
    interaction = relationship('Interaction', back_populates='metrics')


class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    interaction_id = Column(Integer, ForeignKey('interactions.id'), nullable=False)
    alert_type = Column(String, nullable=False)
    element = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    interaction = relationship('Interaction', back_populates='alerts')


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
