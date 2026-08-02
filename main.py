from data_loader import DataLoader
from data_processing import DataProcessor
from missing_values import MissingValuesHandler
from visualization import DataVisualizer
from model import TransactionPriceModel


# 1. Загружаем исходный датасет.
data = DataLoader.load_csv("dirty_financial_transactions.csv")

print("Размер исходного датасета:", data.shape)
print("\nПервые пять строк:")
print(data.head())


# 2. Создаем отчет о пропусках до обработки.
print("\nОтчет о пропусках до обработки:")
print(MissingValuesHandler.missing_report(data))


# 3. Очищаем и преобразуем данные.
clean_data = DataProcessor.prepare_data(data)

print("\nКоличество строк после удаления дубликатов:", len(clean_data))


# 4. Заполняем пропуски там, где это обоснованно.
clean_data = MissingValuesHandler.fill_numeric(
    clean_data,
    "Quantity",
    method="mean"
)

clean_data = MissingValuesHandler.fill_numeric(
    clean_data,
    "Price",
    method="mean"
)

clean_data = MissingValuesHandler.fill_categorical(
    clean_data,
    "Transaction_Status"
)

print("\nОтчет о пропусках после частичного заполнения:")
print(MissingValuesHandler.missing_report(clean_data))


# 5. Создаем новый расчетный столбец.
clean_data["Total_Amount"] = (
    clean_data["Quantity"] * clean_data["Price"]
)

# 6. Строим визуализации.
visualizer = DataVisualizer()

visualizer.add_histogram(
    clean_data,
    "Price"
)

visualizer.add_scatter_plot(
    clean_data.sample(1000, random_state=42),
    "Quantity",
    "Price"
)

daily_sales = (
    clean_data
    .dropna(subset=["Transaction_Date"])
    .groupby("Transaction_Date", as_index=False)["Total_Amount"]
    .sum()
    .sort_values("Transaction_Date")
)

visualizer.add_line_plot(
    daily_sales.head(100),
    "Transaction_Date",
    "Total_Amount"
)

visualizer.remove_visualization()


# 7. Обучаем простую модель линейной регрессии.
price_model = TransactionPriceModel()

X_train, X_test, y_train, y_test = (
    price_model.prepare_model_data(clean_data)
)

price_model.train(X_train, y_train)
predictions = price_model.predict(X_test)
metrics = price_model.evaluate(y_test, predictions)

print("\nРезультаты модели:")
print(metrics)


# 8. Сохраняем обработанные данные.
clean_data.to_csv(
    "clean_financial_transactions.csv",
    index=False
)

print("\nОбработанный датасет сохранен.")
