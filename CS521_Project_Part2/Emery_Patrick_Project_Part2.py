import sqlite3
import collections
import Emery_Patrick_create_dbs

from Emery_Patrick_Project_Part1 import BaseballCSVReader, StocksCSVReader

BASEBALL_CSV = 'MLB2008.csv'
STOCK_CSV = 'StockValuations.csv'

class AbstractDAO:
    '''Abstract Class
    Parameters: Name of created database
    Methods: Insert records into database
             Select all and return into deque
             Connect to passed in db and return connection'''
    def __init__(self, db_name):
        self.db_name = db_name

    def insert_records(self, records):
        '''Takes in record from csv reader, inserts into db with sql'''
        raise NotImplementedError

    def select_all(self):
        '''Selects all records and insterts them into a deque'''
        raise NotImplementedError

    def connect(self):
        '''Returns SQL connection'''
        with sqlite3.connect(self.db_name) as sql_connection:
            return sql_connection

class BaseballStatsDAO(AbstractDAO):
    '''Inherits Abstract Class
       Defines insert and select methods'''
    def insert_records(self, records):
        '''Takes list of records as parameter, creates a cursor
           loops through dictionary of records and inserts them into the database'''
        sql_connection = self.connect()
        baseball_cursor = sql_connection.cursor()

        for baseball_row in records:
            player_name = baseball_row.get('PLAYER', 0)
            player_salary = baseball_row.get('SALARY', 0)
            games_played = baseball_row.get('G', 0)
            game_average = baseball_row.get('AVG', 0)

            baseball_cursor.execute("INSERT INTO baseball_stats VALUES (?,?,?,?)",
                                    (player_name, games_played, game_average, player_salary))
        sql_connection.commit()

    def select_all(self):
        '''Creates deque to hold returned records,
           executes select statement and adds returned values'''
        baseball_deque = collections.deque()
        sql_connection = self.connect()
        baseball_cursor = sql_connection.cursor()
        baseball_cursor.execute("\
                            SELECT player_name, games_played, average, salary \
                            FROM baseball_stats")
        returned_records = baseball_cursor.fetchall()
        for baseball_records in returned_records:
            baseball_deque.append(baseball_records)
        return baseball_deque


class StockStatsDAO(AbstractDAO):
    '''Inherits Abstract Class
       Defines insert and select methods'''
    def insert_records(self, records):
        '''Takes list of records as parameter, creates a cursor
           loops through dictionary of records and inserts them into the database'''
        sql_connection = self.connect()
        stocks_cursor = sql_connection.cursor()

        for stock_row in records:
            company_name = stock_row.get('company_name', 0)
            ticker = stock_row.get('ticker', 0)
            exchange_country = stock_row.get('exchange_country', 0)
            price = stock_row.get('price', 0)
            exchange_rate = stock_row.get('exchange_rate', 0)
            shares_outstanding = stock_row.get('shares_outstanding', 0)
            net_income = stock_row.get('net_income', 0)
            market_value_usd = stock_row.get('market_value_usd', 0)
            pe_ratio = stock_row.get('pe_ratio', 0)

            stocks_cursor.execute("INSERT INTO stock_stats VALUES (?,?,?,?,?,?,?,?,?)",
                                  (company_name, ticker, exchange_country, price,
                                   exchange_rate, shares_outstanding, net_income,
                                   market_value_usd, pe_ratio))
        sql_connection.commit()

    def select_all(self):
        '''Creates deque to hold returned records,
           executes select statement and adds returned values'''
        stocks_deque = collections.deque()
        sql_connection = self.connect()
        stocks_cursor = sql_connection.cursor()
        stocks_cursor.execute("SELECT company_name, ticker, exchange_country, price\
                               exchange_rate, shares_outstanding, net_income\
                               market_value_usd, pe_ratio FROM stock_stats")
        returned_records = stocks_cursor.fetchall()
        for stock_records in returned_records:
            stocks_deque.append(stock_records)
        return stocks_deque

if __name__ == '__main__':
    Emery_Patrick_create_dbs.create_dbs()

    BASEBALL_RECORDS = BaseballCSVReader(BASEBALL_CSV).load()
    BaseballStatsDAO('baseball.db').insert_records(BASEBALL_RECORDS)

    STOCK_RECORDS = StocksCSVReader(STOCK_CSV).load()
    StockStatsDAO('stocks.db').insert_records(STOCK_RECORDS)

    BASEBALL_DEQUE = BaseballStatsDAO('baseball.db').select_all()
    STOCKS_DEQUE = StockStatsDAO('stocks.db').select_all()

    TICKERS_PER_EXCHANGE = collections.defaultdict(list)
    for stock_entries in STOCKS_DEQUE:
        tickers = stock_entries[1]
        exchange_countries = stock_entries[2]

        TICKERS_PER_EXCHANGE[exchange_countries].append(tickers)
    for country, ticker in TICKERS_PER_EXCHANGE.items():
        print('Country:', country, ' Total:', len(ticker))

    SALARY_PER_AVERAGE = collections.defaultdict(list)
    for baseball_entries in BASEBALL_DEQUE:
        batting_averages = baseball_entries[2]
        salaries = baseball_entries[3]

        SALARY_PER_AVERAGE[batting_averages].append(salaries)

    for average, salary in SALARY_PER_AVERAGE.items():
        average_salary = sum(salary) / len(salary)
        print('Average:', round(average, 3), 'Salary:', '${:,.2f}'.format(average_salary))
