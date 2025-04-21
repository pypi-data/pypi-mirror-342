"""files related to visualization of style classifiers are moved here for consistency"""

# ========== NEWLY ADDED CODES BELOW ==========

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.manifold import TSNE

# from simsiam.models import SimSiam


# Function to calculate pairwise distances
def calculate_distances(embeddings):
    num_embeddings = embeddings.shape[0]
    distances = np.zeros((num_embeddings, num_embeddings))
    for i in range(num_embeddings):
        for j in range(num_embeddings):
            distances[i, j] = np.linalg.norm(embeddings[i] - embeddings[j])
    return distances


# Function to visualize embeddings using t-SNE


def visualize_embeddings_tsne(embeddings, image_paths, perplexity=2):
    tsne = TSNE(n_components=2, random_state=0, perplexity=perplexity)
    embeddings_2d = tsne.fit_transform(embeddings)

    plt.figure(figsize=(10, 10))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])

    for i, path in enumerate(image_paths):
        plt.annotate(os.path.basename(path), (embeddings_2d[i, 0], embeddings_2d[i, 1]))

    plt.title("t-SNE visualization of image embeddings")
    plt.show()


# Function to visualize pairwise distances


def visualize_distances(distances, image_paths):
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        distances,
        xticklabels=[os.path.basename(p) for p in image_paths],
        yticklabels=[os.path.basename(p) for p in image_paths],
        cmap="viridis",
        annot=True,
    )
    plt.title("Pairwise Distance Heatmap")
    plt.show()
