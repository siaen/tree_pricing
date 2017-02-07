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
    
    value_of_underlying = np.zeros((2*(n+1)+1)*(n+1)).reshape((2*(n+1)+1), (n+1))
    value_of_option = value_of_underlying.copy()
    price = value_of_underlying.copy()

    value_of_underlying[int((2*(n+1))/2),0] = underlying
    avg_of_underlying = value_of_underlying.copy()
    avg_of_underlying_basic = avg_of_underlying.copy()
    
    for i in range(1, (n+1)):
        for j in range(1, 2*(n+1)):
            value_of_underlying[j,i] = value_of_underlying[j+1,i-1] * u
            
            if value_of_underlying[j-1,i-1] * d != 0:
                value_of_underlying[j,i] = value_of_underlying[j-1,i-1] * d
    
    value_of_underlying_basic = value_of_underlying.copy()
    
    if barrier != 0:
        value_of_underlying = value_of_underlying * (value_of_underlying < barrier)
        
    for i in range(1, (n+1)):
        for j in range(1, 2*(n+1)):
            avg_of_underlying[j,i] = (avg_of_underlying[j+1,i-1]*i + value_of_underlying[j,i]) / (i+1) 
            avg_of_underlying_basic[j,i] = (avg_of_underlying_basic[j+1,i-1]*i + value_of_underlying[j,i]) / (i+1) 
            
            if value_of_underlying[j-1,i-1] * d != 0:
                avg_of_underlying[j,i]= (avg_of_underlying[j-1,i-1] * i + value_of_underlying[j,i])/(i+1)   
                avg_of_underlying_basic[j,i]= (avg_of_underlying_basic[j-1,i-1] * i + value_of_underlying[j,i])/(i+1)    
                
            avg_of_underlying[j,i] = avg_of_underlying[j,i] * (value_of_underlying[j,i] !=0) 
            
            if i == (n+1)-1 and option == "call":
                if model == 1:
                    value_of_option[j,] = max(value_of_underlying[j,i] - strike, 0)
                elif model in [2, 4]:
                    value_of_option[j,i] = max(value_of_underlying[j,i] - strike, 0)
                elif model == 3:
                    value_of_option[j,i] = max(avg_of_underlying[j,i] - strike, 0)              
            elif i == (n+1)-1 and option == "put":
                if model == 1:
                    value_of_option[j,i] = max(strike - value_of_underlying[j,i], 0)
                elif model in [2, 4]:
                    value_of_option[j,i] = max(strike - value_of_underlying[j,i], 0)
                elif model == 3:
                    value_of_option[j,i] = max(strike - avg_of_underlying[j,i], 0)
            
    for i in range(1, (n+1)):
        for j in range(1, 2*(n+1)):
            value_of_option[j,n-i] = np.exp(-1*rate*dt)*(p*value_of_option[j-1,n+1-i]+(1-p)*value_of_option[j+1,n+1-i])
            if model == 4:
                if option == "call":
                    exercise = (value_of_underlying[j,n-i] - strike)*np.exp(-1*rate*dt)
                    if (value_of_option[j,n-i] > exercise):
                        value_of_option[j,n-i] = exercise              
                elif option == "put":
                    exercise = (strike - value_of_underlying[j,n-i])*np.exp(-1*rate*dt)
                    if (value_of_option[j,n-i] < exercise):
                        value_of_option[j,n-i] = exercise
            value_of_option[j,n-i] = value_of_option[j,n-i] * (value_of_underlying[j,n-i] !=0)
   
    price_of_option = value_of_option[int((2*(n+1)) / 2), 0]
    
    return price_of_option

def main():
    underlying = 150
    dev = 0.1
    rate = 0.05
    maturity = 4
    dt = 1
    strike = 100
    barrier = 160
    option = "call"

    print "Europen Vanilla " + option + " price: " + str(binomial_tree(underlying, strike, option, dev, rate,
                                                                       maturity, dt, model=1))
    print "Europen Barrier " + option + " price: " + str(binomial_tree(underlying, strike, option, dev, rate,
                                                                       maturity, dt, barrier, model=2))
    print "Asian Barrier " + option + " price: " + str(binomial_tree(underlying, strike, option, dev, rate,
                                                                     maturity, dt, barrier, model=3))
    print "American Barrier " + option + " price: " + str(binomial_tree(underlying, strike, option, dev, rate,
                                                                        maturity, dt, barrier, model=4))
    
    option = "put"
    
    print "Europen Vanilla " + option + " price: " + str(binomial_tree(underlying, strike, option, dev, rate,
                                                                       maturity, dt, model=1))
    print "Europen Barrier " + option + " price: " + str(binomial_tree(underlying, strike, option, dev, rate,
                                                                       maturity, dt, barrier, model=2))
    print "Asian Barrier " + option + " price: " + str(binomial_tree(underlying, strike, option, dev, rate,
                                                                     maturity, dt, barrier, model=3))
    print "American Barrier " + option + " price: " + str(binomial_tree(underlying, strike, option, dev, rate,
                                                                        maturity, dt, barrier, model=4))
