import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

try:
    project_dir = Path(__file__).resolve().parents[1]
except NameError:
    project_dir = Path(os.getcwd()).resolve
sys.path.insert(0, str(project_dir))

print('aqui: \n', project_dir, '\n')


def read_requirements():
    try:
        with open('requirements.txt', 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'requirements.txt'.")
        return []

setup(name='datupapi',
      version='1.107.2-rc9',
      description='Utility library to support Datup AI MLOps processes',
      long_description_content_type="text/markdown",
      long_description="foo bar baz",
      author='Datup AI',
      author_email='ramiro@datup.ai',
      packages=[
          'datupapi',
          'datupapi.transform',
          'datupapi.configure',
          'datupapi.extract',
          'datupapi.prepare',
          'datupapi.feateng',
          'datupapi.inventory',
          'datupapi.inventory.src.DailyUsage',
          'datupapi.inventory.src.Format',
          'datupapi.inventory.src.FutureInventory',
          'datupapi.inventory.src.InventoryFunctions',
          'datupapi.inventory.src.ProcessForecast', 
          'datupapi.inventory.src.SuggestedForecast',          
          'datupapi.inventory.src.Transformation',
          'datupapi.inventory.conf',
          'datupapi.distribution',
          'datupapi.distribution.src.DistributionFunctions',
          'datupapi.distribution.src.Format',
          'datupapi.distribution.conf',
          'datupapi.training',
          'datupapi.evaluate',
          'datupapi.predict',
          'datupapi.utils'
          
      ],
      install_requires=read_requirements(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.10.5',
      )

