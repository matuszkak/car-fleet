from db import db, BaseModel
from models.model_mixin import MixinModel
import requests, json
from urllib.parse import urlparse


class PositionModel(BaseModel, MixinModel):
  __tablename__ = 'positions'

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime)
  latitude = db.Column(db.Float(precision=5))
  longitude = db.Column(db.Float(precision=5))
  address = db.Column(db.String)
  # one to many with bidirectional relationship
  # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
  car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
  car = db.relationship('CarModel', back_populates='positions')

  def json(self):
    position_json = {
        'longitude': self.longitude,
        'latitude': self.latitude,
        'address': self.address,
        'date': self.date.isoformat(),
    }
    return (position_json)

  def resolve_address(latitude, longitude):

    old = urlparse(
        "https://nominatim.openstreetmap.org/reverse?format=json&lat=47.4979&lon=19.0402"
    )
    new = "format=json&lat=" + str(latitude) + "&lon=" + str(longitude)
    # print(old)
    # print(new)

    try:
      cim = old._replace(query=new).geturl()
      # print(cim)
      url = requests.get(cim)
      text = url.text
      data = json.loads(text)
      # print(data)
      return (data['display_name'])
    except:
      return ("")
