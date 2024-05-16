import numpy as np
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('agg')

# Setting global font properties
plt.rcParams['font.size'] = 16  # Sets the global font size


class DataVisualizer:
    """
    Class responsible for creating diagrams to present the analyzed data.
    """

    def __init__(self):
        """
        Initialize the class.
        """

    def create_figure(self, figure_type, data, *args, **kwargs):
        """
        Based on figure_type, create different figures.
        :param figure_type: The type of figure to create.
        :param data: A dictionary with label and axis data.
        :param args: Additional positional arguments that are passed directly to the figure creation method.
        :param kwargs: Additional keyword arguments that are passed directly to the figure creation method.
        :return: A matplotlib figure and axes.
        """
        if figure_type == 'bar':
            return self._create_bar_figure(data, *args, **kwargs)
        elif figure_type == 'pie':
            return self._create_pie_figure(data, *args, **kwargs)
        elif figure_type == 'line':
            return self._create_line_figure(data, **kwargs)
        elif figure_type == 'spider':
            return self._create_spider_chart(data, *args, **kwargs)
        else:
            raise ValueError(f"Unsupported figure type: {figure_type}")

    @staticmethod
    def _create_bar_figure(data, title="Bar Chart", xlabel="X", ylabel="Y"):
        """
        Creates a bar chart figure.
        :param data: A dictionary where keys are categories (x-values) and values are the
        corresponding values (y-values).
        :param title: The title of the chart.
        :param xlabel: The label for the x-axis.
        :param ylabel: The label for the y-axis.
        :return: A matplotlib figure and axes.
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=75)
        ax.bar(data.keys(), data.values())
        ax.set_title(title)
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(data.keys(), rotation=30, ha="right")
        plt.tight_layout(pad=3.0)
        ax.set_xlabel(xlabel, labelpad=15)
        ax.set_ylabel(ylabel, labelpad=15)
        plt.subplots_adjust(bottom=0.3, left=0.15)
        return fig, ax

    @staticmethod
    def _create_pie_figure(data, title="Pie Chart"):
        """
        Creates a pie chart figure.
        :param data: A dictionary where keys are labels for the pie sections and values are the corresponding sizes.
        :param title: The title of the chart.
        :return: A matplotlib figure and axes.
        """
        threshold = 0.05  # 5% of the total
        total = sum(data.values())
        other = sum(value for value in data.values() if value / total < threshold)
        data_filtered = {k: v for k, v in data.items() if v / total >= threshold}
        if other > 0:
            data_filtered['Others'] = other

        fig, ax = plt.subplots(figsize=(10, 6), dpi=75)
        # autopct generates the percentage labels on the pie pieces.
        ax.pie(data_filtered.values(), labels=data_filtered.keys(), autopct='%1.1f%%', startangle=90,
               counterclock=False)

        ax.set_title(title)
        plt.tight_layout()
        return fig, ax

    @staticmethod
    def _create_line_figure(data, title="Line Chart", xlabel="X", ylabel="Y"):
        """
        Creates a line graph figure.
        :param data: A dictionary where keys are the x-axis labels and values are the corresponding y-values.
        :param title: The title of the chart.
        :param xlabel: The label for the x-axis.
        :param ylabel: The label for the y-axis.
        :return: A matplotlib figure and axes.
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=75)
        ax.plot(list(data.keys()), list(data.values()), marker='o')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(data.keys(), rotation=45, ha="right")
        plt.subplots_adjust(bottom=0.16)
        return fig, ax

    @staticmethod
    def _create_spider_chart(data, title="Spider Chart"):
        """
        Creates a spider chart (radar chart).
        :param data: A dictionary where each key is a category with its corresponding value.
        :param title: The title of the chart.
        :return: A matplotlib figure and axes.
        """
        labels = list(data.keys())
        values = list(data.values())
        values += values[:1]  # Repeat the first value to close the circle

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]  # Repeat the first angle to close the circle

        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True), dpi=75)
        ax.fill(angles, values, "#158274", alpha=0.1)
        ax.plot(angles, values, "#3FA27B")
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        ax.set_title(title, position=(0.5, 1.1), ha='center')
        return fig, ax
