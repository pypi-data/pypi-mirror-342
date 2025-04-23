from setuptools import setup, find_packages

setup(
    name='zeropip',
    version='1.3.2',
    description='Minimal UI Framework for Text Tool in Colab (Single file)',
    author='dzbuit',
    packages=find_packages(),
    install_requires=['ipywidgets>=7.7.1'],
    include_package_data=True,
    zip_safe=False,
)
