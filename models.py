from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime
import json
engine = create_engine('sqlite:///foo.db', echo=True)
Base = declarative_base()

class Demo(Base):
    __tablename__ = 'demo'

    id = Column(Integer, primary_key=True)
    val = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "<demo('%s','%s','%s')>" % (self.id, self.val, self.created_at)

    def todict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d

    def tojson(self):
        # o.__dict__ is not accessible...
        return json.dumps(self, default=lambda o: o.todict(), sort_keys=True)

metadata = Base.metadata

if __name__ == "__main__":
    metadata.create_all(engine)
