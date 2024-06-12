from ctoi import visualizer

visualizer = visualizer.Visualizer("data/temp.csv", xaxis=True, CI=False)
visualizer.mutiple_bar(
    grid=False, xlabel="temperature", ylabel="AUROC", title="Multiple bar chart"
)
