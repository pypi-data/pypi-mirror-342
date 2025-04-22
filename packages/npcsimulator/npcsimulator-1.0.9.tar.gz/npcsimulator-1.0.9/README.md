# **NPCSimulator**  
This project is a Python-based simulator for simulating data like that resulting from MINFLUX imaging.
In short, emitter structures are generated around centroids, and random repeated measurements are generated around these emitters. Noise / clutter is generated throughout the ROI.
Also featured are functions to convert the generated data to 3D through applying a user specified membrane function, and functions to both plot and save the resulting data.
A command line implementation is also included to streamline user workflow, with some examples included here.

---

## **Table of Contents**  
1. [Features](#features)  
2. [Installation](#installation)  
3. [Usage](#usage)  
    - [Basic Usage](#basic-usage)  
    - [Input Arguments](#input-arguments)  
4. [CLI Examples](#examples)  
5. [Licence](#licence)  

---

## **Features**  
- **Centroid Generation**: Generate centroids using a Poisson process or read from a CSV file.  
- **Structure Parsing**: Define custom structures or use preset configurations (e.g., dimers, polygons).  
- **Distribute Emitters**: Distribute emitters in the defined structures.
- **Simulation of Measurements**: Model labelled emitters with probabilities of fluorescence and ground-truth uncertainty. Distribute random, repeated measurements around these labelled emitters.
- **Noise Simulation**: Add random noise emitters to the simulation.  
- **Custom Membrane Function**: Load user-defined membrane functions to map data into 3D.  
- **Data Export**: Save simulation results to CSV or HDF5 files.  
- **3D Visualization**: Plot emitters, centroids, measurements, and noise in a 3D space.  

---

## **Installation**  
Install NPCSimulator using pip:

```bash
pip install npcsimulator
```
or if preferred, install from the source distribution:
```bash
git clone https://github.com/j-peyton/NPCPackage.git
cd .../npcsimulator
```

---


## **Usage**
**Basic Usage**

Following installation, import and run functions directly in your IDE:

```python
from npcsimulator.centroids import generate_centroids

xrange = (-100, 100)
yrange = (-100, 100)
poisson_mean = 25
radius = 5
centroids_data = generate_centroids(xrange, yrange, poisson_mean, radius)
...
```

**CLI Usage & Input Variables**

## Table of Input Variables

Here’s a detailed overview of the CLI arguments available for your application:

| Argument            | Type    | nargs  | Default         | Description |
|---------------------|---------|--------|-----------------|--------------|
| `--xrange`          | `float` | `nargs` | `[ -50, 50 ]`   | X coordinate range for centroids |
| `--yrange`          | `float` | `nargs` | `[ -50, 50 ]`   | Y coordinate range for centroids |
| `--poisson_mean`    | `int`   |        | `15`            | Generates centroids via Poisson distribution defined by this variable |
| `--centroids`       | `str`   |        | `None`          | Path to a CSV file containing centroids |
| `--radius`          | `float` |        | `5.0`           | Centroid/emitter structure radius |
| `--Pe`              | `float` |        | `0.80`          | Probability of successful labelling |
| `--Pf`              | `float` |        | `0.80`          | Probability of fluorescence / signal received |
| `--gt_uncertainty`  | `float` |        | `0.1`           | Uncertainty of the position of the ground truth emitter |
| `--measured`        | `int`   |        | `5`             | Poisson mean of the number of measurements per emitter |
| `--ms_uncertainty`  | `float` |        | `0.05`          | Uncertainty of repeated measurements around an emitter as a percentage of the radius of the structure |
| `--noise`           | `float` |        | `0.0`           | Average number of noise emitters per unit area |
| `--output`          | `str`   |        | `None`          | Output file name with `.csv` or `.h5` extension |
| `--x_structures`    | `float` | `nargs` | `None`          | List of x coordinates for each structure. Specify multiple structures as separate lists. E.g. `--x_structures 2 4 5 6 --x_structures 4 9 1 4` |
| `--y_structures`    | `float` | `nargs` | `None`          | List of y coordinates for each structure. Specify multiple structures as separate lists. E.g. `--y_structures 1 3 5 7 --x_structures 2 5 3 8` |
| `--structure_abundances` | `float` | `nargs` |                 | Abundance values for each structure. E.g. `--structure_abundance 0.8 0.2` |
| `--preset_structures` | `nargs` | `choices` | `None`           | Preset structure to use in emitter distribution |
| `--preset_sides`    | `int`   | `nargs` | `[3,4,5,6,7,8]` | List of side counts for preset polygons |
| `--membrane`        | `str`   |        |                 | Filepath to the custom membrane function. Store membrane function in its own isolated .py file |


## Command-Line Usage Examples

The `NPCSimulator` comes with a command-line interface (CLI) tool for simulating emitter distributions. Below are some examples to get started.

### Example 1: Generate Centroids Using Default Parameters
To generate centroids with default parameters and visualize the results:

```bash
python npcsimulator/CLI.py
```

Each variable can be called as the above table specifies. For example, a data set of entirely pentagonal structures with a small amount of noise can be generated via:

```bash
python npcsimulator/CLI.py --preset_structures polygon --preset_sides 5 
--structure_abundances 1 --noise 0.005 --output pent.csv
```

## License

This project is licensed under the MIT License. 

You are free to use, modify, and distribute this software under the terms of the MIT License. See the [LICENCE](./LICENCE) file for details.

