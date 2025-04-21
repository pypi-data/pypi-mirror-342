from setuptools import setup, find_packages

setup(
    name='hyperparameter-optimizer',
    version='0.1.1',
    description='A lightweight Python library for hyperparameter tuning using Metaheuristic algorithms.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dr. Ahmed Moussa',
    author_email='ahmedyosrihamdy@gmail.com',
    url='https://github.com/real-ahmed-moussa/hyperparameter-optimizer',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.7',
)
