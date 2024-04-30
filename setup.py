from setuptools import setup, find_packages

setup(
    name='snap2luks',
    version='0.1.0',  # Add the version here
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snap2luks=snap2luks.main:main'
        ]
    },
    install_requires=[
        # Add your dependencies here
    ],
    python_requires='>=3.6',
)
