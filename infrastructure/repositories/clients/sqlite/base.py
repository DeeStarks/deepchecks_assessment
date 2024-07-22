from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from infrastructure.repositories.clients.sqlite.models import Base
from infrastructure.repositories.clients.sqlite.models.alert import Alert
from infrastructure.repositories.clients.sqlite.models.interaction import Interaction
from infrastructure.repositories.clients.sqlite.models.metric import Metric

engine = create_engine(settings.database_url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)
