from werkzeug.security import safe_str_cmp
from models.user import UserModel
from models.model_mixin import MixinModel


def authenticate(username, password):
  user = UserModel.find_by_attribute(username=username)
  if user and safe_str_cmp(user.password, password):
    return user


def identity(payload):
  user_id = payload['identity']
  return UserModel.find_by_attribute(id=user_id)
