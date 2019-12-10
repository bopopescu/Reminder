from .dbConn import Base
import datetime
from .eventNotification import EventNotification, EventNotificationSchema
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Date, Time, Boolean, ForeignKey
from marshmallow import Schema, fields,EXCLUDE
from sqlalchemy.orm import relationship


class EventSchema(Schema):
    id = fields.Number()
    title = fields.Str()
    date = fields.DateTime()
    time = fields.String()
    id_calendar = fields.Number()
    color = fields.Str()





class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, nullable=True)
    title = Column(String)
    date = Column(DateTime)
    time = Column(String)
    id_calendar = Column(Integer)
    color = Column(String)
    
    reminders = relationship(EventNotification, backref="owner")


    def __init__(self, title, date, time, color, id_calendar, id=None):
        self.title = title
        self.time = time
        self.date = date
        self.id = id
        self.id_calendar = id_calendar
        self.color = color

