# BIBAS: Bayesian Network Impact Heatmap

<p align="center">
  <img src="examples/bibas_heatmap_example.png" width="600">
</p>

**BIBAS** (Bayesian Networks Impact Factor Based on Analysis of Sensitivity) computes pairwise sensitivity scores between all nodes in a Bayesian Network and visualizes the results in a clean, interpretable heatmap.

## Features

- Quantifies how much **observing a source variable** changes the predicted probability of a **target variable**
- Clean `.plot_bibas_heatmap(model)` interface
- Diagonal cells visually excluded via **hatching** (no self-impact)
- Supports `pgmpy` models (`DiscreteBayesianNetwork`) with **binary nodes**
- For multi-state support, see my thesis or [contact me](mailto:giladmatat@gmail.com)

---

## Example Usage

```python
from bibas.heatmap_plot import plot_bibas_heatmap
plot_bibas_heatmap(model)