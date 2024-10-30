import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import itertools
import scienceplots


plt.style.use(["science", "no-latex"])


def addlabels(x, y, fontsize=8, label_offset=0.0):
    for x_, y_ in zip(x, y):
        plt.text(x_, y_ + label_offset, y_, ha="center", fontsize=fontsize)


class MonetPlot:
    def __init__(
        self,
        path=None,
        xaxis=False,
        CI=False,
        label_axis="row",
        labels=None,
        x0=None,
        yy=None,
        CI_value=None,
    ):
        """
        Initializes the data handler with path and axis options for labels and confidence intervals.
        Allows for direct input of labels, x0, and yy if path is None.

        Parameters:
        path (str or None): The file path to the data file. If None, labels, x0, and yy must be provided as numpy arrays.
        xaxis (bool): If True, the first column (or first row) is used as x-axis values.
        CI (bool): If True, confidence interval (CI) values are used in the figures.
                   Ensure that the CI file is saved with the name <file_name>_CI.csv.
        label_axis (str): Specifies the axis where labels (classes) are located.
                          If set to "col", the first column is used for labels.
                          If set to "row", the first row is used for labels.
        labels (numpy array): Array of labels if path is None.
        x0 (numpy array): Array of x-axis values if path is None.
        yy (numpy array): 2D array of y-axis values if path is None.
        CI_value (numpy array or None): Array of confidence interval values if CI is True.
        """

        if path is None:
            # Check if labels, x0, and yy are provided directly
            if labels is None or x0 is None or yy is None:
                raise ValueError(
                    "When 'path' is None, 'labels', 'x0', and 'yy' must be provided as numpy arrays."
                )
            self.labels = labels
            self.x0 = x0
            self.yy = yy
            self.CI = CI_value if CI_value is not None else np.array([False])

        else:
            # Load data from the CSV file
            if label_axis == "col":
                data = self._csv_cleansing(path, "rows")
                labels = np.squeeze(data.iloc[:, :1].values, axis=1)
                x0 = data.columns.values[1:]
                yy = data.iloc[:, 1:].apply(pd.to_numeric).values
                if CI:
                    CI_path = path.split(".")[0] + "_CI.csv"
                    CI_data = pd.read_csv(CI_path, encoding="UTF8")
                    CI_value = CI_data.iloc[:, :].apply(pd.to_numeric).values.T
                    self.CI = CI_value
                else:
                    self.CI = np.array([False])
            else:
                data = self._csv_cleansing(path, "rows")
                if CI:
                    CI_path = path.split(".")[0] + "_CI.csv"
                    CI_data = pd.read_csv(CI_path, encoding="UTF8")
                    CI_value = CI_data.iloc[:, :].apply(pd.to_numeric).values.T
                    self.CI = CI_value
                else:
                    self.CI = np.array([False])
                if xaxis:
                    labels = data.columns.values[1:]
                    x0 = np.squeeze(data.iloc[:, :1].values, axis=1)
                    yy = data.iloc[:, 1:].apply(pd.to_numeric).values.T
                else:
                    labels = data.columns.values
                    x0 = np.array([1])  # just placeholder
                    yy = data.iloc[:, :].apply(pd.to_numeric).values.T
            self.labels = labels
            self.x0 = x0
            self.yy = yy

    def plot(
        self,
        marker=None,
        linestyle=None,
        grid=False,
        xtick_density=None,
        ytick_density=None,
        xlabel=None,
        ylabel=None,
        legend=False,
        title=None,
        markersize=7,
        titlesize=12,
        path=None,
    ):
        """
        Plots the data series (x0, yy) for each label, with optional customization for markers, line styles, grid, and more.

        This method generates line plots for each series in `yy` based on the x-axis values in `x0`. Optional customization
        allows for setting markers, line styles, grid display, axis labels, legend, title, and saving the figure. If the
        `marker` parameter is set to `"enum"`, unique marker styles are applied for each line to enhance visual distinction.

        Parameters:
        ----------
        marker : bool or str, default=False
            Specifies the marker style. If set to `"enum"`, unique markers will be cycled through for each line in the plot.
            If set to False, no markers are applied.

        linestyle : str or None, default=None
            Specifies the line style for each plot (e.g., "-", "--", "-.", ":"). Defaults to None for Matplotlib's default style.

        grid : bool, default=False
            If True, a grid is displayed on the plot background for improved readability.

        xtick_density : float, default=None
            Controls the density of major y-axis ticks. Values less than 1.0 decrease the number of x-ticks,
            while greater than 1.0 increase the number. For example, setting `xtick_ratio=0.5` halves the
            y-tick density, while `xtick_ratio=2.0 doubles it.

        ytick_density : float, default=None
            Controls the density of major y-axis ticks.

        xlabel : str or None, default=None
            Label for the x-axis. If None, no label is applied.

        ylabel : str or None, default=None
            Label for the y-axis. If None, no label is applied.

        legend : bool, default=False
            If True, displays a legend that labels each plot line based on `self.labels`.

        title : str or None, default=None
            Title of the plot. If None, no title is displayed.

        markersize : int, default=7
            Size of the markers if markers are applied to the plot.

        titlesize : int, default=12
            Font size for the title of the plot.

        path : str or None, default=None
            If provided, saves the plot as an image to the specified file path. Format is inferred from file extension.

        Notes:
        ------
        - This method checks `self.CI` for confidence interval values. If available, it shades the area around each line
          plot to represent the confidence interval.
        - Applies the "nature" style context for a refined visual presentation.
        - Adjusts legend aesthetics if displayed, with a black edge around the legend box.

        Examples:
        ---------
        To create a plot with unique markers for each line, a title, and save it to a file:

            plot(marker="enum", title="Performance Comparison", xlabel="Epoch", ylabel="Accuracy", path="plot.png")
        """

        plt.clf()
        CI_flag = True if self.CI.all() else False
        if marker == "enum":
            markers = itertools.cycle(("^", "D", "s", "o", "X"))

        with plt.style.context("nature"):
            for i, (y, label) in enumerate(zip(self.yy, self.labels)):
                if marker == "enum":
                    plt.plot(
                        self.x0,
                        y,
                        label=label,
                        marker=next(markers),
                        linestyle=linestyle,
                        markersize=markersize,
                        markeredgecolor="black",
                    )
                else:
                    plt.plot(
                        self.x0,
                        y,
                        label=label,
                        marker=marker,
                        linestyle=linestyle,
                        markersize=markersize,
                        markeredgecolor="black",
                    )
                if CI_flag:
                    plt.fill_between(self.x0, y - self.CI[i], y + self.CI[i], alpha=0.2)

            if grid:
                plt.grid()

            # Adjust the ticks
            if xtick_density:
                max_x = plt.gca().get_xlim()[1]
                min_x = plt.gca().get_xlim()[0]
                self._adjust_xticks(plt, min_x, max_x, xtick_density)

            if ytick_density:
                max_y = plt.gca().get_ylim()[1]
                min_y = plt.gca().get_ylim()[0]
                self._adjust_yticks(plt, min_y, max_y, ytick_density)

            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
                # plt.legend(shadow=True)
            if title:
                plt.title(title, fontsize=titlesize)
            if legend:
                leg = plt.legend()

            if path:
                plt.savefig(path, dpi=300)
            plt.plot()

    def two_yscale_plot(
        self,
        marker=None,
        linestyle=None,
        grid=False,
        xtick_density=None,
        xlabel=None,
        ylabel=None,
        title=None,
        markersize=7,
        titlesize=12,
        path=None,
    ):
        """
        Plots two data series (x0, yy) on a single figure with two y-axes for distinct scaling.

        This method generates a line plot with two y-axes (`ax1` and `ax2`) on the same x-axis (`x0`) for comparing two
        data series with different y-axis scales. Each y-axis has an independent scale, making it ideal for contrasting
        data with differing units or magnitudes. Optional customizations include marker style, line style, grid display,
        axis labels, and title. If confidence interval data (`self.CI`) is available, shaded regions representing the
        intervals are added around each line.

        Parameters:
        ----------
        marker : str or None, default=None
            Specifies the marker style for the plot lines. If None, no marker is applied.

        linestyle : str or None, default=None
            Specifies the line style (e.g., "-", "--", "-.", ":"). If None, Matplotlib's default style is used.

        grid : bool, default=False
            If True, displays a grid on the plot background to improve readability.

        xtick_density : float, default=None
            Controls the density of major y-axis ticks. Values less than 1.0 decrease the number of x-ticks,
            while greater than 1.0 increase the number. For example, setting `xtick_ratio=0.5` halves the
            x-tick density, while `xtick_ratio=2.0 doubles it.

        xlabel : str or None, default=None
            Label for the x-axis. If None, no label is displayed.

        ylabel : str or None, default=None
            Not directly used, as `self.labels` is used to set the y-axis labels. If `self.labels` is unavailable,
            consider providing explicit y-axis labels here.

        title : str or None, default=None
            Title of the plot. If None, no title is displayed.

        markersize : int, default=7
            Size of the markers on the plot lines, if markers are applied.

        titlesize : int, default=12
            Font size for the title text.

        path : str or None, default=None
            If specified, saves the plot as an image to the provided file path with a resolution of 300 DPI.
            The format is inferred from the file extension.

        Notes:
        ------
        - This method uses a twin-axis (`ax1` and `ax2`) approach to plot two y-axes. Each axis is colored based on the
          data line color for easy identification.
        - Confidence intervals, if available in `self.CI`, are automatically shaded for each line plot.
        - The x-tick labels are set to display every other label, rotated vertically for readability.

        Example:
        --------
        To create a dual y-axis plot with a title and grid, and save it to a file:

            two_yscale_plot(marker="o", title="Dual Y-Axis Comparison", grid=True, path="dual_y_plot.png")
        """
        CI_flag = True if self.CI.any() else False
        with plt.style.context("nature"):
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax2._get_lines.get_next_color()
            plot1 = ax1.plot(
                self.x0,
                self.yy[0],
                label=self.labels[0],
                marker=marker,
                linestyle=linestyle,
                markersize=markersize,
                markeredgecolor="black",
            )
            plot2 = ax2.plot(
                self.x0,
                self.yy[1],
                label=self.labels[1],
                marker=marker,
                linestyle=linestyle,
                markersize=markersize,
                markeredgecolor="black",
            )
            if CI_flag:
                ax1.fill_between(
                    self.x0, self.yy[0] - self.CI[0], self.yy[0] + self.CI[0], alpha=0.2
                )
                ax2.fill_between(
                    self.x0, self.yy[1] - self.CI[1], self.yy[1] + self.CI[1], alpha=0.2
                )
            plt.xticks(self.x0[::2], rotation="vertical")

            # Adjust the ticks
            if xtick_density:
                max_x = plt.gca().get_xlim()[1]
                min_x = plt.gca().get_xlim()[0]
                self._adjust_xticks(plt, min_x, max_x, xtick_density)

            if xlabel:
                ax1.set_xlabel(xlabel)

            ax1.set_ylabel(self.labels[0], color=plot1[0].get_color())
            ax2.set_ylabel(self.labels[1], color=plot2[0].get_color())
            if grid:
                plt.grid(axis="y")
            if title:
                plt.title(title, fontsize=titlesize)
            if path:
                plt.savefig(path, dpi=300)
            plt.plot()

    def histogram(
        self,
        density=False,
        xlabel=None,
        ylabel=None,
        title=None,
        titlesize=12,
        path=None,
    ):
        """
        Plots a histogram for each dataset in `yy`, with optional density normalization and custom labels.

        This method generates overlaid histograms for each data series in `yy`, with distinct colors and labels for
        easy comparison. Optional parameters allow for normalization, axis labeling, title customization, and
        saving the figure to a specified file path.

        Parameters:
        ----------
        density : bool, default=False
            If True, the histogram will display a probability density instead of counts, where the area under each histogram
            sums to 1. Useful when comparing distributions rather than raw counts.

        xlabel : str or None, default=None
            Label for the x-axis. If None, no label is displayed.

        ylabel : str or None, default=None
            Label for the y-axis. If None, no label is displayed.

        title : str or None, default=None
            Title of the histogram plot. If None, no title is displayed.

        titlesize : int, default=12
            Font size for the title text.

        path : str or None, default=None
            If specified, saves the histogram plot as an image to the provided file path with a resolution of 300 DPI.
            The format is inferred from the file extension.

        Example:
        --------
        To create a normalized histogram with a title and save it to a file:

            histogram(density=True, title="Data Distribution Comparison", xlabel="Value", ylabel="Density", path="histogram.png")
        """
        with plt.style.context("nature"):
            for y, label in zip(self.yy, self.labels):
                plt.hist(y, alpha=0.7, density=density, label=label)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.legend()
            if title:
                plt.title(title, fontsize=titlesize)
            plt.plot()
            if path:
                plt.savefig(path, dpi=300)

    def mutiple_bar(
        self,
        rotation=0,
        grid=False,
        show_value=False,
        cgr=1.5,
        wr=1.0,
        ytick_density=None,
        xlabel=None,
        ylabel=None,
        title=None,
        titlesize=10,
        legend_cols=None,
        path=None,
    ):
        """
        Plots a grouped bar chart with customizable options for category spacing, width ratio, and y-axis tick density.

        This method creates a grouped bar plot for comparing multiple categories, where x-axis labels are derived
        from `x0` and the grouping is determined by `self.labels`. Optional parameters allow for customizing
        rotation, grid, spacing, y-axis tick density, and appearance of plot elements. Confidence intervals can
        be displayed as error bars if available in `self.CI`.

        Parameters:
        ----------
        rotation : int, default=0
            Rotation angle for x-axis tick labels. Use positive or negative integers for angled labels.

        grid : bool, default=False
            If True, displays a grid on the y-axis for enhanced readability.

        show_value : bool, default=False
            If True, displays the values of each bar above the bar itself.

        cgr : float, default=1.5
            Class gap ratio, which controls the spacing between different bar groups. Higher values increase spacing.

        wr : float, default=1.0
            Width ratio for adjusting the width of bars. Higher values make bars wider.

        ytick_density : float, default=None
            Controls the density of major y-axis ticks.

        xlabel : str or None, default=None
            Label for the x-axis. If None, no label is applied.

        ylabel : str or None, default=None
            Label for the y-axis. If None, no label is applied.

        title : str or None, default=None
            Title for the plot. If None, no title is displayed.

        titlesize : int, default=10
            Font size for the plot title.

        legend_cols : int, default=#class
            Number of columns in the legend. If None, the number of column eqauls to the number of classes.

        path : str or None, default=None
            If specified, saves the plot as an image to the given file path with a resolution of 300 DPI. The
            file format is inferred from the file extension.


        Notes:
        ------
        - Each dataset in `self.yy` is represented as a grouped bar plot with an offset determined by `cgr` and `wr`.
        - If `self.CI` is present, error bars are added to represent the confidence intervals.
        - The legend is generated based on `self.labels` and positioned above the plot for compact layout.
        - `ytick_ratio` modifies y-axis tick spacing dynamically, making it useful for customizing visual density.

        Example:
        --------
        To create a grouped bar chart with custom spacing, title, and save it to a file:

            multiple_bar(rotation=45, grid=True, title="Comparison of Models", cgr=2.0, ytick_ratio=1.5, path="bar_plot.png")
        """
        CI_flag = True if self.CI.any() else False
        plt.figure(figsize=(6.4 * cgr * wr, 4.8))
        with plt.style.context("nature"):
            plt.cla()
            plt.rcParams.update({"axes.edgecolor": "black"})
            offsets = np.arange(len(self.x0)) * cgr * wr
            width = 1 / (1 + len(self.labels)) * wr
            for i, (y, label) in enumerate(zip(self.yy, self.labels)):
                yerr = self.CI[i] if CI_flag else None
                plt.bar(
                    offsets + width * i,
                    y,
                    width,
                    yerr=yerr,
                    label=label,
                    ecolor="black",
                    capsize=4,
                )
                if show_value:
                    ylim = plt.gca().get_ylim()[1]
                    addlabels(offsets + width * i, y, label_offset=ylim * 0.02)
            centering = (
                width * (len(self.labels) / 2)
                if len(self.labels) / 2 == 0
                else width * (len(self.labels) / 2 - 0.5)
            )
            plt.xticks(offsets + centering, self.x0, rotation=rotation, fontsize=10)

            if grid:
                plt.gca().yaxis.grid(True)

            if ytick_density:
                max_y = plt.gca().get_ylim()[1]
                min_y = plt.gca().get_ylim()[0]
                self._adjust_yticks(plt, min_y, max_y, ytick_density)

            legend_cols = len(self.yy) if not legend_cols else legend_cols
            plt.legend(loc="upper center", ncol=legend_cols, shadow=False, fontsize=7)
            plt.ylim(0, plt.gca().get_ylim()[1] * 1.1)
            if xlabel:
                plt.xlabel(xlabel, fontsize=12)
            if ylabel:
                plt.ylabel(ylabel, fontsize=12)
            if title:
                plt.title(title, pad=10, fontsize=titlesize)
            if path:
                plt.savefig(path, dpi=300)
            plt.show()

    def _adjust_xticks(self, plt, min_x, max_x, xtick_density):
        """Helper to set custom x-tick spacing."""
        x_ticks = plt.gca().get_xticks()
        if xtick_density >= 1.0:
            tick_interval = (x_ticks[1] - x_ticks[0]) / xtick_density
            new_x_ticks = np.arange(x_ticks[0], x_ticks[-1], tick_interval)
        else:
            num_xticks = len(x_ticks)
            after_num_xticks = int(np.ceil(num_xticks * xtick_density))
            interval = num_xticks // after_num_xticks
            new_x_ticks = x_ticks[::interval]
        plt.xticks(new_x_ticks)

    def _adjust_yticks(self, plt, min_y, max_y, ytick_density):
        """Helper to set custom y-tick spacing."""
        y_ticks = plt.gca().get_yticks()
        if ytick_density >= 1.0:
            tick_interval = (y_ticks[1] - y_ticks[0]) / ytick_density
            new_y_ticks = np.arange(y_ticks[0], y_ticks[-1], tick_interval)
        else:
            num_yticks = len(y_ticks)
            after_num_yticks = int(np.ceil(num_yticks * ytick_density))
            interval = num_yticks // after_num_yticks
            new_y_ticks = y_ticks[::interval]
        plt.yticks(new_y_ticks)
        plt.ylim(y_ticks[0], y_ticks[-1])

    def _csv_cleansing(self, path, axis):
        data = pd.read_csv(path, encoding="UTF8")
        data = data.replace("", np.nan)
        data = data.dropna(axis=axis, how="any")
        data[data.select_dtypes("object").columns] = data[
            data.select_dtypes("object").columns
        ].apply(lambda x: x.str.replace(",", ""))

        return data

    def stdout_data(self):
        print(f"Label: ({len(self.labels)})", self.labels)
        print(f"X0: {self.x0.shape}", self.x0)
        print(f"yy: {self.yy.shape}", self.yy[0])
        if self.CI.all():
            print(f"Confidence interval: {self.CI}")

    @staticmethod
    def display_array(array, cmap="Blues"):
        vmin, vmax = array.min(), array.max()
        fig, ax = plt.subplots()
        psm = ax.pcolormesh(array, cmap=cmap, rasterized=False, vmin=vmin, vmax=vmax)
        fig.colorbar(psm, ax=ax)
        plt.show()

    @staticmethod
    def array2csv(stack, tags, path):
        df = pd.DataFrame(stack, columns=tags)
        df.to_csv(path, index=False)

    @staticmethod
    def scatter(x, y, timestamp=None, colormap="RdPu_r", size=18, title=None):
        if type(timestamp) is np.ndarray:
            plt.scatter(x, y, c=timestamp, cmap=colormap, s=size)
            plt.colorbar()
        else:
            plt.scatter(x, y, s=size)
        if title:
            plt.title(title, fontsize=10)
        plt.show()
