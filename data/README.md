# Introduction 
This repository contains scripts for downloading pitch data from MLB StatsAPI.

# Getting Started
0. If possible, install 'pipenv'. It'd make things smoother.
   - if not using pipenv, the scripts expect the following prerequisites.
     - python 3.7
     - request
     - pandas
1. Set up a python environment.
  ```
  pipenv install
  ```
2. Enter the python environment.
  ```
  pipenv shell
  ```
3. Download all the pitches from the MLB games in October 2019, for example,
  ```
  python ./extract_pitches_by_month.py 2019 10
  ```
4. Pitch data is written to ```pitches_{year}_{month}.csv```

# Build and Test
TODO: Describe and show how to build your code and run the tests. 
