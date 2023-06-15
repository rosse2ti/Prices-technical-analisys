# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

np.set_printoptions(
    formatter={"float": lambda x: "{0:0.8f}".format(x)}, threshold=sys.maxsize
)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


class Analisys:
    def __init__(self, data_path) -> None:
        self.df = self.__make_df(data_path)
        pass

    def add_ma(self, window_size, ema=True) -> None:
        if ema == True:
            self.df["EXP"] = (
                self.df["Close"]
                .copy()
                .ewm(span=window_size, min_periods=window_size)
                .mean()
            )
        else:
            self.df["SMA"] = self.df["Close"].copy().rolling(window_size).mean()
        pass

    def add_rsi(self, periods=14, ema=True) -> None:
        close_delta = self.df["Close"].diff()

        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)

        if ema == True:
            ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
            ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        else:
            ma_up = up.rolling(window=periods, adjust=False).mean()
            ma_down = down.rolling(window=periods, adjust=False).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100 / (1 + rsi))
        self.df["RSI"] = rsi
        pass

    def __make_df(self, data_path) -> pd.DataFrame:
        df = pd.read_csv(data_path, parse_dates=[["Date", "Time"]])
        df = df.drop(columns=["SPREAD", "VOL"])
        df = df.set_index("Date_Time")
        return df


# %%
csv_path = "csv/NDX.csv"
df_NDX = Analisys(csv_path)
df_NDX.add_ma(36, ema=False)
df_NDX.add_rsi(14, ema=False)
print(df_NDX.df[0:400])

# %%
