# TSNE-PSO

t-Distributed Stochastic Neighbor Embedding with Particle Swarm Optimization (TSNE-PSO) is an enhanced version of t-SNE that uses Particle Swarm Optimization instead of gradient descent for the optimization step.

## Installation

```bash
pip install tsne-pso
```

## Usage

```python
from tsne_pso import TSNEPSO
import numpy as np
from sklearn.datasets import load_iris

# Load data
iris = load_iris()
X = iris.data

# Apply TSNE-PSO
tsne_pso = TSNEPSO(
    n_components=2,
    perplexity=30.0,
    n_particles=10,
    n_iter=500,
    random_state=42
)
X_embedded = tsne_pso.fit_transform(X)

# Visualize results
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 8))
scatter = plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=iris.target)
plt.legend(handles=scatter.legend_elements()[0], labels=iris.target_names)
plt.title('TSNE-PSO visualization of Iris dataset')
plt.show()
```

## Features

- Uses Particle Swarm Optimization for better optimization
- Supports multiple initialization strategies (PCA, UMAP, t-SNE)
- Optional hybrid approach using both PSO and gradient descent
- Customizable parameters for optimization (particles, inertia, cognitive/social weights)

## Dependencies

- numpy
- scipy
- scikit-learn
- umap-learn (optional)
- tqdm (optional, for progress bars)

## License

BSD-3-Clause License (same as scikit-learn) 