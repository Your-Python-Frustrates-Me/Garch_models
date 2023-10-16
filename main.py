import yfinance_loader as YL
import VaR_calculator as VC


if __name__ == "__main__":
    option = int(input('Select option: print 1 if you want to load data else 2 if calculate var '))
    if option == 1:
        data_loader = YL.YahooFinanceDataLoader()
        data_loader.get_input()
        df_bare = data_loader.fetch_data()
        df_filled = data_loader.preprocess()

        if df_filled is not None:
            print(df_filled)
    else:
        calculation_date = "2023-10-15"
        start_date = "2023-10-01"
        horizon = 10
        tickers = ["AAPL", "MSFT"]

        var_calculator = VC.VaRCalculator(calculation_date, start_date, horizon, tickers)
        var_calculator.get_returns()
        var = var_calculator.calculate_garch_var()

        print(f"VaR at {horizon}-day horizon for {tickers}: {var}")
