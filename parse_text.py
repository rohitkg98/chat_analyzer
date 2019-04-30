import re
import numpy as np
import pandas as pd

def parse(file_path):
    """
    args 
        - file_path : str, path to the .txt WhatsApp Backup
    
    returns pd.DataFrame, containing columns date, sender and message
    """
    cols = ['date', 'sender', 'message']
    r = re.compile('.{2}/.{2}/.{2}, .{2}:.{2}')

    df = pd.read_fwf(file_path, colspecs=[(0,15), (18, 31), (33, -1)],
                    skiprows=1, names=cols)
    df = df.dropna()

    df = df.apply(lambda x: x if r.match(x['date']) else pd.Series([np.NaN, np.NaN, x['date']+x['sender']+x['message']], index=cols), axis=1)

    df = df.fillna(method='ffill')

    return df