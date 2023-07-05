import io
import zipfile

import numpy as np
import pandas as pd
import requests


class DataProcessingService:
    @staticmethod
    def load_data(url):
        df = pd.DataFrame()
        response = requests.get(url)

        if response.status_code == 200:
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            data_file = zip_file.namelist()[0]
            df = pd.read_csv(zip_file.open(data_file), delimiter=';')

            # Convert columns to numerical if possible
            for col in df.columns:
                df[col] = df[col].apply(
                    lambda x: pd.to_numeric(x.replace(',', '.'), errors='coerce')
                    if isinstance(x, str) else x)

        return df

    @staticmethod
    def clean_data(df):
        df = df.dropna(axis=1, how='all')
        df = df.replace(-200, np.nan)
        df = df.fillna(df.median())

        return df
