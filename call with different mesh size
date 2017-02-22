underlying = 100
dev = 0.1
rate = 0.025
maturity = 5
dt = 0.1
dt_move = 0.1
strike = 100
option = "call"
M = maturity/dt_move
PriceVan = []
PriceVanBar1 = []
PriceVanBar2 = []
PriceVanBar3 = []
PriceVanBar4 = []
PriceVanBar5 = []
PriceAmBar1 = []
PriceAmBar2 = []
PriceAmBar3 = []
PriceAmBar4 = []
PriceAmBar5 = []
PriceAsBar1 = []
PriceAsBar2 = []
PriceAsBar3 = []
PriceAsBar4 = []
PriceAsBar5 = []
DT = []

for i in range(0, int(M)):
    PriceVan.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, model=1))  
    PriceVanBar1.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike, model=2)) 
    PriceVanBar2.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*1.5, model=2))  
    PriceVanBar3.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*2, model=2))  
    PriceVanBar4.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*2.5, model=2)) 
    PriceVanBar5.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*3, model=2)) 
    PriceAmBar1.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike, model=4)) 
    PriceAmBar2.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*1.5, model=4))  
    PriceAmBar3.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*2, model=4))  
    PriceAmBar4.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*2.5, model=4)) 
    PriceAmBar5.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*3, model=4))  
    PriceAsBar1.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike, model=3)) 
    PriceAsBar2.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*1.5, model=3))  
    PriceAsBar3.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*2, model=3))  
    PriceAsBar4.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*2.5, model=3)) 
    PriceAsBar5.append(binomial_tree(underlying, strike, option, dev, rate, maturity, dt, strike*3, model=3)) 
    
    DT.append(dt)
    dt = round(dt + dt_move, 1)
