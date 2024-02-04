from pony.orm import *
from datetime import datetime
from pprint import pprint

from models.tournament import Tournament 
from .model import db


class Club(db.Entity):
  # clubID from json
  id = PrimaryKey(int)
  name = Required(str)
  city = Required(str)
  # stateAbbreviation from json
  state = Optional(str)
  country = Required(str)
  courses = Set('Course')
  tournaments = Set(Tournament)

  def __init__(self, dictionary: dict):
    super().__init__(
      id = int(dictionary['clubID']),
      name = dictionary['name'],
      city = dictionary['city'],
      state = dictionary['state'],
      country = dictionary['country']
    )



class Course(db.Entity):
  # courseID from json
  id = PrimaryKey(int)
  name = Required(str)
  frontNine = Optional(int)
  backNine = Optional(int)
  totalPar = Optional(int)
  totalYardage = Optional(int)
  holes = Set('Hole')
  club = Required(Club)

  def __init__(self, dictionary: dict, club: Club):
    super().__init__(
      id = int(dictionary['courseID']),
      name = dictionary['name'],
      frontNine = int(dictionary['frontNine']) if dictionary['frontNine'] else None,
      backNine = int(dictionary['backNine']) if dictionary['backNine'] else None,
      totalPar = int(dictionary['totalPar']) if dictionary['totalPar'] else None,
      totalYardage = int(dictionary['totalYardage']) if dictionary['totalYardage'] else None,
      club = club
    )


class Hole(db.Entity):
  id = PrimaryKey(int, auto=True)
  number = Required(int)
  par = Required(int)
  yardage = Required(int)
  course = Required('Course')

  def __init__(self, dictionary: dict, course: Course):
    super().__init__(
      number = int(dictionary['number']),
      par = int(dictionary['par']),
      yardage = int(dictionary['yardage']),
      course = course
    )

