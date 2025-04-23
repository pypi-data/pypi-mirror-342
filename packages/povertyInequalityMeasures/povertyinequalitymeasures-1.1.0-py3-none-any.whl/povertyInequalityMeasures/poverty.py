from povertyInequalityMeasures import inequality
import numpy as np

def get_headcount_index(pl,data,target_col,weight_col):
    #pl is the poverty line
    #data is a dataframe containing survey data
    #target_col is the column within the data that will be used. It can be expenditure, income, or something else
    #weight_col is the column that has the weight of each row (i.e. the number of actual households that a row represents)
    total_sample = data[weight_col].sum() # the number of actual people each hh row represents
    #print(total_sample)
    the_poor = data[data[target_col] < pl]  # a dataframe that only includes poor people, ie those below the poverty line
    #print("the poor are ", the_poor)
    the_weighted_poor = the_poor[weight_col].sum()  # the actual amount of poor people based on the number of people each household represents
    #print(the_weighted_poor)
    poverty_index = the_weighted_poor / total_sample
    return poverty_index

def get_poverty_gap_index(pl,data,target_col, weight_col):
    #pl is the poverty line
    #data is a dataframe containing survey data
    total_sample = data.shape[0] # number of rows
    total_sample_weighted = data[weight_col].sum()
    data["poverty_gap"] = ((pl - data[target_col]) / pl).clip(lower=0)
    poverty_gap_index = (data["poverty_gap"]*data[weight_col]).sum() / total_sample_weighted
    return round(poverty_gap_index,5)

def get_poverty_severity_index(pl, data, target_col, weight_col):
    #pl is the poverty line
    #data is a dataframe containing survey data
    total_sample = data.shape[0] # number of rows
    total_sample_weighted = data[weight_col].sum()
    data["poverty_gap_squared"] = (((pl - data[target_col]) / pl).clip(lower=0))**2
    poverty_severity_index = (data["poverty_gap_squared"]*data[weight_col]).sum() / total_sample_weighted
    #print(data)
    return round(poverty_severity_index,5)

def get_poverty_severity_index_generic(pl, data, target_col, weight_col,alpha):
    #pl is the poverty line
    #data is a dataframe containing survey data
    # alpha is the measure of the sensitivity of the index to poverty.Alpha has to be >=o
    if alpha < 0:
        return "Error. Alpha must be >=0"
    total_sample = data.shape[0] # number of rows
    total_sample_weighted = data[weight_col].sum()
    data["poverty_gap_alpha"] = data[target_col].apply(lambda x: ((pl - x)/pl)**alpha if (pl - x) > 0 else 0)
    poverty_severity_index_generic = (data["poverty_gap_alpha"]*data[weight_col]).sum() / total_sample_weighted
    #print(data)
    return round(poverty_severity_index_generic,5)

def get_sen_index(pl,data, target_col, weight_col):
    pov_headcount = get_headcount_index(pl,data, target_col, weight_col)
    #print(pov_headcount)
    pov_gap = get_poverty_gap_index(pl,data, target_col, weight_col)
    #print(pov_gap)
    gini = inequality.get_gini(data, target_col, weight_col)
    sen_index = pov_headcount*gini + pov_gap*(1-gini)
    return round(sen_index,3)

def get_watts_index (pl, data,target_col, weight_col):
    total_sample = data.shape[0] # number of rows
    total_sample_weighted = data[weight_col].sum()  #number of actual people the sample represents
    watts_total=0 # to contain our adding of the totals below

    mask = data[target_col] < pl 
    # Creates a boolean Series marking which rows are below the poverty line. 
    # Then uses only those to add to the watts total
    watts_total = np.sum(np.log(pl / data.loc[mask, target_col]) * data.loc[mask, weight_col])
    #finally divide by the total sample
    watts_total = watts_total / total_sample_weighted
    return round(watts_total,5)

def get_time_to_exit(pl,data, growth, target_col):
    total_sample = data.shape[0] # number of rows
    data["time_to_exit"] = data[target_col].apply(lambda x: round((np.log(pl/x))/growth,2) if x<pl else 0 )
    # for i in range(0,total_sample):
    #     if data.loc[i, target_col] < pl:
    #         #add a time to exit to that row
    #         data.loc[i, "time_to_exit"] = round((math.log(pl/data.loc[i,target_col]))/growth,2)
    print (data)
    return data