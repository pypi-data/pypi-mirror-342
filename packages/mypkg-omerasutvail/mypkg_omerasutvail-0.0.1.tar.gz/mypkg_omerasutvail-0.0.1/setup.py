from setuptools import setup, find_packages

setup(
    name='mypkg_omerasutvail',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],
    author='Bùi Phong Phú',
    author_email='omerasutvailworkit@gmail.com',
    description='A simple greeting package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
