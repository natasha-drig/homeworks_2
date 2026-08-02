import pandas as pd


class DataProcessor:
    """Класс для проверки и предварительной обработки данных."""

    @staticmethod
    def remove_duplicates(data):
        """Удаляет полностью повторяющиеся строки."""
        return data.drop_duplicates().copy()

    @staticmethod
    def convert_data_types(data):
        """Преобразует дату, цену и количество в подходящие типы данных."""
        result = data.copy()

        # Некорректные даты превращаются в пропуски NaT.
        result["Transaction_Date"] = pd.to_datetime(
            result["Transaction_Date"],
            errors="coerce"
        )

        # Удаляем знак доллара и преобразуем цену в число.
        result["Price"] = (
            result["Price"]
            .astype("string")
            .str.replace("$", "", regex=False)
            .str.strip()
        )
        result["Price"] = pd.to_numeric(result["Price"], errors="coerce")

        # Преобразуем количество в число.
        result["Quantity"] = pd.to_numeric(
            result["Quantity"],
            errors="coerce"
        )

        return result

    @staticmethod
    def standardize_categories(data):
        """Приводит способы оплаты и статусы к единому написанию."""
        result = data.copy()

        payment_mapping = {
            "creditcard": "Credit Card",
            "credit card": "Credit Card",
            "cash": "Cash",
            "paypal": "PayPal",
            "pay pal": "PayPal"
        }

        result["Payment_Method"] = (
            result["Payment_Method"]
            .astype("string")
            .str.strip()
            .str.lower()
            .replace(payment_mapping)
        )

        status_mapping = {
            "complete": "Completed",
            "completed": "Completed",
            "pending": "Pending",
            "failed": "Failed"
        }

        result["Transaction_Status"] = (
            result["Transaction_Status"]
            .astype("string")
            .str.strip()
            .str.lower()
            .replace(status_mapping)
        )

        return result

    @staticmethod
    def mark_invalid_numbers_as_missing(data):
        """
        Заменяет отрицательные количества и цены на пропуски.
        Строки не удаляются, чтобы не искажать число транзакций.
        """
        result = data.copy()

        result.loc[result["Quantity"] < 0, "Quantity"] = pd.NA
        result.loc[result["Price"] < 0, "Price"] = pd.NA

        return result

    @classmethod
    def prepare_data(cls, data):
        """Последовательно выполняет основные этапы обработки."""
        result = cls.remove_duplicates(data)
        result = cls.convert_data_types(result)
        result = cls.standardize_categories(result)
        result = cls.mark_invalid_numbers_as_missing(result)
        return result

