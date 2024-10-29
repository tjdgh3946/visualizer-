import torch

# Define a tensor X with shape (32, 10, 128)
B, T, D = 32, 10, 128
X = torch.randn(B, T, D)  # Random values for testing

# Compute the pairwise distances between samples in X
dist_matrix = torch.cdist(X, X)

# Check the shape of the resulting distance matrix
print("Shape of X:", X.shape)
print("Shape of pairwise distance matrix:", dist_matrix.shape)
