# BRIEF
Python module to visualize Lattice Knots and Links in 3D, and analyse their distortion.

# PREVIEW
High Distortion vertices of the Minimal Stick Trefoil (25x)
![alt text](https://github.com/sava-1729/lattice-knots-vis/blob/main/img/taxicab_distortion_preview.png?raw=true)

# DEPENDENCIES
1. numpy >= 1.21.0
2. matplotlib >= 3.3.4
3. vtk >= 9.0.2
4. mayavi >= 4.7.2

The programs have been tested on the versions of the dependencies listed above, however, it may run on lower versions too.

# INSTRUCTIONS TO INSTALL DEPENDENCIES
1. Install Miniconda (preferred) with Python 3.7
https://docs.conda.io/en/latest/miniconda.html
2. Install numpy
conda install -c anaconda numpy
3. Install matplotlib
conda install -c conda-forge matplotlib 
4. Install vtk
conda install -c conda-forge vtk
5. Install mayavi
conda install -c conda-forge mayavi

# INSTRUCTIONS TO RUN THE CODE
1. Modify the `DIRECTIONS` variable in the main.py file
2. Comment out the other definitions of the `DIRECTIONS` variable
3. Run `main.py` inside anaconda prompt in order to draw your knot.
