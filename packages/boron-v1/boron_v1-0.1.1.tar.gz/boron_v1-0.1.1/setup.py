from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='boron-v1',
    version='0.1.1',
    author='Harsith S',
    author_email='boron.version.1@gmail.com',  
    description='Link programming languages effortlessly using Boron (.bn) files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    package_data={
        'boron': ['c_lib.dll'],  
    },
    entry_points={
        'console_scripts': [
            'boron=boron.builder:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
