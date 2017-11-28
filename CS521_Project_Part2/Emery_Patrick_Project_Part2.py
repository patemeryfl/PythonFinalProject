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
    def __init__(self):
        super().__init__('baseball.db')

    def insert_records(self, records):
        '''Takes list of records as parameter, creates a cursor
           loops through dictionary of records and inserts them into the database'''
        sql_connection = self.connect()
        baseball_cursor = sql_connection.cursor()

        for baseball_row in records:
            player_name = baseball_row.name
            player_salary = baseball_row.salary
            games_played = baseball_row.games
            game_average = baseball_row.average

            baseball_cursor.execute("INSERT or ignore INTO baseball_stats VALUES (?,?,?,?)",
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
    def __init__(self):
        super().__init__('stocks.db')

    def insert_records(self, records):
        '''Takes list of records as parameter, creates a cursor
           loops through dictionary of records and inserts them into the database'''
        sql_connection = self.connect()
        stocks_cursor = sql_connection.cursor()

        for stock_row in records:
            company_name = stock_row.company_name
            stock_ticker = stock_row.name
            exchange_country = stock_row.exchange_country
            price = stock_row.price
            exchange_rate = stock_row.exchange_rate
            shares_outstanding = stock_row.shares_outstanding
            net_income = stock_row.net_income
            market_value_usd = stock_row.market_value_usd
            pe_ratio = stock_row.pe_ratio

            stocks_cursor.execute("INSERT or ignore INTO stock_stats VALUES (?,?,?,?,?,?,?,?,?)",
                                  (company_name, stock_ticker, exchange_country, price,
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
    #Create the database tables using create_db module
    Emery_Patrick_create_dbs.create_dbs()

    #Call the load method of the external CSV readers, pass returned record into insert statement
    BASEBALL_RECORDS = BaseballCSVReader(BASEBALL_CSV).load()
    BaseballStatsDAO().insert_records(BASEBALL_RECORDS)
    STOCK_RECORDS = StocksCSVReader(STOCK_CSV).load()
    StockStatsDAO().insert_records(STOCK_RECORDS)

    #Return a deque with all of the records returned by the select all method
    BASEBALL_DEQUE = BaseballStatsDAO().select_all()
    STOCKS_DEQUE = StockStatsDAO().select_all()

    #Create a default dictionary to maintain similar countries
    #Use length of matched values to determine number of tickers
    TICKERS_PER_EXCHANGE = collections.defaultdict(list)
    for stock_entries in STOCKS_DEQUE:
        tickers = stock_entries[1]
        exchange_countries = stock_entries[2]

        TICKERS_PER_EXCHANGE[exchange_countries].append(tickers)
    for country, ticker in TICKERS_PER_EXCHANGE.items():
        print('Country:', country, ' Total:', len(ticker))

    #Create a default dictionary to maintain similar salaries
    #Extract salary and avg and perform calculation, not repeating any salaries
    SALARY_PER_AVERAGE = collections.defaultdict(list)
    for baseball_entries in BASEBALL_DEQUE:
        batting_averages = baseball_entries[2]
        salaries = baseball_entries[3]

        SALARY_PER_AVERAGE[batting_averages].append(salaries)

    for average, salary in SALARY_PER_AVERAGE.items():
        average_salary = sum(salary) / len(salary)
        print('Average:', round(average, 3), 'Salary:', '${:,.2f}'.format(average_salary))
