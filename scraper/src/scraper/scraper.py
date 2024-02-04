from datetime import datetime
import json
import urllib3
from models import Player, Course, Tournament, Club, Hole
from typing import List
from pony.orm import db_session, commit, count

from models.scorecard import Score, Scorecard

base_url = 'https://apiweb.owgr.com/api/owgr'

def scrape_years(years, tour_id):
    http = urllib3.PoolManager()

    players = get_players(tour_id, http)
    print("Got player data...")

    # for year in years:
    #     print(f'Starting to scrape for {year}...')
    #     tournaments = get_tournaments(year, tour_id, http)
    #     for tournament in tournaments:
    #         if tournament.startDate < datetime.now():
    #             with db_session:
    #                 scorecards_count = count(s for s in Scorecard if s.tournament.id == tournament.id)
    #                 if scorecards_count == 0:         
    #                     print(f'Getting data for {tournament.name}...')
    #                     get_tournament_data(tournament.id, http)
    #     print(f'Got all data for {year}...')

@db_session
def get_players(tour_id: int, http: urllib3.PoolManager):
    url = f'{base_url}/rankings/getRankings?pageSize=200'

    response = http.request("GET", url)

    players  = []
    if(response.status == 200 and response.data is not None):
        players_list = json.loads(response.data)
        for ranking in players_list['rankingsList']:
            player_dict = ranking['player']
            parse_player(player_dict)

    return players

@db_session
def parse_player(dictionary: dict):
    player = Player.get(id=dictionary['id'])
    
    if player is None:
        try:
            player = Player(dictionary)
            return player
        except ValueError:
            print(dictionary)
    

@db_session
def get_player(id: int, http: urllib3.PoolManager ):
    player = Player.get(id=id)
    if player is None:
        url = f'{base_url}/golfers/{id}'
        response = http.request("GET", url)
        if(response.status == 200 and response.data is not None):
            pjson = json.loads(response.data)
            if 'golfer' in pjson:
                player_data = pjson['golfer']
                player = parse_player(player_data)
    
    return player


def get_tournaments(year: int, tour_id: int, http: urllib3.PoolManager) -> List[Tournament]:
    url = f'{base_url}/tours/{tour_id}/events/{year}'

    response = http.request("GET", url)
    if(response.status == 200 and response.data is not None):
        tournaments_list = json.loads(response.data)
        tournaments = []
        for tournament_dictiontary in tournaments_list:
            with db_session:
                tournament = Tournament.get(id=tournament_dictiontary['key'])
                if tournament is None:
                    clubs = []
                    club_dicts = tournament_dictiontary['golfClubs']
                    for club_dict in club_dicts:
                        club = Club.get(id=club_dict['clubID'])
                        if not club:
                            club = Club(club_dict)
                        courses_dictionary = club_dict['courses']
                        for course_dictionary in courses_dictionary:
                            course = Course.get(id=course_dictionary['courseID'])
                            if not course:
                                course = Course(course_dictionary, club)
                                holes_dictionary = course_dictionary['holes']
                                for hole_dictionary in holes_dictionary:
                                    hole = Hole(hole_dictionary, course)
                        
                        clubs.append(club)
                    
                    tournament = Tournament(tournament_dictiontary)
                    tournament.clubs = clubs
                    commit()
            tournaments.append(tournament)
        return tournaments
    else:
        raise Exception(f'no data found for {year}')


def get_tournament_data(tournament_id: int, http: urllib3.PoolManager):
    url = f'{base_url}/events/{tournament_id}/scorecard'

    response = http.request("GET", url)
    if(response.status == 200 and response.data is not None):
        sjson = json.loads(response.data)
        if 'scorecards' in sjson:
            scorecards_list = sjson['scorecards']
            for scorecard_dictionary in scorecards_list:
                with db_session:
                    golfer_id = scorecard_dictionary['golferId']
                    player = get_player(golfer_id, http)
                    if not player:
                        print(f'missing {golfer_id}')
                    else:
                        tournament = Tournament[tournament_id]
                        scorecard = Scorecard(scorecard_dictionary, tournament, player)
                        scores_list = scorecard_dictionary['scores']
                        for score_dictionary in scores_list:
                            score = Score(score_dictionary, scorecard)




