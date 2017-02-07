import numpy as np

import pandas as pd


def binomial_tree(underlying, strike, option, dev, rate, maturity, dt, barrier=0, model=1):
    """
    1 model -> European Vanilla
    2 model -> European Barrier Vanilla
    3 model -> Asian Barrier Vanilla
    4 model -> American Barrier Vanila
    """

    n = int(maturity/dt)
    u = np.exp(dev*np.sqrt(dt))
    d = 1/u
    p = (np.exp(rate*dt)-d)/(u-d)
    indicator_barrier = 1
    
    barrier_model = False
    if model == 2 or model == 3 or model == 4:
        barrier_model = True
    
    i_max = n+1
    j_max = 2*(n+1)
    i_dim = range(1, i_max)
    j_dim = range(1, j_max)

    def _reverse_calc_options(max_recalc_i=i_max):
        for i in range(1, max_recalc_i):
            for j in j_dim:
                i_this = max_recalc_i - 1 - i
                if value_of_underlying[j,i_this] != 0:
                    value_of_option[j,i_this]= np.exp(-1*rate*dt)*(p*value_of_option[j-1,i_this+1]+(1-p)*value_of_option[j+1,i_this+1])
                if barrier_model and value_of_underlying[j,i_this] > barrier:
                    value_of_option[j,i_this] = 0
                if model == 4:
                    if option == "call":
                        exercise = (value_of_underlying[j,i_this] - strike)*np.exp(-1*rate*dt)
                        if (value_of_option[j,i_this] > exercise):
                            value_of_option[j,i_this] = exercise               
                    elif option == "put":
                        exercise = (strike - value_of_underlying[j,i_this])*np.exp(-1*rate*dt)
                        if (value_of_option[j,i_this] < exercise):
                            value_of_option[j,i_this] = exercise

    
    value_of_underlying = np.zeros((j_max+1)*i_max).reshape((j_max+1), i_max)
    value_of_option = value_of_underlying.copy()
    price = value_of_underlying.copy()

    value_of_underlying[int((j_max)/2),0] = underlying
    avg_of_underlying = value_of_underlying.copy()
    
    for i in i_dim:
        for j in j_dim:
            value_of_underlying[j,i] = value_of_underlying[j+1,i-1] * u
            avg_of_underlying[j,i] = (avg_of_underlying[j+1,i-1]*i + value_of_underlying[j,i]) / (i+1)
            
            if value_of_underlying[j-1,i-1] * d != 0:
                value_of_underlying[j,i] = value_of_underlying[j-1,i-1] * d
                avg_of_underlying[j,i]= (avg_of_underlying[j-1,i-1] * i + value_of_underlying[j,i])/(i+1)
                        
            if i == (n+1)-1 and option == "call":
                if model == 1:
                    value_of_option[j,i] = max(value_of_underlying[j,i] - strike, 0)
                elif model in [2, 4]:
                    value_of_option[j,i] = max(value_of_underlying[j,i] - strike, 0)
                elif model == 3:
                    value_of_option[j,i] = max(avg_of_underlying[j,i] - strike, 0)
                else:
                    return "Error, not valid model type!"               
            elif i == (n+1)-1 and option == "put":
                if model == 1:
                    value_of_option[j,i] = max(strike - value_of_underlying[j,i], 0)
                elif model in [2, 4]:
                    value_of_option[j,i] = max(strike - value_of_underlying[j,i], 0)
                elif model == 3:
                    value_of_option[j,i] = max(strike - avg_of_underlying[j,i], 0)
                else:
                    return "Error, not valid model type!"
            elif i == (n+1)-1:
                return "Error, not valid option type!"
            else:
                pass
    
    # Barrier models
    in_barrier = False
    if barrier_model:
        for i in range(0, i_max):
            for j in range(0, j_max):
                if value_of_underlying[j,n-i] > barrier:
                    value_of_option[j,n-i] = 0
                    in_barrier = True
               
    
    _reverse_calc_options()
    print value_of_option
    
    if in_barrier:
        recalc_points = []
        for i in range(0, i_max - 1):
            if value_of_underlying[:,i].max() > barrier:
                top_idx = 0
                down_idx = 0
                for j in range(0, j_max):
                    if value_of_underlying[j,i] > barrier:
                        top_idx = j
                    elif value_of_underlying[j,i] < barrier and value_of_underlying[j,i] != 0:
                        bottom_idx = j
                        break
                recalc_points.append([i, [top_idx, bottom_idx]])
    
        for recalc in recalc_points:
            D = value_of_underlying[recalc[1][1], recalc[0]]
            U = value_of_underlying[recalc[1][0], recalc[0]]
            value_op = value_of_option[recalc[1][1], recalc[0]]
            value_of_option[recalc[1][1], recalc[0]] = (barrier - D) / (U - D) * value_op
        
        print value_of_option
        _reverse_calc_options(i_max - 1)
    
    print value_of_option

    price_of_option = value_of_option[int((2*(n+1)) / 2), 0]
    
    return price_of_option
