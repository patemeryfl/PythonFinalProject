import csv

'''Project Part 1
   Patrick Emery'''

BASEBALL_CSV = 'MLB2008.csv'
STOCK_CSV = 'StockValuations.csv'

BASEBALL_COLUMNS = ('PLAYER', 'SALARY', 'G', 'AVG')

class BadDataError(Exception):
    '''Custom error exception'''
    pass

class AbstractRecord:
    '''Abtract Record Class'''
    def __init__(self, name):
        self.name = name

class BaseballStatRecord(AbstractRecord):
    '''Baseball Class, inherits abtract record class, overrides str'''
    def __init__(self, name, salary, games, average):
        super().__init__(name)
        self.salary = salary
        self.games = games
        self.average = float(average)

    def __str__(self):
        return "BaseballStatRecord({0}, {1}, {2}, {3:.3f})".format(self.name, self.salary, self.games, self.average)

class StockStatRecord(AbstractRecord):
    '''Stocks Class, inherits abtract record class, overrides str'''
    def __init__(self, name, exchange_country, company_name, price, exchange_rate, \
                 shares_outstanding, net_income, market_value_usd, pe_ratio):
        super().__init__(name)
        self.exchange_country = exchange_country
        self.company_name = company_name
        self.price = price
        self.exchange_rate = exchange_rate
        self.shares_outstanding = shares_outstanding
        self.net_income = float(net_income)
        self.market_value_usd = market_value_usd
        self.pe_ratio = pe_ratio

    def __str__(self):
        return "StockStatRecord({0}, {1}, $price={2:.2f}, $Cap={3:.2f}, P/E={4:.2f})".format(\
            self.name, self.company_name, self.net_income, self.market_value_usd, self.pe_ratio)

class AbstractCSVReader:
    '''Abstract CSV Reader'''
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def row_to_record(self, csv_row):
        '''Method Docstring'''
        raise NotImplementedError
    
    def load(self):
        '''Method Docstring'''
        with open(self.csv_file, 'r') as csv_input_data:
            reader = csv.DictReader(csv_input_data)
            for row in reader:
                valid_data = self.row_to_record(row)
        return valid_data

class BaseballCSVReader(AbstractCSVReader):
    '''Class Docstring'''
    valid_row_items = []

    def row_to_record(self, csv_row):
        '''Loop through rows, check if any rows are empty,
           format decimals, etc'''
        try:
            for column_name, row_value in csv_row.items():
                if not column_name or not row_value:
                    raise BadDataError
            self.valid_row_items.append(csv_row)
        except BadDataError:
            print('BadDataError in Baseball')
        return self.valid_row_items

class StocksCSVReader(AbstractCSVReader):
    '''Class Docstring'''
    valid_row_items = []

    def row_to_record(self, csv_row):
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
                            pe_ratio = 0
                        else:
                            pe_ratio = price / net_income
                    except ValueError:
                        continue
            csv_row.update({'market_value_usd':market_value_usd})
            csv_row.update({'pe_ratio':pe_ratio})
            self.valid_row_items.append(csv_row)         
        except BadDataError:
                pass
        return self.valid_row_items

if __name__ == "__main__":
    BASEBALL_DATA = BaseballCSVReader(BASEBALL_CSV).load()
    STOCK_DATA = StocksCSVReader(STOCK_CSV).load()

    for valid_rows in BASEBALL_DATA:
        player_name = valid_rows.get('PLAYER', 0)
        player_salary = valid_rows.get('SALARY', 0)
        games_played = valid_rows.get('G', 0)
        game_average = valid_rows.get('AVG', 0)
        record = BaseballStatRecord(player_name, player_salary, games_played, game_average)
        print(record)
        print_baseball = []

    for valid_rows in STOCK_DATA:
        valid_ticker = valid_rows.get('ticker', 0)
        valid_exchange_country = valid_rows.get('exchange_country', 0)
        valid_company_name = valid_rows.get('company_name', 0)
        valid_price = valid_rows.get('price', 0)
        valid_exchange_rate = valid_rows.get('exchange_rate', 0)
        valid_shares_outstanding = valid_rows.get('shares_outstanding', 0)
        valid_net_income = valid_rows.get('net_income', 0)
        valid_market_value_usd = valid_rows.get('market_value_usd', 0)
        valid_pe_ratio = valid_rows.get('pe_ratio', 0)

        record = StockStatRecord(valid_ticker, valid_exchange_country, valid_company_name, valid_price, valid_exchange_rate, \
                                 valid_shares_outstanding, valid_net_income, valid_market_value_usd, valid_pe_ratio)
        print(record)