import sqlite3
import collections
import create_dbs

from Emery_Patrick_Projec_Part1 import BaseballCSVReader, StocksCSVReader

BASEBALL_CSV = 'MLB2008.csv'
STOCK_CSV = 'StockValuations.csv'

class AbstractDAO:
    '''Info'''
    def __init__(self, db_name):
        self.db_name = db_name

    def insert_records(self, records):
        '''Info'''
        raise NotImplementedError

    def select_all(self):
        '''Info'''
        raise NotImplementedError

    def connect(self):
        '''Info'''
        with sqlite3.connect(self.db_name) as sql_connection:
            return sql_connection

class BaseballStatsDAO(AbstractDAO):
    '''Info'''
    def insert_records(self, records):
        '''takes list of records as parameter'''
        sql_connection = self.connect()
        for baseball_row in records:
            player_name = baseball_row.get('PLAYER', 0)
            player_salary = baseball_row.get('SALARY', 0)
            games_played = baseball_row.get('G', 0)
            game_average = baseball_row.get('AVG', 0)

            baseball_cursor = sql_connection.cursor()
            baseball_cursor.execute("INSERT INTO baseball_stats VALUES (?,?,?,?)",
                                    (player_name, games_played, game_average, player_salary))
        sql_connection.commit()

    def select_all(self):
        '''Info'''
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
    '''Info'''
    def insert_records(self, records):
        '''takes list of records as parameter'''
        sql_connection = self.connect()
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

            stocks_cursor = sql_connection.cursor()
            stocks_cursor.execute("INSERT INTO stock_stats VALUES (?,?,?,?,?,?,?,?,?)",
                                  (company_name, ticker, exchange_country, price,
                                   exchange_rate, shares_outstanding, net_income,
                                   market_value_usd, pe_ratio))
        sql_connection.commit()

    def select_all(self):
        '''Info'''
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
    create_dbs.create_dbs()

    BASEBALL_RECORDS = BaseballCSVReader(BASEBALL_CSV).load()
    BaseballStatsDAO('baseball.db').insert_records(BASEBALL_RECORDS)

    STOCK_RECORDS = StocksCSVReader(STOCK_CSV).load()
    StockStatsDAO('stocks.db').insert_records(STOCK_RECORDS)

    BASEBALL_DEQUE = BaseballStatsDAO('baseball.db').select_all()
    STOCKS_DEQUE = StockStatsDAO('stocks.db').select_all()



