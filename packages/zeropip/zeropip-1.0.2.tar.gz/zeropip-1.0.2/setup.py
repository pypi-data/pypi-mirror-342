from setuptools import setup, find_packages

setup(
    name='zeropip',
    version='1.0.2',
    packages=find_packages(include=["zeropip", "zeropip.*"]),
    install_requires=[
        'ipywidgets',
        'langdetect'
    ],
    description='Zero-loading, zero-server, Colab-optimized UI for text-based AI tools.',
    author='Zeropip Contributors',
    url='https://github.com/dzbuit/zeropip',
    license='MIT'
)