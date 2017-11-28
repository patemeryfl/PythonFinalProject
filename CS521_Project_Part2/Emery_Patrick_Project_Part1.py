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
        self.price = price
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
        records = []
        with open(self.csv_file, 'r') as csv_input_data:
            csv_reader = csv.DictReader(csv_input_data)
            for individual_row in csv_reader:
                try:
                    csv_record = self.row_to_record(individual_row)
                    records.append(csv_record)
                except BadDataError:
                    pass
        return records

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

            return BaseballStatRecord(
                csv_row['PLAYER'],
                int(csv_row['SALARY']),
                float(csv_row['AVG']),
                int(csv_row['G'])
            )
        except BadDataError:
            pass

class StocksCSVReader(AbstractCSVReader):
    '''Inherits Abstract Reader, initializes list of validated row items'''

    def row_to_record(self, csv_row):
        '''Calculates net income, market value and price/exchange ratio'''
        for column_name, row_value in csv_row.items():
            if not column_name or not row_value:
                raise BadDataError
        try:
            price = float(csv_row['price'])
            exchange_rate = float(csv_row['exchange_rate'])
            shares_outstanding = float(csv_row['shares_outstanding'])
            net_income = float(csv_row['net_income'])
            market_value_usd = price * exchange_rate * shares_outstanding
            if net_income > 0:
                pe_ratio = price / net_income
            else:
                pe_ratio = 0
            return StockStatRecord(
                csv_row['ticker'],
                csv_row['exchange_country'],
                csv_row['company_name'],
                price,
                exchange_rate,
                shares_outstanding,
                net_income,
                market_value_usd,
                pe_ratio
            )
        except ValueError:
            raise BadDataError
        except BadDataError:
            pass

if __name__ == "__main__":
    BASEBALL_RECORDS = BaseballCSVReader(BASEBALL_CSV).load()
    STOCK_RECORDS = StocksCSVReader(STOCK_CSV).load()

    for record in BASEBALL_RECORDS:
        print(record)

    for record in STOCK_RECORDS:
        print(record)
