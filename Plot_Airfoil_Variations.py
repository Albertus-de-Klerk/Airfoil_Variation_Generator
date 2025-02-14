import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

# Airfoil variations .dat
airfoil_variations_file = "airfoil_variations.dat"

# Generate Bezier curve
def bezier_curve(control_points, n_points=100):
    n = len(control_points) - 1
    t = np.linspace(0, 1, n_points)
    curve = np.zeros((n_points, 2))
    for i in range(n + 1):
        bernstein_poly = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        curve[:, 0] += bernstein_poly * control_points[i, 0]
        curve[:, 1] += bernstein_poly * control_points[i, 1]
    return curve

# Read airfoil vars
with open(airfoil_variations_file, 'r') as f:
    lines = f.readlines()

variations = []
current_variation = []

for line in lines:
    if line.strip().startswith("Variation"):
        if current_variation:
            variations.append(np.array(current_variation, dtype=float))
            current_variation = []
    else:
        parts = line.strip().split()
        if len(parts) == 3:
            current_variation.append([float(parts[0]), float(parts[1]), float(parts[2])])

if current_variation:
    variations.append(np.array(current_variation, dtype=float))

# Plot fig
plt.figure(figsize=(10, 5))

for i, variation in enumerate(variations):
    # Extract control points
    x_values = variation[:, 0]
    top_control_points = np.column_stack((x_values, variation[:, 1]))
    bottom_control_points = np.column_stack((x_values, variation[:, 2]))

    # Generate Bezier curves
    top_curve = bezier_curve(top_control_points, n_points=200)
    bottom_curve = bezier_curve(bottom_control_points, n_points=200)

    # Calculate camber line and thickness
    camber_line = (top_curve[:, 1] + bottom_curve[:, 1]) / 2
    thickness = top_curve[:, 1] - bottom_curve[:, 1]

    # Plot B-curves and camber lines
    plt.plot(top_curve[:, 0], top_curve[:, 1], label=f'Upper Surface {i+1}', alpha=0.7)
    plt.plot(bottom_curve[:, 0], bottom_curve[:, 1], label=f'Lower Surface {i+1}', alpha=0.7)
    plt.plot(top_curve[:, 0], camber_line, linestyle='--', label=f'Camber Line {i+1}', alpha=0.7)

plt.title('Airfoil Variations - Bezier Curve Representation')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
