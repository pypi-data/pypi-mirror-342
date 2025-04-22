from setuptools import setup, find_packages

setup(
    name="gradient_descentbjk",
    version="0.1.0",
    description="A Python package implementing various gradient descent optimization algorithms",
    author="Jordan Buwa",
    author_email="jmbouobda@aimsammi.org",
    url="https://github.com/Jordan-buwa/gradient_descent",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
    keywords="machine learning, optimization, gradient descent, neural networks",
)