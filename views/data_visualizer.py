import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('agg')

class DataVisualizer:
    def __init__(self, padding):
        self.padding = padding

    def create_figure(self, figure_type, data, *args, **kwargs):
        # Based on figure_type, create different figures
        if figure_type == 'bar':
            return self._create_bar_figure(data, *args, **kwargs)
        elif figure_type == 'pie':
            return self._create_pie_figure(data, *args, **kwargs)
        elif figure_type == 'line':
            return self._create_line_figure(data, **kwargs)
        else:
            raise ValueError(f"Unsupported figure type: {figure_type}")

    def _create_bar_figure(self, data, title="Bar Chart", xlabel="X", ylabel="Y"):
        """
        Creates a bar chart figure.

        Parameters:
        - data: A dictionary where keys are categories (x-values) and values are the corresponding values (y-values).
        - title: The title of the chart.
        - xlabel: The label for the x-axis.
        - ylabel: The label for the y-axis.

        Returns:
        A matplotlib figure and axes.
        """
        fig, ax = plt.subplots(dpi=75)  # Adjust dpi as needed
        ax.bar(data.keys(), data.values())
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        return fig, ax

    def _create_pie_figure(self, data, title="Pie Chart"):
        """
        Creates a pie chart figure.

        Parameters:
        - data: A dictionary where keys are labels for the pie sections and values are the corresponding sizes.
        - title: The title of the chart.

        Returns:
        A matplotlib figure and axes.
        """
        fig, ax = plt.subplots(dpi=75)  # Adjust dpi as needed
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
        ax.set_title(title)
        return fig, ax

    def _create_line_figure(self, data, title="Line Chart", xlabel="X", ylabel="Y"):
        """
        Creates a line graph figure.

        Parameters:
        - data: A dictionary where keys are the x-axis labels and values are the corresponding y-values.
        - title: The title of the chart.
        - xlabel: The label for the x-axis.
        - ylabel: The label for the y-axis.

        Returns:
        A matplotlib figure and axes.
        """
        fig, ax = plt.subplots(dpi=75)
        ax.plot(list(data.keys()), list(data.values()), marker='o')  # Use 'marker' to mark each data point
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        return fig, ax
