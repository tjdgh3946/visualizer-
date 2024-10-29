import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotx
import numpy as np
import itertools
from style.asahikawa import asahikawa
import matplotlib.ticker as ticker


def addlabels(x, y, fontsize=8, label_offset=0.0):
    for x_, y_ in zip(x, y):
        plt.text(x_, y_ + label_offset, y_, ha="center", fontsize=fontsize)


def updateminmax(yarray):
    array = np.concatenate([yarr for yarr in yarray])

    ymin, ymax = np.min(array), np.max(array)

    return ymin, ymax


class Visualizer:
    def __init__(self, path, xaxis=False, CI=False, label_axis="row", style=None):
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
            # If the CI set to true, save the confidence interval value
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
        self.style = {"plot": "plot1", "hist": "hist1", "bar": "bar1"}  # default style
        if style:
            self.style.update(style)
        plt.rcParams["font.family"] = "DejaVu Serif"

    def plot(
        self,
        marker=False,
        linestyle=None,
        grid=False,
        xlabel=None,
        ylabel=None,
        title=None,
        legend=False,
        markersize=7,
        y_resolution=3,
        filesave=None,
    ):
        """This method plot (x0, yy) for all labels (e.g, model, method)
        If the marker="enum", different marker style for each plot is applied"""

        CI_flag = True if self.CI.all() else False
        if marker == "enum":
            markers = itertools.cycle(("^", "D", "s", "o", "X"))
        else:
            markers = itertools.cycle((marker))

        colors = []
        marker_stack = []
        with plt.style.context(asahikawa[self.style["plot"]]):
            for i, (y, label) in enumerate(zip(self.yy, self.labels)):
                if label[-1] == "_":
                    label = None

                if label:
                    fig = plt.plot(
                        self.x0,
                        y,
                        label=label,
                        marker=next(markers),
                        linestyle=linestyle,
                        markersize=markersize,
                    )
                    colors.append(fig[0].get_color())
                    marker_stack.append(fig[0].get_marker())
                else:
                    color_index = int(
                        i - len(self.labels) / 2
                    )  # if there is no label, follow the previous one.
                    fig = plt.plot(
                        self.x0,
                        y,
                        label=label,
                        color=colors[color_index],
                        marker=marker_stack[color_index],
                        linestyle=linestyle,
                        markersize=markersize,
                    )

                if CI_flag:
                    try:
                        plt.fill_between(
                            self.x0, y - self.CI[i], y + self.CI[i], alpha=0.2
                        )
                    except ValueError:
                        print(
                            "Please check the shape of file.csv and file_CI.csv are same."
                        )

            # Ticks setting
            plt.xticks(self.x0[::2])
            current_xticks, current_yticks = (
                plt.gca().get_xticks(),
                plt.gca().get_yticks(),
            )
            plt.yticks(current_yticks[::y_resolution])

            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            if grid:
                plt.grid(which="major")
            if title:
                plt.title(title, pad=10)
            if legend:
                leg = plt.legend(framealpha=0.33)
                leg.get_frame().set_edgecolor("black")
            else:
                matplotx.line_labels()
            plt.plot()
            if filesave:
                plt.savefig(filesave, dpi=300, bbox_inches="tight")

    def two_yscale_plot(
        self,
        marker=None,
        linestyle=None,
        grid=False,
        xlabel=None,
        ylabel=None,
        title=None,
        markersize=7,
        filesave=None,
    ):
        """This method plot (x0 ,yy) for two y scales"""
        CI_flag = True if self.CI.any() else False
        with plt.style.context(asahikawa[self.style["plot"]]):
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
            )
            plot2 = ax2.plot(
                self.x0,
                self.yy[1],
                label=self.labels[1],
                marker=marker,
                linestyle=linestyle,
                markersize=markersize,
            )
            if CI_flag:
                ax1.fill_between(
                    self.x0, self.yy[0] - self.CI[0], self.yy[0] + self.CI[0], alpha=0.2
                )
                ax2.fill_between(
                    self.x0, self.yy[1] - self.CI[1], self.yy[1] + self.CI[1], alpha=0.2
                )
            plt.xticks(self.x0[::2], rotation="vertical")
            if xlabel:
                ax1.set_xlabel(xlabel)

            ax1.set_ylabel(self.labels[0], color=plot1[0].get_color())
            ax2.set_ylabel(self.labels[1], color=plot2[0].get_color())
            if grid:
                plt.grid()
            if title:
                plt.title(title, pad=10)
            plt.plot()
            if filesave:
                plt.savefig(filesave, dpi=300, bbox_inches="tight")

    def histogram(
        self, density=False, xlabel=None, ylabel=None, title=None, filesave=None
    ):
        """Plot histogram"""
        with plt.style.context(asahikawa[self.style["hist"]]):
            for y, label in zip(self.yy, self.labels):
                plt.hist(y, alpha=0.7, density=density, label=label)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.legend(framealpha=0.5)
            if title:
                plt.title(title, pad=10)
            plt.plot()
            if filesave:
                plt.savefig(filesave, dpi=300, bbox_inches="tight")

    def mutiple_bar(
        self,
        rotation=0,
        margin_ratio=1.5,
        grid=False,
        show_value=False,
        xlabel=None,
        ylabel=None,
        title=None,
        filesave=None,
        label_offset=0.02,
    ):
        """Plot multiple bar, self.x0: category list, self.labels: class"""
        CI_flag = True if self.CI.any() else False
        with plt.style.context(asahikawa[self.style["bar"]]):
            # plt.cla()
            plt.rcParams.update({"axes.edgecolor": "black"})
            fig, ax = plt.subplots(figsize=(2.0 * len(self.x0), 5))
            width = 0.4
            offsets = (
                np.arange(len(self.x0)) * (len(self.labels) * margin_ratio) * width
            )
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
                    addlabels(offsets + width * i, y, label_offset=ylim * label_offset)
            centering = (
                width * (len(self.labels) / 2)
                if len(self.labels) / 2 == 0
                else width * (len(self.labels) / 2 - 0.5)
            )
            plt.xticks(offsets + centering, self.x0, rotation=rotation, fontsize=14)
            plt.ylim(np.min(self.yy) * 0.8, np.max(self.yy) * 1.2)
            if grid:
                plt.gca().yaxis.grid(True, color="#989898")
            plt.legend(
                loc="upper center", ncol=4, shadow=False, fontsize=12, framealpha=0.5
            )
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            if title:
                plt.title(title, pad=10)
            if filesave:
                plt.savefig(filesave, bbox_inches="tight")
            plt.tight_layout()
            plt.show()

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
            plt.title(title, fontsize=14)
