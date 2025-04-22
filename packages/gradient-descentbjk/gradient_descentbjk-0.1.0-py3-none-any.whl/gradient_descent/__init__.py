"""
Gradient Descent Package

A package for implementing various gradient descent optimization algorithms.
"""

from .optimizers import GradientDescent, StochasticGradientDescent, MomentumGradientDescent, AdaGrad, RMSProp, Adam
from .loss_functions import MeanSquaredError, BinaryCrossEntropy, CategoricalCrossEntropy

__version__ = '0.1.0'