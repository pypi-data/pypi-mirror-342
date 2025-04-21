from setuptools import setup, find_packages

setup(
    name='pupu',
    version='0.1.0',
    description='Package containing blue.py, green.py, and purple.py files',
    author='Amex005',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'pupu': ['blue.py', 'green.py', 'purple.py'],
    },
    install_requires=[
        'PySide6',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
