# Poverty and Inequality Measures

Python Package to calculate some poverty and inequality measures. 

Based on the [Wold Bank Poverty and Inequality Handbook](https://documents1.worldbank.org/curated/en/488081468157174849/pdf/483380PUB0Pove101OFFICIAL0USE0ONLY1.pdf). 


## Poverty 

Package includes calculations of:

- Headcount Index: `get_headcount_index` (pg 68 of the Handbook)
- Poverty Gap Index: `get_poverty_gap_index` (pg 70)
- Poverty Severity Index: `get_poverty_severity_index` (pg 71)
- Generic Poverty Severity Index: `get_poverty_severity_index_generic` (pg 72)
- Sen Index: `get_sen_index` (pg 74)
- Watts Index: `get_watts_index` (pg 77)
- Time To Exit Poverty: `get_time_to_exit` (pg 78)


## Inequality 

Package includes calculations of:

- Gini Coefficient: `get_gini` (pg 104)
- Palma Ratio: `get_palma` (not in the handbook but defined as being the ratio between the income or expenditure of the richest decile divided by the income or expenditure of the poorest four deciles)

## Installation


```sh
pip install povertyInequalityMeasures
```

## General Usage


All methods require a `data` dataframe with at least two columns:

1. `target_col`: The column of data that is being used to measure poverty/inequality. In most cases this is either some sort of total household/individual expenditure or income. See page 20 of the handbook for considerations of which to use.
2. `weight_col`: The column that represents the weighting of each row of data. Normally, data used is survey data and therefore each row (a household or individual sureveyed) represents a given number of actual households/individuals in the population. The weight column should hold that information.

Additionally all `poverty` methods require a poverty line (`pl`) parameter, which is the amount of expenditure/income below which someone is said to be in poverty.

The `time to exit` method requires a `growth` parameter for the expected growth rate of the economy over time.

The `Generic Poverty Severity Index` method requires an `alpha` parameter, which must be greater than 0. 

## Examples

```python
from povertyInequalityMeasures import poverty, inequality
import pandas as pd
```

### Example 1
```python
data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], "weight":[1,1,1,1]})

result=poverty.get_headcount_index(125,data,"total_expenditure","weight")

print(result)
#0.5
```

### Example 2

```python
data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
poverty_line= 125
result = poverty.get_sen_index(poverty_line, data, "total_expenditure","weight")


print(result)
#0.374
```

### Example 3

```python
data = pd.DataFrame({'total_expenditure': [ 100,110,150,160], 'weight':[1,1,1,1]})
poverty_line= 125
result = poverty.get_poverty_severity_index_generic(poverty_line, data, "total_expenditure","weight",2)


print(result)
#0.0136
```

### Example 4

```python
data = pd.DataFrame({'total_expenditure': [7,10,15,18], 'weight':[1,1,1,1]})

result = inequality.get_gini(data, "total_expenditure","weight")

print(result)
#0.19
```