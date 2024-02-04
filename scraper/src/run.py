import sys
from scraper import scrape_years
from models import connect_to_sqlite

def main():
    pga_tour_id = 1
    years = [2022, 2021, 2020, 2019, 2018, 2017]

    # setting this to True will cause scraper to rescrape all data (expensive)
    hard_refresh = False
    db_file_name = 'pga.sqlite'
    sql_debug = False 

    connect_to_sqlite(hard_refresh, db_file_name, sql_debug)
    scrape_years(years, pga_tour_id)

    # do analysis here if desired
    

if __name__ == '__main__':
    main()