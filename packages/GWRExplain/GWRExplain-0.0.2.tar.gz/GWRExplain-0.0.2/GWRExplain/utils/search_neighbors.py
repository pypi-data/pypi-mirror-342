import numpy as np
from sklearn.neighbors import NearestNeighbors
from typing import Tuple, Union, List


def get_neighbors(
    coords: Union[np.ndarray, List[List[float]]],
    n_neighbors: int = None,
    distance: float = None,
    mode: str = 'distance',
    spherical: bool = False
) -> Tuple[Union[np.ndarray, List[np.ndarray]], Union[np.ndarray, List[np.ndarray]]]:
    """
    Get neighborhood relationships for geographic coordinates, either based on distance or fixed number of neighbors.

    Parameters
    ----------
    coords : array-like of shape (n_samples, 2)
        Input coordinates. If spherical=True, the format should be [latitude, longitude] in degrees.
    n_neighbors : int, optional
        Number of nearest neighbors. Used only when mode='adaptive'.
    distance : float, optional
        Neighborhood radius. Used only when mode='distance'. Unit is kilometers if spherical=True.
    mode : {'distance', 'adaptive'}
        Neighbor calculation mode: 'distance' for fixed radius, 'adaptive' for fixed number of neighbors.
    spherical : bool
        Whether to use spherical (Haversine) distance. Input coordinates should be in latitude and longitude if True.

    Returns
    -------
    distances : array or list of arrays
        Distances to neighbors (shape depends on the mode).
    indices : array or list of arrays
        Indices of neighbors.
    """
    
    coords = np.asarray(coords)

    if mode not in ['distance', 'adaptive']:
        raise ValueError("mode must be either 'distance' or 'adaptive'")

    if mode == 'adaptive' and n_neighbors is None:
        raise ValueError("n_neighbors must be set for adaptive mode")
    if mode == 'distance' and distance is None:
        raise ValueError("distance must be set for distance mode")

    if spherical:
        coords_rad = np.radians(coords)
        metric = 'haversine'
        radius = distance / 6371.0 if distance else None  # km → radians
        algorithm = 'ball_tree'
    else:
        coords_rad = coords
        metric = 'euclidean'
        radius = distance
        algorithm = 'kd_tree'

    if mode == 'adaptive':
        nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm=algorithm, metric=metric)
        nbrs.fit(coords_rad)
        distances, indices = nbrs.kneighbors(coords_rad)
        if spherical:
            distances *= 6371.0  # radians → km
    else:
        nbrs = NearestNeighbors(radius=radius, algorithm=algorithm, metric=metric)
        nbrs.fit(coords_rad)
        distances, indices = nbrs.radius_neighbors(coords_rad, return_distance=True)
        if spherical:
            distances = [d * 6371.0 for d in distances]  # radians → km

    return distances, indices

