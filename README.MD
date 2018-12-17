# Robust XPath Generation through Genetic Algorithm

## CS454 Team #6
- Chanyoung Ryu
- Chanmin Park
- Sangwoo Hahn
- JeongHo Ha

Python codes are written in version 3.6.5

### Prerequisites

```
pip install -r requirements.txt
```


### Running the Codes

```
python main.py [option]
```
Results are saved as result.csv

#### Options:
- ```-d``` Specify path to html file (required)
- ```-p``` Set an even number population size (default=30)
- ```-f``` Set fitness evaluation limit
- ```-r``` Set mutation rate (0.0 ~ 1.0, default=0.1)
- ```-k``` Set mutation limit per child (default=10)
- ```-s``` Show progress
- ```-e``` Use elitism (default=generational_replacement)


### Table of Contents
Main python source for robust XPath Generator
```
/main.py
```
Python implementation of Genetic Algorithm
```
/ga.py
```
Hyperparameter testing suite
```
/eval.py
```

### Built With

* [lxml](https://lxml.de/) - lxml - XML and HTML with Python


**Copyright (C) 2018 CS454 Team #6**
