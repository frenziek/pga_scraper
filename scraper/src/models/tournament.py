from pony.orm import *
from datetime import datetime

from .model import db

class Tournament(db.Entity):
  id = PrimaryKey(int)
  name = Required(str)
  weekNumber = Required(int)
  weekDate = Required(datetime)
  weekId = Required(int)
  weekYear = Required(int)
  worldRatingStrengthOfField = Optional(float)
  homeTourStrengthOfFieldPoints = Optional(float)
  fieldRating = Optional(float)
  isCurtailed = Optional(bool)
  fieldSize = Optional(int)
  scheduledRoundsCount = Optional(int)
  isExcludedFromStrokesGainedCalculation = Optional(bool)
  isExcludedFromRanking = Optional(bool)
  cutSize = Optional(int)
  firstPlacePoints = Optional(float)
  totalStrengthOfFieldPoints = Optional(float)
  endDate = Optional(datetime)
  pointsPerPlayer = Optional(float)
  startDate = Optional(datetime)
  holes = Optional(int)
  scorecards = Set('TournamentScorecard')

  def __init__(self, 
      id,
      name,
      weekNumber,
      weekDate,
      weekId,
      weekYear,
      worldRatingStrengthOfField,
      homeTourStrengthOfFieldPoints,
      fieldRating,
      isCurtailed,
      fieldSize,
      scheduledRoundsCount,
      isExcludedFromStrokesGainedCalculation,
      isExcludedFromRanking,
      cutSize,
      firstPlacePoints,
      totalStrengthOfFieldPoints,
      endDate,
      pointsPerPlayer,
      startDate,
      holes
    ):
    super().__init__(
        id = id,
        name = name,
        weekNumber = weekNumber,
        weekDate = weekDate,
        weekId = weekId,
        weekYear = weekYear,
        worldRatingStrengthOfField = worldRatingStrengthOfField,
        homeTourStrengthOfFieldPoints = homeTourStrengthOfFieldPoints,
        fieldRating = fieldRating,
        isCurtailed = isCurtailed,
        fieldSize = fieldSize,
        scheduledRoundsCount = scheduledRoundsCount,
        isExcludedFromStrokesGainedCalculation = isExcludedFromStrokesGainedCalculation,
        isExcludedFromRanking = isExcludedFromRanking,
        cutSize = cutSize,
        firstPlacePoints = firstPlacePoints,
        totalStrengthOfFieldPoints = totalStrengthOfFieldPoints,
        endDate = endDate,
        pointsPerPlayer = pointsPerPlayer,
        startDate = startDate,
        holes = holes
      )

  @classmethod
  def serialize(cls, dict):
    cls(
      id = dict['id'],
      name = dict['name'],
      weekNumber = dict['weekNumber'],
      weekDate = dict['weekDate'],
      weekId = dict['weekId'],
      weekYear = dict['weekYear'],
      worldRatingStrengthOfField = dict['worldRatingStrengthOfField'],
      homeTourStrengthOfFieldPoints = dict['homeTourStrengthOfFieldPoints'],
      fieldRating = dict['fieldRating'],
      isCurtailed = dict['isCurtailed'],
      fieldSize = dict['fieldSize'],
      scheduledRoundsCount = dict['scheduledRoundsCount'],
      isExcludedFromStrokesGainedCalculation = dict['isExcludedFromStrokesGainedCalculation'],
      isExcludedFromRanking = dict['isExcludedFromRanking'],
      cutSize = dict['cutSize'],
      firstPlacePoints = dict['firstPlacePoints'],
      totalStrengthOfFieldPoints = dict['totalStrengthOfFieldPoints'],
      endDate = dict['endDate'],
      pointsPerPlayer = dict['pointsPerPlayer'],
      startDate = dict['startDate'],
      holes = dict['holes']
    )
          
