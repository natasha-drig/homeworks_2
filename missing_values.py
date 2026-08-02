class MissingValuesHandler:
    """Класс для анализа и заполнения пропущенных значений."""

    @staticmethod
    def count_missing(data):
        """Возвращает количество пропусков в каждом столбце."""
        return data.isna().sum()

    @staticmethod
    def missing_report(data):
        """Создает отчет: количество и процент пропусков."""
        missing_count = data.isna().sum()
        missing_percent = (missing_count / len(data) * 100).round(2)

        report = missing_count.to_frame(name="missing_count")
        report["missing_percent"] = missing_percent

        return report

    @staticmethod
    def fill_numeric(data, column, method="median"):
        """
        Заполняет пропуски в числовом столбце.
        method может быть 'mean' или 'median'.
        """
        result = data.copy()

        if method == "mean":
            fill_value = result[column].mean()
        elif method == "median":
            fill_value = result[column].median()
        else:
            raise ValueError("Для числового столбца используйте mean или median")

        result[column] = result[column].fillna(fill_value)
        return result

    @staticmethod
    def fill_categorical(data, column):
        """Заполняет пропуски самым частым значением."""
        result = data.copy()
        mode_values = result[column].mode(dropna=True)

        if mode_values.empty:
            raise ValueError(f"В столбце {column} нет значения для заполнения")

        result[column] = result[column].fillna(mode_values.iloc[0])
        return result
