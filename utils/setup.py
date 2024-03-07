from setuptools import setup, find_packages

setup(
    name='utils_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'diffusers==0.25.0',
        'Pillow==10.2.0',
        'torch==2.1.2',
    ],
    author='OneLeoTav',
    author_email='',
    description='Utility functions for image generation using text prompts',
)