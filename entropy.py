import numpy as np


def calculate_entropy(probabilities):
    """Calculates the Shannon entropy of a probability distribution.

    Args:
      probabilities: A list or NumPy array of probabilities.

    Returns:
      The entropy of the distribution.
    """
    probabilities = np.array(probabilities)  # Ensure it's a NumPy array
    # Remove zero probabilities
    probabilities = probabilities[probabilities > 0]
    return -np.sum(probabilities * np.log2(probabilities))


# Example distributions:
dist1 = [0.96, 0.01, 0.01, 0.01, 0.01]  # Highly peaked
dist2 = [0.3, 0.3, 0.2, 0.1, 0.1]      # More balanced
dist3 = [0.2, 0.2, 0.2, 0.2, 0.2]      # Perfectly balanced (uniform)
dist4 = [0.5, 0.5, 0, 0, 0]           # two choices

print(f"Entropy of dist1: {calculate_entropy(dist1):.4f}")
print(f"Entropy of dist2: {calculate_entropy(dist2):.4f}")
print(f"Entropy of dist3: {calculate_entropy(dist3):.4f}")
print(f"Entropy of dist4: {calculate_entropy(dist4):.4f}")

# Maximum possible entropy for 5 choices:
max_entropy = calculate_entropy([0.2, 0.2, 0.2, 0.2, 0.2])
print(f"Maximum Entropy (5 choices): {max_entropy:.4f}")
