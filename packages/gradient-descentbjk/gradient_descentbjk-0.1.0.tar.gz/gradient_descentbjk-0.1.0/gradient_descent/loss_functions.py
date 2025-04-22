"""
Loss functions and their gradients for optimization.
"""

import numpy as np
from typing import Tuple


class LossFunction:
    """Base class for loss functions."""
    
    def __call__(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute the loss value.
        
        Args:
            y_true: Ground truth values
            y_pred: Predicted values
            
        Returns:
            Loss value
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def gradient(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of the loss with respect to y_pred.
        
        Args:
            y_true: Ground truth values
            y_pred: Predicted values
            
        Returns:
            Gradient of the loss
        """
        raise NotImplementedError("Subclasses must implement this method")


class MeanSquaredError(LossFunction):
    """Mean Squared Error loss function."""
    
    def __call__(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute the MSE loss.
        
        Args:
            y_true: Ground truth values
            y_pred: Predicted values
            
        Returns:
            MSE loss value
        """
        return np.mean(np.square(y_pred - y_true))
    
    def gradient(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of MSE.
        
        Args:
            y_true: Ground truth values
            y_pred: Predicted values
            
        Returns:
            Gradient of MSE with respect to y_pred
        """
        return 2 * (y_pred - y_true) / y_true.size


class BinaryCrossEntropy(LossFunction):
    """Binary Cross Entropy loss function."""
    
    def __init__(self, epsilon: float = 1e-15):
        """
        Initialize BCE loss.
        
        Args:
            epsilon: Small constant to avoid log(0)
        """
        self.epsilon = epsilon
    
    def __call__(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute the BCE loss.
        
        Args:
            y_true: Ground truth values (0 or 1)
            y_pred: Predicted probabilities
            
        Returns:
            BCE loss value
        """
        # Clip predictions to avoid log(0) or log(1)
        y_pred = np.clip(y_pred, self.epsilon, 1 - self.epsilon)
        
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    
    def gradient(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of BCE.
        
        Args:
            y_true: Ground truth values (0 or 1)
            y_pred: Predicted probabilities
            
        Returns:
            Gradient of BCE with respect to y_pred
        """
        # Clip predictions to avoid division by 0
        y_pred = np.clip(y_pred, self.epsilon, 1 - self.epsilon)
        
        return -(y_true / y_pred - (1 - y_true) / (1 - y_pred)) / y_true.size


class CategoricalCrossEntropy(LossFunction):
    """Categorical Cross Entropy loss function."""
    
    def __init__(self, epsilon: float = 1e-15):
        """
        Initialize CCE loss.
        
        Args:
            epsilon: Small constant to avoid log(0)
        """
        self.epsilon = epsilon
    
    def __call__(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Compute the CCE loss.
        
        Args:
            y_true: One-hot encoded ground truth values
            y_pred: Predicted probabilities
            
        Returns:
            CCE loss value
        """
        # Clip predictions to avoid log(0)
        y_pred = np.clip(y_pred, self.epsilon, 1.0)
        
        return -np.sum(y_true * np.log(y_pred)) / y_true.shape[0]
    
    def gradient(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of CCE.
        
        Args:
            y_true: One-hot encoded ground truth values
            y_pred: Predicted probabilities
            
        Returns:
            Gradient of CCE with respect to y_pred
        """
        # Clip predictions to avoid division by 0
        y_pred = np.clip(y_pred, self.epsilon, 1.0)
        
        return -y_true / y_pred / y_true.shape[0]