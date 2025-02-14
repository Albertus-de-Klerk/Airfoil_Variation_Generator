import numpy as np
import pandas as pd

x_values = np.array([0.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

# Airfoil bounds
top_bounds = {
    0.0 (0.0, 0.0),
    0.0 (0.03, 0.04),
    0.1 (0.02, 0.10),
    0.2 (0.08, 0.12),
    0.3 (0.05, 0.15),
    0.4 (0.05, 0.15),
    0.5 (0.05, 0.15),
    0.6 (0.05, 0.12),
    0.7 (0.05, 0.15),
    0.8 (0.00, 0.03),
    0.9 (0.00, 0.02),
    1.0 (0.0, 0.0)
}

bottom_bounds = {
    0.0 (0.0, 0.0),
    0.0 (-0.04, 0.0),
    0.1 (-0.10, 0.0),
    0.2 (-0.12, 0.0),
    0.3 (-0.15, -0.04),
    0.4 (-0.15, 0.0),
    0.5 (-0.15, 0.0),
    0.6 (-0.12, 0.0),
    0.7 (-0.12, 0.0),
    0.8 (-0.03, 0.0),
    0.9 (-0.02, -0.10),
    1.0 (0.0, 0.0)
}

def generate_airfoil_variation()
    new_top_y = np.zeros_like(x_values)
    new_bottom_y = np.zeros_like(x_values)

    # Force firstlast points remain (0,0)
    new_top_y[0] = 0.0
    new_top_y[-1] = 0.0
    new_bottom_y[0] = 0.0
    new_bottom_y[-1] = 0.0

    # Randomly select parameters
    for i in range(1, len(x_values) - 1)
        new_top_y[i] = round(np.random.uniform(top_bounds[x_values[i]][0], top_bounds[x_values[i]][1]), 6)
        new_bottom_y[i] = round(np.random.uniform(bottom_bounds[x_values[i]][0], bottom_bounds[x_values[i]][1]), 6)

    return new_top_y, new_bottom_y

# Generate airfoil var correct coordinat points
airfoil_variations = []

# Num variations
num_variations = 10 

for _ in range(num_variations)
    top_var, bottom_var = generate_airfoil_variation()
    airfoil_variations.append({
        X x_values,
        Top Y top_var,
        Bottom Y bottom_var
    })

# Save correct data struct to .dat
file_path = airfoil_variations.dat

with open(file_path, 'w') as f
    f.write(Airfoil Variationsn)  # Header line
    for i in range(num_variations)
        f.write(fnVariation {i+1}n)  # Label for each variation
        for x, top_y, bottom_y in zip(x_values, airfoil_variations[i][Top Y], airfoil_variations[i][Bottom Y])
            f.write(f{x.6f} {top_y.6f} {bottom_y.6f}n)

# Verification of file
file_path