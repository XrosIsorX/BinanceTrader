import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
from statsmodels.tsa.arima_model import ARIMA

import warnings
warnings.filterwarnings("ignore")

def invert_transformation(df_train, df_forecast, second_diff=False):
    """
    Revert back the differencing to get the forecast to original scale. (Max : 2 differencing)
    df_train (dataframe) : train data
    df_forecast (dataframe) : forecast data
    second_diff (boolean) : if True invert second difference, if False invert first difference
    return (dataframe) : reverted data
    """
    df_fc = df_forecast.copy()
    columns = df_train.columns
    for col in columns:
        # Roll back 2nd Diff
        if second_diff:
            df_fc[str(col)+'_1d'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2]) + df_fc[str(col)+'_2d'].cumsum()
        # Roll back 1st Diff
        df_fc[str(col)+'_forecast'] = df_train[col].iloc[-1] + df_fc[str(col)+'_1d'].cumsum()
    return df_fc

def append_string_to_each_item(list_of_string, string_to_add):
    """
    append specific string to all items in list
    list_of_string (list) : list of string that will be appended by string_to_add
    string_to_add (str) : string that will be added to all items in list_of_string
    return (list) : list of appended string
    """
    return list(map(lambda string: string + string_to_add, list_of_string))

def forecast(df_train, number_of_forecast_points, forecast_index, lag_order=5, diff=2):
    """
    Learn and forecast with VAR model (Max : 2 differencing)
    df_train (dataframe) : input data
    number_of_forecast_points (int) : number of time step that want to predict
    forecast_index (list) : index name of each predicted value
    lag_order (int) : window size of input (How many previous timestep will be used as input)
    diff (int 0, 1, 2) : number of differencing
    return 
    real_forecast (dataframe) : dataframe with predicted value
    model (Object) : fitted model
    """
    assert diff == 0 or diff == 1 or diff == 2, 'diff = 1 or 2 only'

    df_differenced = df_train
    for _ in range(diff):
        df_differenced = df_differenced.diff().dropna()

    model = VAR(df_differenced)
    model_fitted = model.fit(lag_order)

    forecast_input = df_differenced.values[-lag_order:]

    fc = model_fitted.forecast(y=forecast_input, steps=number_of_forecast_points)

    if diff == 0:
        real_forecast = pd.DataFrame(fc, index=forecast_index, columns=df_train.columns + '_forecast')
    elif diff == 1:
        df_forecast = pd.DataFrame(fc, index=forecast_index, columns=df_train.columns + '_1d')
        real_forecast = invert_transformation(df_train, df_forecast, second_diff=False)
    elif diff == 2:
        df_forecast = pd.DataFrame(fc, index=forecast_index, columns=df_train.columns + '_2d')
        real_forecast = invert_transformation(df_train, df_forecast, second_diff=True) 

    return real_forecast, model_fitted

def calculate_origin_coefficient(coeff_df, diff=2):
    """
    Calculate from coefficient of difference value to no difference value
    coeff_df (dataframe) : a dataframe with statsmodel(model.params) format
    diff (int 0, 1, 2) : number of differencing
    return
    origin_coeff_df_dict (dict) : dict that contain no difference coefficient dataframe of each column
    const_dict (dict) : constant of formula of each column
    """
    assert diff == 0 or diff == 1 or diff == 2, "diff = 0, 1 or 2 only"

    coeff_df = coeff_df.copy()
    origin_coeff_df_dict = {}
    const_dict = {}
    for column in coeff_df.columns:
        temp_dict = {c : {} for c in coeff_df.columns}

        # Calculate right side formula
        for index in coeff_df.index:
            value = coeff_df[column].loc[index]
            if index == "const":
                const_dict[column] = value
            else:
                first_dot_index = index.find(".") 
                lag = index[:first_dot_index] 
                feature = index[first_dot_index + 1:]
                lag = -1 * int(lag.replace("L", ""))
                if diff == 1:
                    if lag in temp_dict[feature]:
                        temp_dict[feature][lag] += value
                    else:
                        temp_dict[feature][lag] = value
                    if (lag - 1) in temp_dict[feature]:
                        temp_dict[feature][lag - 1] += -1 * value
                    else:
                        temp_dict[feature][lag - 1] = -1 * value
                elif diff == 2:
                    if lag in temp_dict[feature]:
                        temp_dict[feature][lag] += value
                    else:
                        temp_dict[feature][lag] = value

                    if (lag - 1) in temp_dict[feature]:
                        temp_dict[feature][lag - 1] += -2 * value
                    else:
                        temp_dict[feature][lag - 1] = -2 * value

                    if (lag - 2) in temp_dict[feature]:
                        temp_dict[feature][lag - 2] += value
                    else:
                        temp_dict[feature][lag - 2] = value
        
        # Calculate left side formula
        if diff == 1:
            temp_dict[column][-1] += 1
        elif diff == 2:
            temp_dict[column][-1] += 2
            temp_dict[column][-2] += -1
            
        origin_coeff_df_dict[column] = pd.DataFrame(temp_dict)
        
    return origin_coeff_df_dict, const_dict
