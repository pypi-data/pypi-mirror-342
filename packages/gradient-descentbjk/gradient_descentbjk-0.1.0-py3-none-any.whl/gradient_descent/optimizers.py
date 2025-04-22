"""
Gradient descent optimization algorithms.
"""

import numpy as np
from typing import Callable, Dict, Any, Optional, Tuple


class GradientDescent:
    """
    Standard (Batch) Gradient Descent optimizer.
    """
    
    def __init__(self, learning_rate: float = 0.01):
        """
        Initialize the gradient descent optimizer.
        
        Args:
            learning_rate: Step size for parameter updates
        """
        self.learning_rate = learning_rate
        self.iterations = 0
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters using gradients.
        
        Args:
            params: Current parameter values
            gradients: Computed gradients
            
        Returns:
            Updated parameters
        """
        self.iterations += 1
        return params - self.learning_rate * gradients
    
    def optimize(self, 
                objective_fn: Callable[[np.ndarray], float], 
                gradient_fn: Callable[[np.ndarray], np.ndarray],
                initial_params: np.ndarray,
                max_iterations: int = 1000,
                tolerance: float = 1e-6) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Optimize parameters to minimize the objective function.
        
        Args:
            objective_fn: Function to minimize
            gradient_fn: Function to compute gradients
            initial_params: Starting parameter values
            max_iterations: Maximum number of iterations
            tolerance: Convergence threshold for parameter changes
            
        Returns:
            Tuple of (optimized parameters, optimization history)
        """
        params = initial_params.copy()
        history = {
            'objective_values': [],
            'params_history': [],
            'gradients': []
        }
        
        for i in range(max_iterations):
            # Compute objective value and gradients
            objective_value = objective_fn(params)
            gradients = gradient_fn(params)
            
            # Store in history
            history['objective_values'].append(objective_value)
            history['params_history'].append(params.copy())
            history['gradients'].append(gradients.copy())
            
            # Update parameters
            new_params = self.update(params, gradients)
            
            # Check for convergence
            param_change = np.linalg.norm(new_params - params)
            params = new_params
            
            if param_change < tolerance:
                break
                
        return params, history


class StochasticGradientDescent(GradientDescent):
    """
    Stochastic Gradient Descent optimizer.
    """
    
    def __init__(self, learning_rate: float = 0.01, batch_size: int = 1):
        """
        Initialize the SGD optimizer.
        
        Args:
            learning_rate: Step size for parameter updates
            batch_size: Number of samples to use for each update
        """
        super().__init__(learning_rate)
        self.batch_size = batch_size


class MomentumGradientDescent(GradientDescent):
    """
    Gradient Descent with Momentum.
    """
    
    def __init__(self, learning_rate: float = 0.01, momentum: float = 0.9):
        """
        Initialize the momentum gradient descent optimizer.
        
        Args:
            learning_rate: Step size for parameter updates
            momentum: Momentum coefficient
        """
        super().__init__(learning_rate)
        self.momentum = momentum
        self.velocity = None
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters using gradients with momentum.
        
        Args:
            params: Current parameter values
            gradients: Computed gradients
            
        Returns:
            Updated parameters
        """
        self.iterations += 1
        
        if self.velocity is None:
            self.velocity = np.zeros_like(params)
            
        self.velocity = self.momentum * self.velocity - self.learning_rate * gradients
        return params + self.velocity


class AdaGrad(GradientDescent):
    """
    Adaptive Gradient Algorithm (AdaGrad).
    """
    
    def __init__(self, learning_rate: float = 0.01, epsilon: float = 1e-8):
        """
        Initialize the AdaGrad optimizer.
        
        Args:
            learning_rate: Step size for parameter updates
            epsilon: Small constant to avoid division by zero
        """
        super().__init__(learning_rate)
        self.epsilon = epsilon
        self.accumulated_squared_gradients = None
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters using AdaGrad.
        
        Args:
            params: Current parameter values
            gradients: Computed gradients
            
        Returns:
            Updated parameters
        """
        self.iterations += 1
        
        if self.accumulated_squared_gradients is None:
            self.accumulated_squared_gradients = np.zeros_like(params)
            
        self.accumulated_squared_gradients += np.square(gradients)
        
        adaptive_learning_rates = self.learning_rate / (np.sqrt(self.accumulated_squared_gradients) + self.epsilon)
        return params - adaptive_learning_rates * gradients


class RMSProp(GradientDescent):
    """
    Root Mean Square Propagation (RMSProp).
    """
    
    def __init__(self, learning_rate: float = 0.01, decay_rate: float = 0.9, epsilon: float = 1e-8):
        """
        Initialize the RMSProp optimizer.
        
        Args:
            learning_rate: Step size for parameter updates
            decay_rate: Decay rate for accumulated squared gradients
            epsilon: Small constant to avoid division by zero
        """
        super().__init__(learning_rate)
        self.decay_rate = decay_rate
        self.epsilon = epsilon
        self.accumulated_squared_gradients = None
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters using RMSProp.
        
        Args:
            params: Current parameter values
            gradients: Computed gradients
            
        Returns:
            Updated parameters
        """
        self.iterations += 1
        
        if self.accumulated_squared_gradients is None:
            self.accumulated_squared_gradients = np.zeros_like(params)
            
        self.accumulated_squared_gradients = (
            self.decay_rate * self.accumulated_squared_gradients + 
            (1 - self.decay_rate) * np.square(gradients)
        )
        
        adaptive_learning_rates = self.learning_rate / (np.sqrt(self.accumulated_squared_gradients) + self.epsilon)
        return params - adaptive_learning_rates * gradients


class Adam(GradientDescent):
    """
    Adaptive Moment Estimation (Adam).
    """
    
    def __init__(self, 
                learning_rate: float = 0.001, 
                beta1: float = 0.9, 
                beta2: float = 0.999, 
                epsilon: float = 1e-8):
        """
        Initialize the Adam optimizer.
        
        Args:
            learning_rate: Step size for parameter updates
            beta1: Exponential decay rate for first moment estimates
            beta2: Exponential decay rate for second moment estimates
            epsilon: Small constant to avoid division by zero
        """
        super().__init__(learning_rate)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None  # First moment estimate
        self.v = None  # Second moment estimate
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters using Adam.
        
        Args:
            params: Current parameter values
            gradients: Computed gradients
            
        Returns:
            Updated parameters
        """
        self.iterations += 1
        
        if self.m is None:
            self.m = np.zeros_like(params)
            self.v = np.zeros_like(params)
            
        # Update biased first moment estimate
        self.m = self.beta1 * self.m + (1 - self.beta1) * gradients
        
        # Update biased second raw moment estimate
        self.v = self.beta2 * self.v + (1 - self.beta2) * np.square(gradients)
        
        # Compute bias-corrected first moment estimate
        m_corrected = self.m / (1 - self.beta1 ** self.iterations)
        
        # Compute bias-corrected second raw moment estimate
        v_corrected = self.v / (1 - self.beta2 ** self.iterations)
        
        # Update parameters
        return params - self.learning_rate * m_corrected / (np.sqrt(v_corrected) + self.epsilon)