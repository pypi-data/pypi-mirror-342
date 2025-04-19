from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='grandprix',
    version='0.1.1',
    author='Idin K',
    author_email='python@idin.net',
    description='A Python package for Formula 1 data analysis and visualization.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/idin/grandprix',
    packages=find_packages(),
    license='CFL-1.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: Other/Proprietary License',
    ],
    python_requires='>=3.8',
    install_requires=[
        'pandas',
        'numpy',
    ],
) 