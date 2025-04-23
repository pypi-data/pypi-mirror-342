from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='il4pred2',
    version='1.0',
    description='A tool to predict il4-inducing peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/il4pred2', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={
        "il4pred2.model": ["*"],  # Include everything in Model/
        "il4pred2.Feature": ["*.csv"],  # Include specific file types in Data/
        "il4pred2.pfeature_standalone": ["*"],  # Include everything in Resources/
    },
    entry_points={ 'console_scripts' : ['il4pred2 = il4pred2.Python_scripts.il4pred2:main']},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'pandas', 'numpy', 'scikit-learn == 1.2.1'# Add any Python dependencies here
    ]
)
