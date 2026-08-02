import matplotlib.pyplot as plt


class DataVisualizer:
    """Класс для создания и удаления визуализаций."""

    def add_histogram(self, data, column, bins=20):
        """Строит гистограмму для одного числового столбца."""
        plt.figure()
        data[column].dropna().plot(kind="hist", bins=bins)
        plt.title(f"Распределение: {column}")
        plt.xlabel(column)
        plt.ylabel("Количество")
        plt.tight_layout()
        plt.show()

    def add_line_plot(self, data, x_column, y_column):
        """Строит линейный график."""
        plt.figure()
        plt.plot(data[x_column], data[y_column])
        plt.title(f"{y_column} по {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def add_scatter_plot(self, data, x_column, y_column):
        """Строит диаграмму рассеяния."""
        plt.figure()
        plt.scatter(data[x_column], data[y_column], alpha=0.4)
        plt.title(f"{y_column} и {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def remove_visualization():
        """Закрывает все открытые графики."""
        plt.close("all")
