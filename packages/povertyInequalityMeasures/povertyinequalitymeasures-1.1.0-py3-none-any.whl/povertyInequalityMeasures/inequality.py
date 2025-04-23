import pandas as pd
import numpy as np

def get_gini(data,target_col,weight_col):
    nrows = data.shape[0] # count of rows
    if nrows == 0:
        return 0.0
    gini=0.0
    #sort by target column - this could be income, expenditure etc
    sorted_data = data.sort_values(by=target_col).reset_index(drop=True)
    #print(sorted_data)
    #now do accuumulation for the thing you are sorting, because this is all about cumulative income/expenditure/whatever
    sorted_data["POPN_ACCUM"] = sorted_data[weight_col].cumsum()
    sorted_data["TARGET_ACCUM"] = (sorted_data[target_col] * sorted_data[weight_col]).cumsum()
    #print(sorted_data)
    # now work out the gini

    # Shifted versions of the columns
    popn = sorted_data["POPN_ACCUM"].values
    target = sorted_data["TARGET_ACCUM"].values

    #Use vectorized trapezoidal rule
    lorenz_area = np.sum((popn[1:] - popn[:-1]) * (target[1:] + target[:-1]))
    lorenz_area /= (popn[-1] * target[-1])  # Normalize
    #print(lorenz_area)
    gini = 1 - lorenz_area
    return round(gini,2)

def get_palma(data,target_col,weight_col):
    nrows = data.shape[0] # count of rows
    if nrows == 0:
        return 0.0
    palma=0.0
    #sort by target column - this could be income, expenditure etc
    sorted_data = data.sort_values(by=target_col).reset_index(drop=True)
    #print(sorted_data)
    #now do accuumulation for the thing you are sorting, because this is all about cumulative income/expenditure/whatever

    sorted_data["POPN_ACCUM"] = sorted_data[weight_col].cumsum()
    sorted_data["TARGET_ACCUM"] = (sorted_data[target_col] * sorted_data[weight_col]).cumsum()
    sorted_data["TARGET_WEIGHTED"] = sorted_data.apply(lambda row: row[target_col]*row[weight_col], axis=1) #the thing you are measuring, but weighted
    #print(sorted_data)

    #now work out the palma
    sorted_data['bins'] = pd.cut(x=sorted_data['POPN_ACCUM'],bins=10) #split into ten bins by population
    #print(sorted_data)
    accumulated_target_per_decile = sorted_data.groupby(['bins'], observed=False)['TARGET_ACCUM'].agg(['max'])
    #print (accumulated_income_per_decile)
    target_per_decile = (sorted_data.groupby(['bins'],observed=False)['TARGET_WEIGHTED'].agg(['sum']))  
    palma = float(target_per_decile.iloc[9].iloc[0]) / float(accumulated_target_per_decile.iloc[3].iloc[0])
    # in other words the amount that the top decile has of the thing you are measuring divided by the amount that the bottom 4 deciles have
    return round(palma,2)
    # also, not to future self: that strange double iloc notation was used to get rid of this warning:
    # FutureWarning: Calling float on a single element Series is deprecated and will raise a TypeError in the future. Use float(ser.iloc[0]) instead
    # was following this article: https://stackoverflow.com/questions/76256618/how-to-deal-with-futurewarning-regarding-applying-int-to-a-series-with-one-item#76848560
    # it works, but I don't understand why!
    