import pandas as pd
import sqlite3
from scraper import scrape_years
from models import connect_to_sqlite

def main():
    pga_tour_id = 23
    years = [2024, 2023, 2022, 2021, 2020]

    # setting this to True will cause scraper to rescrape all data (expensive)
    hard_refresh = False
    db_file_name = 'pga.sqlite'
    sql_debug = False 

    connect_to_sqlite(hard_refresh, db_file_name, sql_debug)
    scrape_years(years, pga_tour_id)

    # dump to csv
    db_file_path = f'data/{db_file_name}'
    conn = sqlite3.connect(db_file_path, isolation_level=None,
                        detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql(f"""
        SELECT 
            p.firstName as player_first_name,
            p.lastName as player_last_name,
            t.name as tournament_name,
            t.weekDate as tournament_week_date,
            t.worldRatingStrengthOfField as tournament_world_rating_strength_of_field,
            t.homeTourStrengthOfFieldPoints as tournament_home_tour_strength_of_field_points,
            t.fieldRating as tournament_field_rating,
            t.fieldSize as tournament_field_size,
            ts.*
        FROM TournamentScorecard ts
        JOIN Player p ON p.id = ts.player
        JOIN Tournament t ON t.id = ts.tournament
    """, conn)
    db_df.to_csv('data/csvs/database.csv', index=False)

    # do analysis here if desired
    

if __name__ == '__main__':
    main()