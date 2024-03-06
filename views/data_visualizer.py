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

    def _create_pie_figure(self, data, title="Pie Chart"):
        """
        Creates a pie chart figure.

        Parameters:
        - data: A dictionary where keys are labels for the pie sections and values are the corresponding sizes.
        - title: The title of the chart.

        Returns:
        A matplotlib figure and axes.
        """
        threshold = 0.05  # 5% of the total
        total = sum(data.values())
        other = sum(value for value in data.values() if value / total < threshold)
        data_filtered = {k: v for k, v in data.items() if v / total >= threshold}
        if other > 0:
            data_filtered['Others'] = other

        fig, ax = plt.subplots(figsize=(10, 6), dpi=75)
        wedges, texts, autotexts = ax.pie(data_filtered.values(), autopct='%1.1f%%', startangle=90, counterclock=False)
        ax.legend(wedges, data_filtered.keys(), title="Contributors", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax.set_title(title)
        plt.tight_layout()
        plt.subplots_adjust(right=0.7)
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
        fig, ax = plt.subplots(figsize=(10, 6), dpi=75)
        ax.plot(list(data.keys()), list(data.values()), marker='o')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(data.keys(), rotation=45, ha="right")
        plt.subplots_adjust(bottom=0.16)
        return fig, ax
