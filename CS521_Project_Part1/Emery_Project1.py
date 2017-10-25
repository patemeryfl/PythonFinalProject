'''Project Part 1
   Patrick Emery'''

'''Constants'''
BASEBALL_CSV = 'MLB2008.csv'
STOCK_CSV = 'StockValuations.csv'

class AbstractRecord:
    def __init__(self, name):
        self.name = name

class AbstractCSVReader:
    def __init__(self, path_to_csv):
        self.path_to_csv = path_to_csv
    
    def record_to_row(row):
        raise NotImplementedError
    
    def load():
        #Open csv file
        pass

class BaseballStatRecord(AbstractRecord):
    def __init__(self, name, salary, G, AVG):
        self.name = name
        self.salary = salary
        self.G = games
        self.AVG = average

    def __str__(self):
        return "{0} {1}{2}{3}{4}".format(self.name, self.salary, self.G, self.AVG)

    def record_to_row(row):
        pass
        #if error, raise BadDataError()

class StockStatrecord(AbstractRecord):
    def __init__(self, name, company_name, exchange_country, price, exchange_rate, shares_outstanding, net_income, market_value_usd, pe_ratio):
        self.name = name
        self.company_name = company_name
        self.exchange_country = exchange_country
        self.price = price
        self.exchange_rate = exchange_rate
        self.shares_outstanding = shares_outstanding
        self.net_income = net_income
        self.market_value_usd = market_value_usd
        self.pe_ratio = pe_ratio

    def __str__(self):
        return "{0}, {1}, $price={2}, $Cap={3}, {4}, P/E={5}".format(self.name, self.company_name, self.net_income, self.market_value_usd, self.pe_ratio)

    def record_to_row(row):
        pass

class BadDataError(Exception):
    pass