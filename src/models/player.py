
from .model import db
from pony.orm import *
from datetime import datetime


class Player(db.Entity):
  # golferId in tour json, key in direct jjson
  id = PrimaryKey(int)
  firstName = Required(str)
  lastName = Required(str)
  # representsCountryName in json
  represents = Optional(str)
  proDate = Optional(datetime)
  age = Optional(int)
  scorecards = Set('Scorecard')


  def __init__(self, dictionary: dict):
    super().__init__(
      id = int(dictionary['golferId']) if 'golferId' in dictionary else int(dictionary['key']),
      firstName = dictionary['firstName'],
      lastName = dictionary['lastName'],
      represents = dictionary['representsCountryName'],
      proDate = dictionary['proDate'],
      age = int(dictionary['age']) if dictionary['age'] and any(i.isdigit() for i in dictionary['age']) else None
    )