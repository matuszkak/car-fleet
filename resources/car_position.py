from flask_restful import Resource, reqparse
from models.car import CarModel
from models.position import PositionModel
from models.model_mixin import MixinModel
from sqlalchemy.sql.functions import now


class CarPosition(Resource):

  parser = reqparse.RequestParser()
  parser.add_argument('latitude',
                      type=float,
                      required=True,
                      help='Field can not be blank and should be float!')
  parser.add_argument('longitude',
                      type=float,
                      required=True,
                      help='Field can not be blank and should be float!')

  def post(self, plate):

    car = CarModel.find_by_attribute(license_plate=plate)
    if not car:
      return {"message": "Car with this licence plate does not exist"}, 404

    data = CarPosition.parser.parse_args()

    car_position = PositionModel(date=now(),
                                 latitude=data['latitude'],
                                 longitude=data['longitude'],
                                 car_id=car.id)

    try:
      car_position.save_to_db()
    except Exception:
      return {'message': 'error during database communication...'}, 400
    return {'message': f'Position saved for { plate }'}, 201

  def get(self, plate):
    car = CarModel.find_by_attribute(license_plate=plate)

    if car:
      positions = PositionModel.query.filter(PositionModel.car_id == car.id)
      return {"positions": [position.json() for position in positions]}
    return {'message': 'car not found'}, 404
