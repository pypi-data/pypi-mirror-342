from setuptools import setup, find_packages

setup(
    name='zeropip',
    version='1.3.3',
    description='Lightweight UI Framework for Jupyter/Colab Text Apps',
    author='dzbuit',
    packages=find_packages(),
    install_requires=['ipywidgets'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)