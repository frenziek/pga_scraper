
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
  birthDate = Optional(datetime)
  scorecards = Set('Scorecard')


  def __init__(self, id, firstName, lastName, represents, birthDate):
    self.id = id
    self.firstName = firstName
    self.lastName = lastName
    self.represents = represents
    self.birthDate = birthDate

  @classmethod
  def serialize(cls, data: dict):
    cls(
      id = int(data['id']),
      firstName = data['firstName'],
      lastName = data['lastName'],
      represents = data['country']['name'],
      birthDate = data['birthDate']
    )