import sqlite3

'''Pat Emery
    Project Part 2: Create Database Tables to hold records'''

def create_dbs():
    '''Open SQL Connection, create tables if they do not exist'''
    with sqlite3.connect('baseball.db') as baseball_connection:
        db_cursor = baseball_connection.cursor()

        db_cursor.execute('''CREATE TABLE IF NOT EXISTS 'baseball_stats' (
                            player_name  text,
                            games_played int,
                            average      real,
                            salary       real)''')

    with sqlite3.connect('stocks.db') as stocks_connection:
        db_cursor = stocks_connection.cursor()

        db_cursor.execute('''CREATE TABLE IF NOT EXISTS 'stock_stats' (
                            company_name       text,
                            ticker             text,
                            exchange_country   text,
                            price              real,
                            exchange_rate      real,
                            shares_outstanding real,
                            net_income         real,
                            market_value       real,
                            pe_ratio           real)''')
