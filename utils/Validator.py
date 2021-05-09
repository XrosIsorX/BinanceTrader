import pandas as pd
import numpy as np

def calculate_all(real, predict):
    print("Accurary up/mid/down : ", calculate_accurary_up_mid_down(real, predict))
    print("Accurary only up/down : ", calculate_accurary_only_up_down(real, predict))
    print("Accurary up/down(zero up) : ", calculate_accurary_up_down_zero_up(real, predict))
    print("Accurary up/down(zero down) : ", calculate_accurary_up_down_zero_down(real, predict))

def calculate_accurary_up_mid_down(real, predict, scope=0.2):
    correct = 0
    incorrect = 0
    for i in range(len(real)):
        if (real[i] >= scope and predict[i] >= scope) or (real[i] <= -1 * scope and predict[i] <= -1 * scope) or (real[i] < scope and predict[i] < scope and real[i] > -1 * scope and predict[i] > -1 * scope):
            correct += 1
        else:
            incorrect += 1
    percent = float(correct/len(real))
    return percent

def calculate_accurary_only_up_down(real, predict):
    correct = 0
    incorrect = 0
    zero = 0
    for i in range(len(real)):
        if real[i] == 0:
            zero += 1
        elif (real[i] > 0 and predict[i] > 0) or (real[i] < 0 and predict[i] < 0):
            correct += 1
        else:
            incorrect += 1
    percent = float(correct / (len(real) - zero))
    print(zero)
    print(len(real))
    return percent

def calculate_accurary_up_down_zero_up(real, predict):
    correct = 0
    incorrect = 0
    for i in range(len(real)):
        if (real[i] >= 0 and predict[i] >= 0) or (real[i] < 0 and predict[i] < 0):
            correct += 1
        else:
            incorrect += 1
    percent = float(correct/len(real))
    return percent

def calculate_accurary_up_down_zero_down(real, predict):
    correct = 0
    incorrect = 0
    for i in range(len(real)):
        if (real[i] > 0 and predict[i] > 0) or (real[i] <= 0 and predict[i] <= 0):
            correct += 1
        else:
            incorrect += 1
    percent = float(correct/len(real))
    return percent

def calculate_sharpe_ratio(data, risk_free_rate=0, period=252):
    data = pd.Series(data)
    std = data.std()
    expected_return = data.mean()
    if std == 0:
        return 0
    sharpe_ratio = (expected_return / std) * (period ** 0.5)
    return sharpe_ratio

def calculate_maximum_drawdown(cumulative_profits):
    cumulative_profits = pd.Series(cumulative_profits)
    cumulative_highs = cumulative_profits.cummax()
    return max(cumulative_highs - cumulative_profits)

def calculate_maximum_profit(cumulative_profits):
    return max(cumulative_profits)

def calculate_maximum_loss(cumulative_profits):
    return min(cumulative_profits)

def calculate_class_accuracy(real_list, predict_list):
    real_series = pd.Series(list(real_list)) # convert to list to remove index
    predict_series = pd.Series(list(predict_list)) # convert to list to remove index
    return (real_series == predict_series).sum() / real_series.shape[0]
