import pandas as pd


class DataLoader:
    """Класс для загрузки данных из разных источников."""

    @staticmethod
    def load_csv(file_path):
        """Загружает CSV-файл и возвращает DataFrame."""
        return pd.read_csv(file_path)

    @staticmethod
    def load_json(file_path):
        """Загружает JSON-файл и возвращает DataFrame."""
        return pd.read_json(file_path)

    @staticmethod
    def load_api(url):
        """Загружает JSON-данные по URL."""
        return pd.read_json(url)
