
from ._helpers import generate_style

# https://github.com/ayu-theme/ayu-vim/blob/master/colors/ayu.vim


plot = generate_style(
        background="#FFFFFF",
        foreground="#000000",
        comment="#ABB0B6",
        cycle=[
            "#003f5c",  
            "#A94064",
            "#bc5090",  
            "#ff6361", 
            "#ffa600",  
            "#444e86",    
            "#58508d",  
        ],
    )

plot.update({"font.size": 14})

asahikawa = {
    "plot": plot,
    "bar": generate_style(
        background="#FFFFFF",
        foreground="#000000",
        comment="#ABB0B6",
        cycle=[
            "#B5C2B7",  # Ash gray 
            "#8C93A8",  # Cool gray 
            "#62466B",  # English Violet
            "#45364B",  # English Viloet 
            "#2D2327",  # Raisin black 
            "#363636",  # Jet
            "#242F40",  # Gunmetal
            "#CCA43B",  # Satin Sheen gold
        ],
    ),
    "hist": generate_style(
        background="#FFFFFF",
        foreground="#000000",
        comment="#ABB0B6",
        cycle=[
            "#1f77b4", #(Blue)
            "#ff7f0e", #(Orange)
            "#2ca02c", #(Green)
            "#d62728", #(Red)
            "#9467bd", #(Purple)
        ], 
    ),
}
asahikawa["hist"].update({"font.size": 14})