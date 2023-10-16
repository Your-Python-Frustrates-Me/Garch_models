import numpy as np
from arch import arch_model
import yfinance_loader as yl


class VaRCalculator:
    """
    TODO: Implement EWMA function
    """
    def __init__(self, calculation_date_1, start_date_1, horizon_1, tickers_1):
        """
        Params initiation
        :param calculation_date_1: date on which VaR is calculated
        :param start_date_1: date on which VaR starts learning
        :param horizon_1: horizon VaR calculation
        :param tickers_1: tickers on which VaR is calculated
        """
        self.calculation_date = calculation_date_1
        self.start_date = start_date_1
        self.horizon = horizon_1
        self.tickers = tickers_1
        self.returns_df = None

    def get_returns(self):
        """
        Calculating returns of stock
        :return: dataframe of returns based on Adj Close
        """
        np.random.seed(42)
        dataloader = yl.YahooFinanceDataLoader(tickers=self.tickers, start_date=self.start_date,
                                               end_date=self.calculation_date, interval='1d')
        dataloader.fetch_data()
        df_filled = dataloader.preprocess()
        self.returns_df = 100 * df_filled['Adj Close'].pct_change().dropna()

    def calculate_garch_var(self):
        """
        Calculating var based on garch on 5% confidence level
        :return: var list on horizon for each instrument
        """
        var_list = []
        for ticker in self.tickers:
            am = arch_model(self.returns_df[ticker], vol="GARCH", p=1, o=0, q=1, dist="normal")
            res = am.fit(disp="off")
            forecasts = res.forecast(reindex=False, horizon=self.horizon)
            cond_mean = forecasts.mean
            cond_var = forecasts.variance
            q = am.distribution.ppf(0.05)
            value_at_risk = -cond_mean.values - np.sqrt(cond_var).values * q
            var_list.append(value_at_risk)
        return var_list



