import numpy as np
import h5py

def generate_measurements(emitter_position, poisson_mean, uncertainty_std):
    """
    Generates repeated measurements for each emitter, with uncertainty, optionally applying a membrane function.

    :param emitter_position: (ndarray) Emitter's true positions (N x 2 or N x 3).
    :param poisson_mean: (int) Poisson mean of the number of measurements around the emitter.
    :param uncertainty_std: (num) Standard deviation of the Gaussian uncertainty of the measurements.

    :return: (ndarray) Positional data of repeated measurements (M x 2 or M x 3).
    """
    emitter_position = np.atleast_2d(emitter_position)  # Ensure input is at least 2D
    new_emits = []

    for pos in emitter_position:
        # Generate random offsets
        num_measurements = np.random.poisson(poisson_mean)
        offsets = np.random.normal(loc=0, scale=uncertainty_std, size=(num_measurements, 2))
        measurements = pos + offsets
        new_emits.extend(measurements)

    return np.array(new_emits)


def gen_noise(xrange, yrange, rho, measured=5, ms_uncertainty=0.5):
    """
    Generate clutter / spurious measurements across a window.

    :param xrange: (tuple) Specifies xrange of window.
    :param yrange: (tuple) Specifies yrange of window.
    :param rho: (num) Noise density; dictates number of clusters of spurious measurements.
    :param measured: (int) Poisson mean of measurements assigned to each cluster.
    :param ms_uncertainty: (num) Uncertainty of measurements around the dictated point.

    :return: (ndarray) Positional data of spurious measurements across the window.
    """
    n_noise_emitters = np.random.poisson(rho)
    x_noise = np.random.uniform(xrange[0], xrange[1], n_noise_emitters)
    y_noise = np.random.uniform(yrange[0], yrange[1], n_noise_emitters)
    noise = np.column_stack((x_noise, y_noise))
    clutter = []
    for point in noise:
        measurements = generate_measurements(point, poisson_mean=measured, uncertainty_std=ms_uncertainty)
        for measurement in measurements:
            clutter.append((measurement[0], measurement[1], -1))  # ID is always -1 for clutter
    return np.array(clutter)


def apply_membrane(data, membrane_function):
    """
    Applies the membrane function or adds a z=0 coordinate at the dataset level.

    :param data: 2D input data for membrane conversion. Should be an Nx2 array.
    :param membrane_function: Function that dictates the axial values. If not present, all zeros.

    :return: Nx3 array with an additional z-coordinate.
    """
    data = np.atleast_2d(data)  # Ensure 2D format

    if membrane_function:
        x, y = data[:, 0], data[:, 1]
        z = np.array(membrane_function(x, y))  # Ensure output is an array of the same length
        if z.shape[0] != data.shape[0]:  # Ensure shape consistency
            raise ValueError(
                f"Membrane function output shape {z.shape} does not match input data shape {data.shape[0]}")
    else:
        z = np.zeros(data.shape[0])  # Default to z=0 for all

    return np.column_stack((data, z))



def dist_custom(filename, centroids, p, q, radius, structures, abundances, gt_uncertainty=0,
                measured=7, ms_uncertainty=0.05, noise_params=None, membrane_function=None):
    """
    Distributes emitters around centroids, and measurements around these emitters. Generates clutter/spurious
    measurements. Converts emitters, measurements, and clutter to 3D, mimicking a cell membrane. Fully connects emitters
    around the same centroid. Saves emitters, measurements, clutter, and edges to HDF5.

    :param filename: (str) Name of the saved HDF5 file.
    :param centroids: (ndarray) Centroids that dictate structure location.
    :param p: (num) Probability of effective biolabelling.
    :param q: (num) Probability of detecting a signal from a measurement.
    :param radius: (num) Radius of the structure. Keep consistent with radius at centroid generation stage.
    :param structures: (list) Structures to be distributed. Result of structure parsing.
    :param abundances: (ndarray) Relative abundances of each structures presence. Result of structure parsing.
    :param gt_uncertainty: (num) Gaussian uncertainty of ground truth positioning.
    :param measured: (int) Poisson mean of measurements around labelled emitters.
    :param ms_uncertainty: (num) Uncertainty of measurement positioning as a function of the radius of the structure.
    :param noise_params: (tuple) Parameters to generate noise. Form (xrange, yrange, noise_density). Default None.
    :param membrane_function: (func) Function to convert 2D generated data to 3D. Default z=0 in absence of function.

    :return:{ (h5) File containing emitters, measurements, clutter, and edges fully connecting structures. Stored in HDF5
    format; emitters have type b'labelled' or b'unlabelled', measurements are linked with parent emitters via emitter
    ID's, and distinct structures are fully connected via edges defined in terms of emitter ID's. All clutter has an
    emitter ID of -1, and type b'clutter'.}
    """
    observed_data, edges, emitter_data = [], [], []
    emitter_index = 0

    abundances = np.array(abundances) / np.sum(abundances)

    if not structures or len(structures) == 0:
        raise ValueError("Structures list is empty or None.")
    if abundances is None or len(abundances) == 0:
        raise ValueError("Abundances list is empty or None.")
    if len(structures) != len(abundances):
        raise ValueError("Number of structures and abundances must match.")

    for centroid in centroids:
        structure_idx = np.random.choice(len(structures), p=abundances)
        structure = radius * structures[structure_idx]

        angle = np.random.uniform(0, 2 * np.pi)
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]])

        rotated_structure = (structure @ rotation_matrix.T) + centroid
        emitter_indices = []

        for point in rotated_structure:
            corrected_point = np.random.normal(loc=point, scale=gt_uncertainty)
            emitter_type = "labelled" if np.random.binomial(1, p) else "unlabelled"

            emitter_data.append((corrected_point[0], corrected_point[1], emitter_index, emitter_type))
            emitter_indices.append(emitter_index)
            emitter_index += 1

            if emitter_type == "labelled":
                measurements = generate_measurements(corrected_point, poisson_mean=measured,
                                                     uncertainty_std=ms_uncertainty * radius)
                for measurement in measurements:
                    if np.random.binomial(1, q):
                        observed_data.append((measurement[0], measurement[1], emitter_indices[-1]))

        # Store fully connected edges in structures for ground truth graphing
        for i in range(len(emitter_indices)):
            for j in range(i + 1, len(emitter_indices)):
                edges.append((emitter_indices[i], emitter_indices[j]))

    # Generate clutter data
    clutter_data = []
    if noise_params:
        xrange, yrange, rho= noise_params
        clutter_data = gen_noise(xrange, yrange, rho, measured, ms_uncertainty*radius)

    # Create emitter_pos, observed_pos, clutter_pos arrays for easier 3d processing
    emitter_pos = np.array([[e[0], e[1]] for e in emitter_data])
    observed_pos = np.array([[o[0], o[1]]for o in observed_data])
    clutter_pos = np.array([[c[0], c[1]] for c in clutter_data])

    data_dict = {
        "emitter_pos": emitter_pos,
        "observed_pos": observed_pos,
        "clutter_pos": clutter_pos
    }

    for key, data in data_dict.items():
        data_dict[key] = apply_membrane(data, membrane_function)

    emitter_pos, observed_pos, clutter_pos = data_dict.values()

    print("Data Before Saving:")
    print("Emitter Data:", type(emitter_pos), "Shape:", emitter_pos.shape)
    print("Observed Data:", type(observed_pos), "Shape:", observed_pos.shape)
    print("Clutter Data:", type(clutter_pos), "Shape:", clutter_pos.shape)
    print("Edges:", type(edges), "Length:", len(edges))

    # Save data to HDF5 file
    with h5py.File(filename, 'w') as hf:
        emitter_group = hf.create_group('emitter')
        emitter_group.create_dataset('id', data=np.array([e[2] for e in emitter_data], dtype=np.int32))
        emitter_group.create_dataset('position', data=np.array([[e[0], e[1], e[2]] for e in emitter_pos]))
        emitter_group.create_dataset('type', data=np.array([e[3] for e in emitter_data], dtype='S'))

        if observed_data:
            observed_group = hf.create_group('observed')
            observed_group.create_dataset('position', data=np.array([[o[0], o[1], o[2]] for o in observed_pos]))
            observed_group.create_dataset('emitter_id', data=np.array([o[2] for o in observed_data], dtype=np.int32))

        clutter_group = hf.create_group('clutter')
        clutter_group.create_dataset('position', data=np.array([[c[0], c[1], c[2]] for c in clutter_pos]))
        clutter_group.create_dataset('emitter_id', data=np.array([c[2] for c in clutter_data], dtype=np.int32))
        clutter_group.create_dataset('type', data=np.array(['clutter'] * len(clutter_data), dtype='S'))

        hf.create_dataset('edges', data=np.array(edges, dtype=np.int32))