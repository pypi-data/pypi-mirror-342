import numpy as np
from typing import Union, List, Tuple


class Trajectory:
    """A data class for storing robot arm trajectories with times and joint points.

    This class stores a trajectory as separate arrays for times and joint points. Times are stored
    as a 1D array, and points as a 2D array where each row corresponds to a time point and each
    column to a joint.

    Attributes:
        times (np.ndarray): 1D array of time points.
        points (np.ndarray): 2D array of joint points with the shape of (num_points, num_joints).

    Args:
        points (Union[np.ndarray, List[List[float]], List[Tuple[float]]]): Joint points
            corresponding to each time point.
        times (Union[np.ndarray, List[float], Tuple[float]]): Time points for the trajectory.
        sort (bool, optional): If True, sorts the trajectory by time. Defaults to False.

    Raises:
        ValueError: If inputs are invalid (e.g., mismatched lengths, fewer than one joint, NaN/Inf).
    """

    def __init__(
        self,
        points: Union[np.ndarray, List[List[float]], List[Tuple[float]]],
        times: Union[np.ndarray, List[float], Tuple[float]],
        sort: bool = True,
    ):
        # Convert inputs to NumPy arrays
        self.times = np.asarray(times, dtype=np.float64)
        self.points = np.asarray(points, dtype=np.float64)

        # Validate inputs
        if self.times.ndim != 1:
            raise ValueError("Times must be a 1D array")
        if self.points.ndim != 2:
            raise ValueError("points must be a 2D array")
        if self.times.shape[0] != self.points.shape[0]:
            raise ValueError("Number of time points must match number of position rows")
        if self.points.shape[1] < 1:
            raise ValueError("At least one joint is required")
        if np.any(np.isnan(self.times)) or np.any(np.isinf(self.times)):
            raise ValueError("Times contain NaN or Inf values")
        if np.any(np.isnan(self.points)) or np.any(np.isinf(self.points)):
            raise ValueError("points contain NaN or Inf values")

        # Sort by time by default
        if sort:
            sorted_indices = np.argsort(self.times)
            self.times = self.times[sorted_indices]
            self.points = self.points[sorted_indices]

    @property
    def size(self) -> int:
        """Returns the number of time points in the trajectory."""
        return self.times.size

    def copy(self) -> "Trajectory":
        """Returns a deep copy of the Trajectory."""
        return Trajectory(self.times.copy(), self.points.copy())

    def sort_by_time(self) -> "Trajectory":
        """Returns a new Trajectory sorted by time."""
        return Trajectory(self.times, self.points, sort=True)

    def __str__(self) -> str:
        return f"Trajectory(times={self.times}, points={self.points})"

    def __repr__(self) -> str:
        return f"Trajectory(times={self.times!r}, points={self.points!r})"

    def __len__(self) -> int:
        return len(self.times)
