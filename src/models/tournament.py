from pony.orm import *
from datetime import datetime

from .model import db

class Tournament(db.Entity):
  # event key (key) from json 
  id = PrimaryKey(int)

  name = Required(str)
  startDate = Required(datetime)
  endDate = Required(datetime)
  rounds = Required(int)

  major = Required(bool)
  qualifying = Required(bool)
  hasPlayOffs = Required(bool)
  hasRoundReport = Required(bool)

  cutLineScore = Optional(int)
  cutLinePosition = Optional(int)
  progEventKey = Optional(int)

  purse = Optional(int)
  currencyISO = Optional(str)
  defendingChampionKey = Optional(int)
  winnerKey = Optional(int)
  seriesKey = Optional(int)
  clubs = Set('Club')
  scorecards = Set('Scorecard')

  def __init__(self, dictionary: dict):
    progEventKey = int(dictionary['progEventKey']) if dictionary['progEventKey'] else None
    defendingChampionKey = int(dictionary['defendingChampionKey']) if dictionary['defendingChampionKey'] else None
    winnerKey = int(dictionary['winnerKey']) if dictionary['winnerKey'] else None
    seriesKey = int(dictionary['seriesKey']) if dictionary['seriesKey'] else None

    super().__init__(
      id = dictionary['key'],
      name = dictionary['name'],
      startDate = dictionary['startDate'],
      endDate = dictionary['endDate'],
      rounds = int(dictionary['rounds']),
      major = dictionary['major'],
      qualifying = dictionary['qualifying'],
      hasPlayOffs = dictionary['hasPlayOffs'],
      hasRoundReport = dictionary['hasRoundReport'],
      cutLineScore = int(dictionary['cutLineScore']) if dictionary['cutLineScore'] else None,
      cutLinePosition = int(dictionary['cutLinePosition']) if dictionary['cutLinePosition'] else None,
      progEventKey = progEventKey,
      purse = int(dictionary['purse']),
      currencyISO = dictionary['currencyISO'],
      defendingChampionKey = defendingChampionKey,
      winnerKey = winnerKey,
      seriesKey = seriesKey
    )
