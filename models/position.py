from db import db, BaseModel
from models.model_mixin import MixinModel


class PositionModel(BaseModel, MixinModel):
  __tablename__ = 'positions'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  latitude = db.Column(db.Float(precision=5))
  longitude = db.Column(db.Float(precision=5))
  # one to many with bidirectional relationship
  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
  car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
  car = db.relationship('CarModel', back_populates='positions')

  def json(self):
    position_json = {
        'longitude': self.longitude,
        'latitude': self.latitude,
        'date': self.date.isoformat(),
    }
    return (position_json)
