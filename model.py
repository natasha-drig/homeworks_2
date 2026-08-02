from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


class TransactionPriceModel:
    """
    Простая модель линейной регрессии.
    Она пытается предсказать цену по количеству товара.
    """

    def __init__(self):
        """Создает объект модели линейной регрессии."""
        self.model = LinearRegression()

    def prepare_model_data(self, data):
        """Выбирает признаки X и целевую переменную y."""
        model_data = data[["Quantity", "Price"]].dropna()

        X = model_data[["Quantity"]]
        y = model_data["Price"]

        return train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

    def train(self, X_train, y_train):
        """Обучает модель на обучающих данных."""
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        """Возвращает прогнозы модели."""
        return self.model.predict(X_test)

    @staticmethod
    def evaluate(y_test, predictions):
        """Считает MSE и коэффициент R²."""
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        return {
            "MSE": round(mse, 2),
            "R2": round(r2, 4)
        }
