from ._helpers import generate_style

# https://github.com/ayu-theme/ayu-vim/blob/master/colors/ayu.vim


plot1 = generate_style(
    background="#FFFFFF",
    foreground="#000000",
    comment="#d5d7da",
    cycle=[
        "#e8b31b",
        "#32a784",
        "#e93e95",
        "#dc6f1b",
        "#837eba",
        "#75af34",
        "#6f5261",
    ],
)

plot2 = generate_style(
    background="#FFFFFF",
    foreground="#000000",
    comment="#d5d7da",
    cycle=[
        "#FF0000",
        "#2e6930",
        "#0000FF",
        "#808000",
        "#008080",
        "#800080",
        "#bb4400",
    ],
)

plot3 = generate_style(
    background="#FFFFFF",
    foreground="#000000",
    comment="#d5d7da",
    cycle=[
        "#0000FF",
        "#2e6930",
        "#0000FF",
        "#808000",
        "#008080",
        "#800080",
        "#bb4400",
    ],
)


bar1 = generate_style(
    background="#FFFFFF",
    foreground="#000000",
    comment="#d5d7da",
    cycle=["#F1E5D1", "#DBB5B5", "#C39898", "#987070", "#B0A695", "#776B5D"],
)

bar2 = generate_style(
    background="#FFFFFF",
    foreground="#000000",
    comment="#d5d7da",
    cycle=["#ffac81", "#ff928b", "#fec3a6", "#efe9ae", "#cdeac0"],
)

bar3 = generate_style(
    background="#FFFFFF",
    foreground="#000000",
    comment="#d5d7da",
    cycle=["#d88c9a", "#f2d0a9", "#f1e3d3", "#99c1b9", "#8e7dbe"],
)
bar4 = generate_style(
    background="#FFFFFF",
    foreground="#000000",
    comment="#d5d7da",
    cycle=["#084c61", "#db504a", "#e3b505"],
)
hist1 = generate_style(
    background="#FFFFFF",
    foreground="#000000",
    comment="#d5d7da",
    cycle=[
        "#1f77b4",  # (Blue)
        "#ff7f0e",  # (Orange)
        "#2ca02c",  # (Green)
        "#d62728",  # (Red)
        "#9467bd",  # (Purple)
    ],
)

asahikawa = {
    "plot1": plot1,
    "plot2": plot2,
    "plot3": plot3,
    "bar1": bar1,
    "bar2": bar2,
    "bar3": bar3,
    "bar4": bar4,
    "hist1": hist1,
}
