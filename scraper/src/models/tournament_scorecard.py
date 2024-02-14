from pony.orm import *
from datetime import datetime

from .model import db
from .player import Player
from .tournament import Tournament

class TournamentScorecard(db.Entity):
    id = PrimaryKey(int)
    player = Required('Player')
    tournament = Required('Tournament')
    winnings = Optional(float)
    nonFinishingState = Optional(str)
    pointsAwarded = Optional(float)
    mbValue = Optional(float)
    mbPercentage = Optional(float)
    finishPosition = Optional(int)
    rankFrom = Optional(int)
    rankTo = Optional(int)
    strokesGainedRating = Optional(float)
    endowment = Optional(float)
    worldRanking = Optional(int)
    scores = Set('Score')

    def __init__(self, 
        id,
        player,
        tournament,
        winnings,
        nonFinishingState,
        pointsAwarded,
        mbValue,
        mbPercentage,
        finishPosition,
        rankFrom,
        rankTo,
        strokesGainedRating,
        endowment,
        worldRanking
    ):
        super().__init__(
            id = id,
            player = player,
            tournament = tournament,
            winnings = winnings,
            nonFinishingState = nonFinishingState,
            pointsAwarded = pointsAwarded,
            mbValue = mbValue,
            mbPercentage = mbPercentage,
            finishPosition = finishPosition,
            rankFrom = rankFrom,
            rankTo = rankTo,
            strokesGainedRating = strokesGainedRating,
            endowment = endowment,
            worldRanking = worldRanking,
        )


    @classmethod 
    def serialize(cls, data: dict, player: Player, tournament: Tournament):
        return cls(
            id = data['id'],
            player = player,
            tournament = tournament,
            winnings = data['winnings'],
            nonFinishingState = data['nonFinishingState'],
            pointsAwarded = data['pointsAwarded'],
            mbValue = data['mbValue'],
            mbPercentage = data['mbPercentage'],
            finishPosition = data['finishPosition'],
            rankFrom = data['rankFrom'],
            rankTo = data['rankTo'],
            strokesGainedRating = data['strokesGainedRating'],
            endowment = data['endowment'],
            worldRanking = data['worldRanking'],
        )

class Score(db.Entity):
    id = PrimaryKey(int, auto=True)
    round = Required(int)
    score = Required(int)
    scorecard = Required(TournamentScorecard)

    def __init__(self, round, score, scorecard):
        super().__init__(
            round = round,
            score = score,
            scorecard = scorecard
        )

