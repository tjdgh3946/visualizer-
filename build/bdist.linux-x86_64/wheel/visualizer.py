import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotx
import numpy as np
from style.asahikawa import asahikawa


def addlabels(x, y, fontsize=8, label_offset=0.0):
    for x_, y_ in zip(x, y):
        plt.text(x_, y_ + label_offset, y_, ha="center", fontsize=fontsize)


class Visualizer:
    def __init__(self, path, xaxis=False, CI=False, label_axis="row"):
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

    def plot(
        self,
        marker=False,
        linestyle=None,
        grid=False,
        xlabel=None,
        ylabel=None,
        title=None,
    ):
        """This method plot (x0, yy) for all labels (e.g, model, method)"""
        CI_flag = True if self.CI.all() else False
        with plt.style.context(asahikawa["plot"]):
            for i, (y, label) in enumerate(zip(self.yy, self.labels)):
                plt.plot(self.x0, y, label=label, marker=marker, linestyle=linestyle)
                if CI_flag:
                    plt.fill_between(self.x0, y - self.CI[i], y + self.CI[i], alpha=0.2)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
                # plt.legend(shadow=True)
            if grid:
                plt.grid()
            if title:
                plt.title(title, pad=10)
            matplotx.line_labels()
            plt.plot()

    def two_yscale_plot(
        self,
        marker=None,
        linestyle=None,
        grid=False,
        xlabel=None,
        ylabel=None,
        title=None,
    ):
        """This method plot (x0 ,yy) for two y scales"""
        CI_flag = True if self.CI.any() else False
        with plt.style.context(asahikawa["plot"]):
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax2._get_lines.get_next_color()
            plot1 = ax1.plot(
                self.x0,
                self.yy[0],
                label=self.labels[0],
                marker=marker,
                linestyle=linestyle,
            )
            plot2 = ax2.plot(
                self.x0,
                self.yy[1],
                label=self.labels[1],
                marker=marker,
                linestyle=linestyle,
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

    def histogram(self, density=False, xlabel=None, ylabel=None, title=None):
        """Plot histogram"""
        with plt.style.context(asahikawa["hist"]):
            for y, label in zip(self.yy, self.labels):
                plt.hist(y, alpha=0.7, density=density, label=label)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.legend()
            if title:
                plt.title(title, pad=10)
            plt.plot()

    def mutiple_bar(
        self,
        rotation=0,
        grid=False,
        show_value=False,
        xlabel=None,
        ylabel=None,
        title=None,
    ):
        """Plot multiple bar, self.x0: category list, self.labels: class"""
        CI_flag = True if self.CI.any() else False
        with plt.style.context(asahikawa["plot"]):
            plt.cla()
            plt.rcParams.update({"axes.edgecolor": "black"})
            offsets = np.arange(len(self.x0))
            width = 1 / (1 + len(self.labels))
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
            plt.ylim(0, np.max(self.yy) * 1.5)
            if grid:
                plt.gca().yaxis.grid(True)
            plt.legend(loc="upper center", ncol=4, shadow=False, fontsize=8)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            if title:
                plt.title(title, pad=10)
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
