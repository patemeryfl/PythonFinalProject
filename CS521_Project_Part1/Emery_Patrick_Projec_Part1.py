import csv

'''Project Part 1
   Patrick Emery'''

BASEBALL_CSV = 'MLB2008.csv'
STOCK_CSV = 'StockValuations.csv'

class BadDataError(Exception):
    '''Custom error exception'''
    pass

class AbstractRecord:
    '''Abtract Record Class'''
    def __init__(self, name):
        self.name = name

class BaseballStatRecord(AbstractRecord):
    '''Baseball Class, Inherits abtract record class,
       Requires player name, salary, games, and average
       Overrides __str__ method to print out passed in values'''
    def __init__(self, name, salary, games, average):
        super().__init__(name)
        self.salary = salary
        self.games = games
        self.average = float(average)

    def __str__(self):
        return "BaseballStatRecord({0}, {1}, {2}, {3:.3f})".format(\
            self.name, self.salary, self.games, self.average)

class StockStatRecord(AbstractRecord):
    '''Baseball Class, Inherits abtract record class,
       Requires ticker number, country, company, price, exchange rate and shares
       Overrides __str__ method to print out passed in values'''
    def __init__(self, name, exchange_country, company_name, price, exchange_rate, \
                 shares_outstanding, net_income, market_value_usd, pe_ratio):
        super().__init__(name)
        self.exchange_country = exchange_country
        self.company_name = company_name
        self.price = float(price)
        self.exchange_rate = exchange_rate
        self.shares_outstanding = shares_outstanding
        self.net_income = net_income
        self.market_value_usd = market_value_usd
        self.pe_ratio = pe_ratio

    def __str__(self):
        return "StockStatRecord({0}, {1}, $price={2:.2f}, $Cap={3:.2f}, P/E={4:.2f})".format(\
            self.name, self.company_name, self.price, self.market_value_usd, self.pe_ratio)

class AbstractCSVReader:
    '''Abstract CSV Reader'''
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def row_to_record(self, csv_row):
        '''Method Docstring'''
        raise NotImplementedError

    def load(self):
        '''Takes in a csv file and uses with to open it
           Reads CSV into dictionary and passes each row in the
           csv file to the row_to_record method of the class that called it'''
        with open(self.csv_file, 'r') as csv_input_data:
            csv_reader = csv.DictReader(csv_input_data)
            for individual_row in csv_reader:
                csv_row_data = self.row_to_record(individual_row)
        return csv_row_data

class BaseballCSVReader(AbstractCSVReader):
    '''Class Docstring'''
    valid_baseball_rows = []

    def row_to_record(self, csv_row):
        '''Loop through rows, check if any rows are empty,
           format decimals, etc'''
        try:
            for column_name, row_value in csv_row.items():
                if not column_name or not row_value:
                    raise BadDataError
            self.valid_baseball_rows.append(csv_row)
        except BadDataError:
            raise BadDataError
        return self.valid_baseball_rows

class StocksCSVReader(AbstractCSVReader):
    '''Inherits Abstract Reader, initializes list of validated row items'''
    valid_stock_rows = []

    def row_to_record(self, csv_row):
        '''Calculates net income, market value and price/exchange ratio'''
        try:
            for column_name, row_value in csv_row.items():
                if not column_name or not row_value:
                    raise BadDataError
                else:
                    try:
                        price = float(csv_row.get('price', 0))
                        shares_outstanding = float(csv_row.get('shares_outstanding', 0))
                        exchange_rate = float(csv_row.get('exchange_rate', 0))
                        net_income = float(csv_row.get('net_income', 0))

                        market_value_usd = price * exchange_rate * shares_outstanding
                        if net_income == 0:
                            raise BadDataError
                        else:
                            pe_ratio = price / net_income
                    except ValueError:
                        raise BadDataError
            csv_row.update({'market_value_usd':market_value_usd})
            csv_row.update({'pe_ratio':pe_ratio})
            self.valid_stock_rows.append(csv_row)
        except BadDataError:
            pass
        return self.valid_stock_rows

if __name__ == "__main__":
    BASEBALL_DATA = BaseballCSVReader(BASEBALL_CSV).load()
    STOCK_DATA = StocksCSVReader(STOCK_CSV).load()

    for baseball_row in BASEBALL_DATA:
        player_name = baseball_row.get('PLAYER', 0)
        player_salary = baseball_row.get('SALARY', 0)
        games_played = baseball_row.get('G', 0)
        game_average = baseball_row.get('AVG', 0)
        record = BaseballStatRecord(player_name, player_salary, games_played, game_average)
        print(record)
        print_baseball = []

    for stock_row in STOCK_DATA:
        stock_ticker = stock_row.get('ticker', 0)
        stock_exchange_country = stock_row.get('exchange_country', 0)
        stock_company_name = stock_row.get('company_name', 0)
        stock_price = stock_row.get('price', 0)
        stock_exchange_rate = stock_row.get('exchange_rate', 0)
        stock_shares_outstanding = stock_row.get('shares_outstanding', 0)
        stock_net_income = stock_row.get('net_income', 0)
        stock_market_value_usd = stock_row.get('market_value_usd', 0)
        stock_pe_ratio = stock_row.get('pe_ratio', 0)

        record = StockStatRecord(stock_ticker, stock_exchange_country, stock_company_name,\
        stock_price, stock_exchange_rate, stock_shares_outstanding, stock_net_income,\
        stock_market_value_usd, stock_pe_ratio)
        print(record)
