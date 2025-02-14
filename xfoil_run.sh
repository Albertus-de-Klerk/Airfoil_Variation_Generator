#!/bin/bash

# Check for required arguments
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <airfoil> <Re> <Cl>"
    exit 1
fi

AIRFOIL=$1        # Airfoil name (NACAxxxx or .dat file)
REYNOLDS=$2       # Reynolds number
TARGET_CL=$3      # Target lift coefficient
TEMP_OUTPUT=$(mktemp)  # Temporary results file

# Run XFOIL with structured input
xfoil <<EOF
LOAD $AIRFOIL
PANE
PLOP
G

OPER
VISC $REYNOLDS
ITER 200
PACC
xfoil_polar.dat
y  # Asswer 'y' to the "Rewrite Polar file" propmt

CL $TARGET_CL
PACC  # Stop polar accumulation
EOF

AOA=$(grep -oP 'alpha =\s+\K[-0-9.]+' xfoil_polar.dat)
CD=$(grep -oP 'CD =\s+\K[-0-9.]+' xfoil_polar.dat)


# Print results for Python to parse
echo "$AOA $CD"
