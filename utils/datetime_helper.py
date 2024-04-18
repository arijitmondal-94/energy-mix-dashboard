from datetime import datetime, time
import pandas as pd
import numpy as np

def time_to_isp(index_time: time) -> int:
    time_range = pd.date_range("00:00", "23:30", freq="30min").time
    isp = np.where(time_range == index_time)[0][0]
    return 48 if isp == 0 else isp

def isp_to_time(isp: int) -> time:
    pass