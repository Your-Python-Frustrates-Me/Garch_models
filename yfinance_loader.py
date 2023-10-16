import yfinance as yf


class YahooFinanceDataLoader:
    def __init__(self, tickers=None, start_date=None, end_date=None, interval=None):
        """
        Params initiation
        :param tickers: list of tickers, example: ['AAPL', 'MSFT']
        :param start_date: start date in format "yyyy-mm-dd"
        :param end_date: end date in format "yyyy-mm-dd"
        :param interval: param how
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data = None

    def get_input(self):
        """
        Keyboard input function
        """
        ticker_input = input("Input tickers, split with space: ")
        self.tickers = ticker_input.split()
        self.start_date = input("Input start date format yyyy-mm-dd: ")
        self.end_date = input("Input finish date format yyyy-mm-dd: ")
        self.interval = input("Input interval from 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo: ")

    def fetch_data(self):
        """
        Fetching data from yfinance
        :return: dataframe with tickers
        """
        valid_tickers = []
        for ticker in self.tickers:
            try:
                data = yf.Ticker(ticker)
                if len(data.history(start=self.start_date, end=self.end_date, interval=self.interval)) > 0:
                    valid_tickers.append(ticker)
            except Exception as e:
                print(f"Ticker {ticker} is unavailable, exception {e}")

        if valid_tickers:
            try:
                self.data = yf.download(valid_tickers, start=self.start_date, end=self.end_date, interval=self.interval)
                return self.data
            except Exception as e:
                print(f"Error while loading data, exception {e}")
                return None
        else:
            print("No data for dates/tickers")
            return None

    def preprocess(self):
        """
        preprocessing data from yfinance
        :return: dataframe without nans, interpolated
        """
        if self.data is None:
            raise ValueError("Dataframe is empty for preprocessing, fetch first")
        else:
            self.data = self.data.interpolate(method='linear')
            return self.data
