from pandas import DataFrame
from sklearn.model_selection import train_test_split


class DataPreparation:
    def __init__(self) -> None:
        self.train_df = None
        self.test_df = None
        pass

    def train_test_split(self, df: DataFrame, test_size=0.2, random_state=42):
        # Split dataset into train and test sets
        self.train_df, self.test_df = train_test_split(
            df, test_size=test_size, random_state=random_state
        )
        return (self.train_df, self.test_df)

    def train_test_split_stratified(
        self, df: DataFrame, test_size=0.2, random_state=42
    ):
        # Split dataset into train and test sets
        self.train_df, self.test_df = train_test_split(
            df, test_size=test_size, random_state=random_state, stratify=df["label"]
        )
        return (self.train_df, self.test_df)
