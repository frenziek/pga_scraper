
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
  scorecards = Set('TournamentScorecard')


  def __init__(self, id, firstName, lastName, represents, birthDate):
    super().__init__(
      id = id,
      firstName = firstName,
      lastName = lastName,
      represents = represents,
      birthDate = birthDate
    )

  @classmethod
  def serialize(cls, data: dict):
    cls(
      id = int(data['id']),
      firstName = data['firstName'],
      lastName = data['lastName'],
      represents = data['country']['name'],
      birthDate = data['birthDate']
    )