from lib2to3.pgen2.token import OP
from .model import db
from pony.orm import *
from .tournament import Tournament
from .player import Player


class Scorecard(db.Entity):
  id = PrimaryKey(int, auto=True)
  type = Optional(str)
  tournament = Required(Tournament)
  player = Required(Player)
  round = Required(int)
  out = Optional(int)
  # in from json
  inScore = Optional(int)
  total = Optional(int)
  startHole = Optional(int)
  holesPlayed = Optional(int)
  matchId = Optional(int)
  courseKey = Optional(int)
  position = Optional(int)
  scores = Set('Score')


  def __init__(self, dictionary: dict, tournament: Tournament, player: Player):
    super().__init__(
      type = dictionary['type'],
      tournament = tournament,
      player = player,
      round = int(dictionary['round']),
      out = int(dictionary['out']) if dictionary['out'] else None,
      inScore = int(dictionary['in']) if dictionary['in'] else None,
      total = int(dictionary['total']) if dictionary['total'] else None,
      startHole = int(dictionary['startHole']) if dictionary['startHole'] else None,
      holesPlayed = int(dictionary['holesPlayed']) if dictionary['holesPlayed'] else None,
      matchId = int(dictionary['matchId']) if dictionary['matchId'] else None,
      courseKey = int(dictionary['courseKey']) if dictionary['courseKey'] else None,
      position = int(dictionary['position']) if dictionary['position'] else None
    )


class Score(db.Entity):
  id = PrimaryKey(int, auto=True)
  hole = Required(int)
  holeOrder = Required(int)
  par = Required(int)
  score = Optional(int)
  yardage = Optional(int)
  scorecard = Required(Scorecard)

  def __init__(self, dictionary: dict, scorecard: Scorecard):
    super().__init__(
        hole = int(dictionary['hole']),
        holeOrder = int(dictionary['holeOrder']),
        par = int(dictionary['par']),
        score = int(dictionary['score']) if dictionary['score'] and any(i.isdigit() for i in dictionary['score']) else None,
        yardage = int(dictionary['yardage']) if dictionary['yardage'] else None,
        scorecard = scorecard
    )
