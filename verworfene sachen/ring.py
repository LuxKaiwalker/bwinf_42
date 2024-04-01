import numpy as np

def fill_outer_edges_with_zeros(array):
    if len(array.shape) != 2 or array.shape[0] != array.shape[1]:
        raise ValueError("Input must be a square 2D NumPy array")

    n = array.shape[0]
    result_array = np.copy(array)

    # Fill the outermost two edges with zeros
    result_array[:2, :] = 0  # Top two rows
    result_array[-2:, :] = 0  # Bottom two rows
    result_array[:, :2] = 0  # Leftmost two columns
    result_array[:, -2:] = 0  # Rightmost two columns

    return result_array

# Example usage:
original_array = np.full((7,7), 100)
modified_array = fill_outer_edges_with_zeros(original_array)

print("Original Array:")
print(original_array)
print("\nModified Array:")
print(modified_array)
