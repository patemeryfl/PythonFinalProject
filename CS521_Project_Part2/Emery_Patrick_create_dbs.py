import sqlite3

def create_dbs():
    with sqlite3.connect('baseball.db') as baseball_connection:
        db_cursor = baseball_connection.cursor()

        db_cursor.execute('''CREATE TABLE 'baseball_stats' (
                            player_name  text,
                            games_played int,
                            average      real,
                            salary       real)''')

    with sqlite3.connect('stocks.db') as stocks_connection:
        db_cursor = stocks_connection.cursor()

        db_cursor.execute('''CREATE TABLE 'stock_stats' (
                            company_name       text,
                            ticker             text,
                            exchange_country   text,
                            price              real,
                            exchange_rate      real,
                            shares_outstanding real,
                            net_income         real,
                            market_value       real,
                            pe_ratio           real)''')
