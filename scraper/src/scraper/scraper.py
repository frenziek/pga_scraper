from datetime import datetime
import json
import urllib3
from models import Player, Tournament, TournamentScorecard, Score
from typing import List
from pony.orm import db_session, commit

base_url = 'https://apiweb.owgr.com/api/owgr'

def scrape_years(years, tour_id):
    http = urllib3.PoolManager()

    players = get_players(tour_id, http)
    print(f"Got player data for {len(players)} players...")

    for year in years:
        print(f'Starting to scrape for {year}...')
        with db_session:
            tournaments = get_tournaments(year, tour_id, http)
            for tournament in tournaments:
                if tournament is not None and tournament.weekDate < datetime.now():
                        scorecards_exist = TournamentScorecard.exists(tournament=tournament)
                        if not scorecards_exist:
                            print(f'Getting data for {tournament.name}...')
                            get_tournament_data(tournament, http)
        print(f'Got all data for {year}...')

@db_session
def get_players(tour_id: int, http: urllib3.PoolManager):
    pages = [1, 2, 3]
    for page in pages:
        url = f'{base_url}/rankings/getRankings?regionId=0&pageSize=100&pageNumber={page}'

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
            player = Player.serialize(dictionary)
            return player
        except ValueError:
            print(dictionary)

def get_tournaments(year: int, tour_id: int, http: urllib3.PoolManager) -> List[Tournament]:
    url = f'{base_url}/events/getEventsToDate?year={year}&tourId={tour_id}'

    response = http.request("GET", url)
    if(response.status == 200 and response.data is not None):
        tournaments_list = json.loads(response.data)['eventsList']
        tournaments = []
        for tournament_dictiontary in tournaments_list:
            with db_session:
                tournament = Tournament.get(id=tournament_dictiontary['id'])
                if tournament is None:                    
                    tournament = Tournament.serialize(tournament_dictiontary)
                    commit()
            tournaments.append(tournament)
        return tournaments
    else:
        raise Exception(f'no data found for {year}')


def get_tournament_data(tournament: Tournament, http: urllib3.PoolManager):
    next_js_key = 'Pan6gJtCRBmjijMiqzAOK'
    different_base_url = f'https://www.owgr.com/_next/data/{next_js_key}'
    slug = f"{tournament.name.lower().replace(' ', '-')}-{tournament.id}"
    url = f'{different_base_url}/events/{slug}.json?slug={slug}'

    response = http.request("GET", url)
        
    if(response.status == 200 and response.data is not None):
        page_props = json.loads(response.data)['pageProps']
        if 'eventDetailsData' in page_props:
            event_result_list = page_props['eventDetailsData']['eventDetails']
            for scorecard_dictionary in event_result_list['results']:
                with db_session:
                    golfer_id = scorecard_dictionary['playerId']
                    player = Player.get(id=golfer_id)
                    if not player:
                        player = parse_player(scorecard_dictionary['player'])
                    else:
                        scorecard = TournamentScorecard.serialize(
                            scorecard_dictionary,
                            player,
                            tournament
                        )
                        scores_list = scorecard_dictionary['resultScores']
                        for score_dictionary in scores_list:
                            score = Score(
                                round=score_dictionary['roundNumber'], 
                                score=score_dictionary['score'], 
                                scorecard=scorecard
                            )




