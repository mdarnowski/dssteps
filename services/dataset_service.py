import io
from typing import Optional
import pandas as pd
from models.alchemy import Dataset, db
from services.data_processing_service import DataProcessingService


class DatasetService:
    @staticmethod
    def add_dataset(user_id: str, url: str) -> Dataset:
        df = DataProcessingService.load_data(url)
        df = DataProcessingService.clean_data(df)

        # Convert DataFrame to bytes
        csv_data = df.to_csv(index=False).encode('utf-8')

        dataset = Dataset(user_id=user_id, url=url, data=csv_data)
        db.session.add(dataset)
        db.session.commit()

        return dataset

    @staticmethod
    def get_dataset(dataset_id: int) -> Optional[Dataset]:
        return Dataset.query.get(dataset_id)

    @staticmethod
    def get_dataset_dataframe(dataset_id: int):
        dataset = Dataset.query.get(dataset_id)
        df = pd.read_csv(io.BytesIO(dataset.data))
        return df
