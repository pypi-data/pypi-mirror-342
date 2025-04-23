from setuptools import setup, find_packages

setup(
    name='zeropip',
    version='1.3.0',
    description='Lightweight UI Framework for Interactive Text Tools in Colab or Jupyter',
    author='dzbuit',
    packages=find_packages(),
    install_requires=[
        'ipywidgets>=7.7.1',
    ],
    include_package_data=True,
    zip_safe=False,
)
