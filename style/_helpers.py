from __future__ import annotations

import matplotlib as mpl


def generate_style(
    foreground: str,
    background: str,
    comment: str,
    cycle: list[str],
) -> dict:
    return {
        "lines.color": foreground,
        "patch.edgecolor": foreground,
        "text.color": foreground,
        "axes.facecolor": background,
        "axes.edgecolor": foreground,
        "axes.labelcolor": foreground,
        "xtick.color": foreground,
        "ytick.color": foreground,
        "grid.color": comment,
        "figure.facecolor": background,
        "figure.edgecolor": background,
        "savefig.facecolor": background,
        "savefig.edgecolor": background,
        "boxplot.boxprops.color": foreground,
        "boxplot.capprops.color": foreground,
        "boxplot.flierprops.color": foreground,
        "boxplot.flierprops.markeredgecolor": foreground,
        "boxplot.whiskerprops.color": foreground,
        "axes.prop_cycle": mpl.cycler(color=cycle),
        "font.size": 14,
    }


if __name__ == "__main__":
    plot = generate_style(
        background="#FFFFFF",
        foreground="#000000",
        comment="#ABB0B6",
        cycle=[
            "#7fb3b8",  # Light blue
            "#C08497",  # red
            "#F1A500",  # orange
            "#F7E3AF",  # Peach
            "#C3EEC3",  # Lemon chiffon
            "#84DCC6",  # gray
            "#ACD7EC",  # Uranian Blue
        ],
    )
