"""
Utility functions for gradient descent.
"""

import numpy as np
from typing import Callable, Tuple, List, Dict, Any, Optional
import matplotlib.pyplot as plt


def numerical_gradient(func: Callable[[np.ndarray], float], 
                      x: np.ndarray, 
                      epsilon: float = 1e-7) -> np.ndarray:
    """
    Compute numerical gradient using central difference method.
    
    Args:
        func: Function to differentiate
        x: Point at which to compute gradient
        epsilon: Small perturbation
        
    Returns:
        Gradient vector
    """
    grad = np.zeros_like(x)
    
    # Iterate through each dimension
    for i in range(x.size):
        # Create perturbation vector
        h = np.zeros_like(x)
        h[i] = epsilon
        
        # Central difference
        grad[i] = (func(x + h) - func(x - h)) / (2 * epsilon)
        
    return grad


def plot_contour(func: Callable[[np.ndarray], float], 
                x_range: Tuple[float, float], 
                y_range: Tuple[float, float],
                optimization_path: Optional[List[np.ndarray]] = None,
                resolution: int = 100,
                levels: int = 50,
                title: str = "Optimization Path",
                save_path: Optional[str] = None) -> None:
    """
    Plot contour of a 2D function with optional optimization path.
    
    Args:
        func: 2D function to plot
        x_range: Range for x-axis (min, max)
        y_range: Range for y-axis (min, max)
        optimization_path: List of parameter values during optimization
        resolution: Number of points in each dimension
        levels: Number of contour levels
        title: Plot title
        save_path: Path to save the figure (if None, figure is displayed)
    """
    # Create grid
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    
    # Compute function values
    Z = np.zeros_like(X)
    for i in range(resolution):
        for j in range(resolution):
            Z[i, j] = func(np.array([X[i, j], Y[i, j]]))
    
    # Create plot
    plt.figure(figsize=(10, 8))
    contour = plt.contour(X, Y, Z, levels=levels, cmap='viridis')
    plt.colorbar(contour, label='Function Value')
    
    # Plot optimization path if provided
    if optimization_path is not None and len(optimization_path) > 0:
        path = np.array(optimization_path)
        plt.plot(path[:, 0], path[:, 1], 'ro-', linewidth=2, markersize=8)
        plt.plot(path[0, 0], path[0, 1], 'go', markersize=10, label='Start')
        plt.plot(path[-1, 0], path[-1, 1], 'bo', markersize=10, label='End')
    
    plt.xlabel('Parameter 1')
    plt.ylabel('Parameter 2')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


def plot_loss_history(history: Dict[str, Any], 
                     title: str = "Loss History",
                     save_path: Optional[str] = None) -> None:
    """
    Plot loss history during optimization.
    
    Args:
        history: Optimization history dictionary with 'objective_values' key
        title: Plot title
        save_path: Path to save the figure (if None, figure is displayed)
    """
    plt.figure(figsize=(10, 6))
    plt.plot(history['objective_values'], 'b-', linewidth=2)
    plt.xlabel('Iteration')
    plt.ylabel('Loss Value')
    plt.title(title)
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


def create_minibatches(X: np.ndarray, 
                      y: np.ndarray, 
                      batch_size: int, 
                      shuffle: bool = True) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Create minibatches from data.
    
    Args:
        X: Input features
        y: Target values
        batch_size: Size of each batch
        shuffle: Whether to shuffle data before creating batches
        
    Returns:
        List of (X_batch, y_batch) tuples
    """
    assert X.shape[0] == y.shape[0], "X and y must have the same number of samples"
    
    n_samples = X.shape[0]
    indices = np.arange(n_samples)
    
    if shuffle:
        np.random.shuffle(indices)
    
    # Create batch indices
    batch_indices = [
        indices[i:min(i + batch_size, n_samples)]
        for i in range(0, n_samples, batch_size)
    ]
    
    # Create batches
    minibatches = [
        (X[batch_idx], y[batch_idx])
        for batch_idx in batch_indices
    ]
    
    return minibatches