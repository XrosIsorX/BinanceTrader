import os

import pandas as pd
import graphviz 
from sklearn.tree import export_graphviz, DecisionTreeRegressor

def export_decision_tree_graph(model, feature_list, output_filename):
    dot_data = export_graphviz(
        model,
        feature_names = feature_list,
        rounded = True,
        proportion = False,
        filled = True,
    )
    graph = graphviz.Source(dot_data)
    graph.render(filename=output_filename, format="png")