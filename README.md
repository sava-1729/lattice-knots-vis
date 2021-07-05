# BRIEF
Python programs to draw and visualize Lattice Knots and Links!

# DEPENDENCIES
1. matplotlib >= 3.3.4
2. vtk >= 9.0.2
3. mayavi >= 4.7.2

The programs have been tested on the versions of the dependencies listed above, however, it may run on lower versions too.

# INSTRUCTIONS
Modify the `DIRECTIONS` variable in the main.py file and run it in order to plot your knot.

If you are unable to install MayaVi, you can use main_matplotlib.py, which does not use the MayaVi library. However, the plots made using matplotlib seem to have an incorrect view order (some farther objects appear in front of nearer objects, and vice versa).
