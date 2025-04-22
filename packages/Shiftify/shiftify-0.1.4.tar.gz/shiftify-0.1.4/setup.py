from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Shiftify',
    version='0.1.4',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "ijson",
        "PyYAML>=6.0",
        "openpyxl",
        "toml",
    ],
    entry_points={
        'console_scripts': [
            'shiftify=shiftify.cli:main',
        ],
    },
    author='Abdul Rafey',
    author_email='abdulrafey38@gmail.com',
    description='A simple utility for converting formats to different and vice versa.',
    keywords='CSV, JSON, conversion, data transformation, file format, convert CSV to JSON, convert JSON to CSV, data interchange, CSV converter, JSON converter, data conversion, format switcher',
    url='http://github.com/abdulrafey38/shiftify'
)
