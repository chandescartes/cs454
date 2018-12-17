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


### Generating Robust XPaths

```
python main.py [option]
```

For each test case, three candidate robust XPaths are found.

Results are saved as ```results.csv```

#### Options:
- ```-d``` Specify path to test file (required)
- ```-p``` Set an even number population size (default=30)
- ```-f``` Set fitness evaluation limit (default=10000)
- ```-r``` Set mutation rate (0.0 ~ 1.0, default=0.3)
- ```-k``` Set mutation limit per child (default=3)
- ```-c``` Set crossover rate (0.0 ~ 1.0, default=0.8)
- ```-t``` Set tournament selection k value (default=3)
- ```-l``` Use linear ranking (default=tournament selection)
- ```-e``` Use elitism (default=generational_replacement)
- ```-s``` Show progress

Test files are ```.csv``` files with a test case on each row.
Each test case is a filepath to a html document and a XPath of the target element.

See ```example_testfile.csv``` for reference.

### Testing Hyperparameters

```
python eval.py [option]
```

Test on ```test_eval_full``` only.

#### Options:
- ```-d``` Specify path to test file (required)
- ```-p``` Set an even number population size (default=30)
- ```-f``` Set fitness evaluation limit (default=10000)
- ```-r``` Set mutation rate (0.0 ~ 1.0, default=0.3)
- ```-k``` Set mutation limit per child (default=3)
- ```-c``` Set crossover rate (0.0 ~ 1.0, default=0.8)
- ```-t``` Set tournament selection k value (default=3)
- ```-l``` Use linear ranking (default=tournament selection)
- ```-e``` Use elitism (default=generational_replacement)
- ```-s``` Show progress
- ```-P``` Use parallel computation (highly recommended)
- ```-i``` Set test id (default=0)

Test files have all filepath for the old and new html documents as well as the target XPath for both.

See ```test_eval_full.csv``` for reference.

### Table of Contents
Main python source for robust XPath Generator
```
/main.py
```
Python implementation of Genetic Algorithm
```
/ga.py
```
Hyperparameter testing suite- searches for optimal fitness function values
```
/eval.py
```
Example testfile for ```main.py```
```
/example_testfile.csv
```
Full test file for Hyperparameter tuning on ```eval.py```
```
/test_eval_full.csv
```


### Built With

* [lxml](https://lxml.de/) - lxml - XML and HTML with Python


**Copyright (C) 2018 CS454 Team #6**
