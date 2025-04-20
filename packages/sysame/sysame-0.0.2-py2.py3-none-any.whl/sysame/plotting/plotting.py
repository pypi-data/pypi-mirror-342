"""
Module for all plotting classes an functions.
"""

##### IMPORTS #####

# Standard imports
from pathlib import Path
from typing import Optional

# Third party imports
import numpy as np
from numpy.typing import ArrayLike
import seaborn as sns  # type: ignore
from scipy import stats  # type: ignore
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Local imports

# Import Rules

##### CONSTANTS #####

##### CLASSES #####


##### FUNCTIONS #####
def scatter_plot(
    x_data: ArrayLike,
    y_data: ArrayLike,
    density_data: Optional[ArrayLike] = None,
    density_label: str = "Density",
    xlabel: str = "X values",
    ylabel: str = "Y values",
    title: str = "Scatter Plot with Regression",
    gridsize: int = 40,
    plot_save_path: Optional[Path] = None,
) -> None:
    """Polished scatter plot with regression line and optional density grid using hexbin.

    Parameters
    ----------
    x_data : ArrayLike
        X axis values array
    y_data : ArrayLike
        Y axis values array
    density_data : ArrayLike, optional
        Density values for hexbin, by default None
    density_label : str, optional
        Density label, by default "Density"
    x_label : str, optional
        X axis label, by default "X values"
    y_label : str, optional
        Y axis label, by default "Y values"
    title : str, optional
        Plot title, by default "Scatter Plot with Regression"
    gridsize : int, optional
        Number of hexagons in hexbin plot, by default 40
    plot_save_path : Path | None, optional
        Path to save the plot, by default None
    """
    # Convert to numpy arrays
    x_array = np.asarray(x_data)
    y_array = np.asarray(y_data)
    # Check they are the same dimensions
    if x_array.shape != y_array.shape:
        raise ValueError("All input arrays must have the same shape.")

    # Flatten arrays
    x_array_flatten = x_array.flatten()
    y_array_flatten = y_array.flatten()

    if density_data is not None:
        # Convert to numpy array
        density_array = np.asarray(density_data)
        # Check shape
        if density_array.shape != x_array.shape:
            raise ValueError(
                "Density array must have the same shape as x and y arrays."
            )
        # Flatten array
        density_array_flatten = density_array.flatten()
    else:
        density_array_flatten = None

    # Seaborn styling
    sns.set_theme(style="whitegrid", palette="viridis", font_scale=1.2)
    plt.rcParams["figure.facecolor"] = "whitesmoke"
    plt.rcParams["axes.edgecolor"] = ".2"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["xtick.color"] = ".2"
    plt.rcParams["ytick.color"] = ".2"
    plt.rcParams["legend.frameon"] = True
    plt.rcParams["legend.facecolor"] = "white"
    plt.rcParams["legend.edgecolor"] = ".2"

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calculate regression
    slope, intercept, r_value, _, _ = stats.linregress(x_array_flatten, y_array_flatten)
    r_squared = r_value**2
    reg_line = slope * x_array_flatten + intercept

    # Get plot limits with some padding
    min_val = min(np.min(x_array_flatten), np.min(y_array_flatten))
    max_val = max(np.max(x_array_flatten), np.max(y_array_flatten))
    padding = 0.05 * (max_val - min_val)
    extent = (
        min_val - padding,
        max_val + padding,
        min_val - padding,
        max_val + padding,
    )

    # Create scatter plot or hexbin density grid
    if density_array_flatten is None:
        ax.scatter(
            x_array_flatten,
            y_array_flatten,
            alpha=0.7,
            color=sns.color_palette("plasma")[4],
            edgecolors="gray",
            linewidth=0.5,
            s=20,
            label="Data Points",
        )
    else:
        # Colourmap
        cmap = sns.cubehelix_palette(rot=-0.2, as_cmap=True)
        hb = ax.hexbin(
            x_array_flatten,
            y_array_flatten,
            C=density_array_flatten,
            gridsize=gridsize,
            cmap=cmap,
            extent=extent,
            mincnt=1,
            reduce_C_function=np.sum,
        )
        # Colour bar
        cbar = fig.colorbar(hb, ax=ax, label=density_label, shrink=0.8)
        cbar.ax.tick_params(labelsize=10)
        cbar.outline.set_linewidth(0.7)

    # Identity line
    ax.plot(
        [min_val, max_val],
        [min_val, max_val],
        "--",
        color="dimgray",
        linewidth=1.2,
        label="Identity line (y = x)",
        zorder=10,
    )

    # Regression line with equation and R-squared
    ax.plot(
        x_array_flatten,
        reg_line,
        color=sns.color_palette("Set1")[0],
        linewidth=2.0,
        alpha=0.8,
        label=f"$y = {slope:.2f}x {'+' if intercept >= 0 else '-'} {abs(intercept):.2f}$\n$R^2 = {r_squared:.3f}$",
        zorder=11,
    )

    # Set plot limits
    ax.set_xlim(min_val - padding, max_val + padding)
    ax.set_ylim(min_val - padding, max_val + padding)

    # Labels and title
    ax.set_xlabel(xlabel, fontsize=13, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=13, labelpad=10)
    ax.set_title(title, fontsize=16, fontweight="semibold", color=".2", pad=15)

    # Grid
    ax.grid(True, linestyle="--", alpha=0.6, color=".7")

    # Legend
    ax.legend(
        loc="upper left",
        frameon=True,
        shadow=True,
        edgecolor=".2",
        facecolor="white",
        fontsize=10,
    )

    # Format ticks
    ax.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:,.1f}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:,.1f}"))
    ax.tick_params(axis="both", which="major", labelsize=10)

    # Adjust layout
    plt.tight_layout()

    if plot_save_path is not None:
        plt.savefig(plot_save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()


def plot_data_diffs_analysis(
    x_data: ArrayLike,
    y_data: ArrayLike,
    xlabel: str = "X values",
    ylabel: str = "Y values",
    attribute: str = "Data",
    save_path: Path | None = None,
):
    """Comprehensive analysis of differences between two data sets.

    Parameters
    ----------
    x_data : ArrayLike
        X-axis Data
    y_data : ArrayLike
        Y-axis Data
    xlabel : str, optional
        Label for the x-axis, by default "Pre."
    ylabel : str, optional
        Label for the y-axis, by default "Post"
    attribute : str, optional
        Name of the attribute being analyzed, by default "Data"
    save_path : Path | None, optional
        Path to save the figure, by default None
    """
    # Convert to numpy arrays
    x_array = np.asarray(x_data)
    y_array = np.asarray(y_data)
    # Check they are the same dimensions
    if x_array.shape != y_array.shape:
        raise ValueError("All input arrays must have the same shape.")

    # Flatten arrays
    x_array_flatten = x_array.flatten()
    y_array_flatten = y_array.flatten()

    # Basic statistics
    diff = y_array_flatten - x_array_flatten

    # Seaborn styling
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)
    plt.rcParams["figure.facecolor"] = "whitesmoke"
    plt.rcParams["axes.edgecolor"] = ".2"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["xtick.color"] = ".2"
    plt.rcParams["ytick.color"] = ".2"
    plt.rcParams["legend.frameon"] = True
    plt.rcParams["legend.facecolor"] = "white"
    plt.rcParams["legend.edgecolor"] = ".2"

    # Create figure layout
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    fig.suptitle(
        f"{xlabel} vs. {ylabel} Analysis of {attribute}",
        fontsize=20,
        fontweight="bold",
        color=".2",
    )

    # Tick formatter
    formatter = FuncFormatter(lambda x, _: f"{x:,.1f}")
    formatter_int = FuncFormatter(lambda x, _: f"{int(x):,}")

    # Consistent title style for subplots
    title_font = {"fontsize": 15, "fontweight": "semibold", "color": ".2"}

    # 1. Scatter plot with regression
    ax1 = axes[0, 0]

    # Calculate regression
    slope, intercept, r_value, _, _ = stats.linregress(x_array_flatten, y_array_flatten)
    r_squared = r_value**2
    reg_line = slope * x_array_flatten + intercept

    # Format
    scatter_color = "indianred"
    ax1.scatter(
        x_array_flatten,
        y_array_flatten,
        alpha=0.7,
        color=scatter_color,
        edgecolors="gray",
        linewidth=0.5,
        s=30,
    )

    # Identity line
    min_val = min(np.min(x_array_flatten), np.min(y_array_flatten))
    max_val = max(np.max(x_array_flatten), np.max(y_array_flatten))
    ax1.plot(
        [min_val, max_val],
        [min_val, max_val],
        "--",
        color="dimgray",
        linewidth=1.2,
        label="Identity line (y = x)",
    )

    # Regression line with equation and R-squared
    ax1.plot(
        x_array_flatten,
        reg_line,
        color="cornflowerblue",
        linewidth=2,
        alpha=0.8,
        label=f"$y = {slope:.2f}x {'+' if intercept >= 0 else '-'} {abs(intercept):.2f}$\n$R^2 = {r_squared:.3f}$",
    )

    # Clearer labels and title
    ax1.set_xlabel(f"{xlabel} {attribute}", fontsize=13)
    ax1.set_ylabel(f"{ylabel} {attribute}", fontsize=13)
    ax1.set_title("Pre vs. Post Scatter Plot", fontdict=title_font)
    ax1.legend(loc="upper left", fontsize=10, shadow=True)
    ax1.grid(True, linestyle="--", alpha=0.7, color=".7")
    ax1.tick_params(axis="both", which="major", labelsize=10)
    ax1.xaxis.set_major_formatter(formatter)
    ax1.yaxis.set_major_formatter(formatter)

    # 2. Residual plot
    residual_color = "sandybrown"
    ax2 = axes[0, 1]
    ax2.scatter(
        x_array_flatten,
        diff,
        alpha=0.7,
        color=residual_color,
        s=20,
        edgecolors="gray",
        linewidth=0.5,
    )
    ax2.axhline(y=0, color="dimgray", linestyle="--", alpha=0.8, linewidth=1.2)
    ax2.set_xlabel(f"{xlabel} {attribute}", fontsize=13)
    ax2.set_ylabel(f"Residuals ({ylabel} - {xlabel})  {attribute}", fontsize=13)
    ax2.set_title("Residual Plot", fontdict=title_font)
    ax2.grid(True, linestyle="--", alpha=0.7, color=".7")
    ax2.tick_params(axis="both", which="major", labelsize=10)
    ax2.xaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(formatter)

    # 3. Histogram of differences
    hist_color = "lightcoral"
    ax3 = axes[1, 0]
    ax3.hist(
        diff, bins=30, alpha=0.8, color=hist_color, edgecolor="gray", linewidth=0.7
    )
    ax3.axvline(x=0, color="dimgray", linestyle="--", alpha=0.8, linewidth=1.2)
    ax3.set_xlabel(f"Difference ({ylabel} - {xlabel}) {attribute}", fontsize=13)
    ax3.set_ylabel("Frequency", fontsize=13)
    ax3.set_title("Distribution of Differences", fontdict=title_font)
    ax3.grid(axis="y", linestyle="--", alpha=0.7, color=".7")
    ax3.tick_params(axis="both", which="major", labelsize=10)
    ax3.xaxis.set_major_formatter(formatter)
    ax3.yaxis.set_major_formatter(formatter_int)

    # 4. Bland-Altman plot
    bland_altman_color = "plum"
    ax4 = axes[1, 1]
    mean = (x_array_flatten + y_array_flatten) / 2
    ax4.scatter(
        mean,
        diff,
        alpha=0.7,
        color=bland_altman_color,
        s=20,
        edgecolors="gray",
        linewidth=0.5,
    )
    mean_diff = np.mean(diff)
    std_diff = np.std(diff)
    limit_of_agreement = 1.96 * std_diff
    ax4.axhline(
        y=mean_diff,
        color=sns.color_palette("dark:#5A9_r")[0],
        linestyle="-",
        alpha=0.8,
        linewidth=1.5,
        label=f"Mean diff: {mean_diff:.3f}",
    )
    ax4.axhline(
        y=mean_diff + limit_of_agreement,
        color="dimgray",
        linestyle="--",
        alpha=0.8,
        linewidth=1.2,
        label=f"LoA (+1.96 SD): {mean_diff + limit_of_agreement:.3f}",
    )
    ax4.axhline(
        y=mean_diff - limit_of_agreement,
        color="dimgray",
        linestyle="--",
        alpha=0.8,
        linewidth=1.2,
        label=f"LoA (-1.96 SD): {mean_diff - limit_of_agreement:.3f}",
    )
    ax4.set_xlabel(f"Mean of {xlabel} and {ylabel} {attribute}", fontsize=13)
    ax4.set_ylabel(f"Difference ({ylabel} - {xlabel}) {attribute}", fontsize=13)
    ax4.set_title("Bland-Altman Plot", fontdict=title_font)
    ax4.legend(fontsize=10, shadow=True)
    ax4.grid(True, linestyle="--", alpha=0.7, color=".7")
    ax4.tick_params(axis="both", which="major", labelsize=10)
    ax4.xaxis.set_major_formatter(formatter)
    ax4.yaxis.set_major_formatter(formatter)

    plt.tight_layout(
        rect=(0, 0.03, 1, 0.95)
    )  # Adjust layout to prevent overlap with sup-title

    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
