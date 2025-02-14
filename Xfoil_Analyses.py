# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb
import jxfoil
import os

# XFOIL parameters
rho = 1.225
mu = 1.789e-5
V_inf = 60  # [m/s]
alpha = 5   # [deg]
Flap = 5
Re = rho * V_inf * 1 / mu

# Number of points to extract from Bezier curves
num_points = 100

# File names
airfoil_variations_file = "airfoil_variations.dat"
results_file = "xfoil_results.dat"

# Function to generate Bezier curve from control points
def bezier_curve(control_points, n_points=100):
    n = len(control_points) - 1
    t = np.linspace(0, 1, n_points)
    curve = np.zeros((n_points, 2))
    for i in range(n + 1):
        bernstein_poly = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        curve[:, 0] += bernstein_poly * control_points[i, 0]
        curve[:, 1] += bernstein_poly * control_points[i, 1]
    return curve

# Read airfoil variations from file
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

import os
from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
# Process each variation
with open(results_file, 'a') as result_file:  # Append to results file
    result_file.write("AOA  Cd\n")

    for i, variation in enumerate(variations):
        print(f"Processing Variation {i+1}...")

        # Extract control points
        x_values = variation[:, 0]
        top_control_points = np.column_stack((x_values, variation[:, 1]))
        bottom_control_points = np.column_stack((x_values, variation[:, 2]))

        # Generate Bezier curves
        top_curve = bezier_curve(top_control_points, n_points=200)
        bottom_curve = bezier_curve(bottom_control_points, n_points=200)

        # Sort and sample num_points from Bezier curve
        top_curve = top_curve[np.argsort(-top_curve[:, 0])]
        bottom_curve = bottom_curve[np.argsort(bottom_curve[:, 0])]

        top_curve_sampled = top_curve[np.linspace(0, len(top_curve) - 1, num_points, dtype=int)]
        bottom_curve_sampled = bottom_curve[np.linspace(0, len(bottom_curve) - 1, num_points, dtype=int)]

        # Construct ordered coordinates for XFOIL
        airfoil_coordinates = np.vstack((top_curve_sampled, bottom_curve_sampled[1:]))
        #airfoil_coordinates = airfoil_coordinates[:len(airfoil_coordinates)-1] 
        
        testfoil_file = f"testfoil{i+1}.txt"

        with open(testfoil_file, 'w') as f:
            f.write(f"testfoil{i+1}\n")
            for x, y in airfoil_coordinates:
                f.write(f"{x:.6f} {y:.6f}\n")

        # Call XFOIL for this variation

        AOA, Cd, Cm, v = jxfoil.CallXfoilcl(1.2, Re, f"testfoil{i+1}.txt", Flap, 0, 0)
        result_file.write(f"{AOA:.6f}  {Cd:.6f}\n")

print("XFOIL analysis complete. Results saved to xfoil_results.dat.")

