import numpy as np
import pandas as pd

def BinomialTreeVanilla(S0,K,ChoiceOption,s,r,T,dt):
    
    N = int(T/dt)
    u = np.exp(s*np.sqrt(dt))
    d = 1/u
    p = (np.exp(r*dt)-d)/(u-d)
    
    S = np.zeros((2*(N+1)+1)*(N+1)).reshape((2*(N+1)+1),(N+1))
    option = S.copy()
    price = S.copy()
    
    S[int((2*(N+1))/2),0] = S0
    
    for i in range(1,(N+1)):
        for j in range(1,2*(N+1)):
            S[j,i] = S[j+1,i-1]*u
            if S[j-1,i-1]*d != 0:
                S[j,i] = S[j-1,i-1]*d
            if ChoiceOption == "call":
                option[j,i]=max(S[j,i]-K,0)
            else:
                option[j,i]=max(K-S[j,i],0)            
    
    for i in range(1,(N+1)):
        for j in range(1,2*(N+1)):
            price[j,N-i]= np.exp(-1*r*dt)*(p*option[j-1,N+1-i]+(1-p)*option[j+1,N+1-i])
            
    PriceOfOption = price[int((2*(N+1))/2),0]
    
    return PriceOfOption

def BinomialTreeAsianBarrier(S0,K,B,ChoiceOption,s,r,T,dt):
    
    N = int(T/dt)
    u = np.exp(s*np.sqrt(dt))
    d = 1/u
    p = (np.exp(r*dt)-d)/(u-d)
    
    S = np.zeros((2*(N+1)+1)*(N+1)).reshape((2*(N+1)+1),(N+1))
    option = S.copy()
    price = S.copy()
    IndBarrier = S.copy()
        
    S[int((2*(N+1))/2),0] = S0
    Avg = S.copy()
        
    for i in range(1,(N+1)):
        for j in range(1,2*(N+1)):
            S[j,i] = S[j+1,i-1]*u
            Avg[j,i]= (Avg[j+1,i-1]*i+S[j,i])/(i+1)
            
            if S[j-1,i-1]*d != 0:
                S[j,i] = S[j-1,i-1]*d
                Avg[j,i]= (Avg[j-1,i-1]*i+S[j,i])/(i+1)        
            
            if (S[j,i]<B) and (S[j,i] != 0):
                IndBarrier[j,i] = 1
                
            if ChoiceOption == "call":
                option[j,i]=max(Avg[j,i]-K,0)*IndBarrier[j,i]
            else:
                option[j,i]=max(K-Avg[j,i],0)*IndBarrier[j,i]    
    
    for i in range(1,(N+1)):
        for j in range(1,2*(N+1)):
            price[j,N-i]= np.exp(-1*r*dt)*(p*option[j-1,N+1-i]+(1-p)*option[j+1,N+1-i])
            
    PriceOfOption = price[int((2*(N+1))/2),0]
    
    return PriceOfOption    

def main():
    S0 = 100
    s = 0.1
    r = 0.05
    T = 4
    dt = 1
    K = 100
    B = 120
    ChoiceOption = "call"

    print BinomialTreeVanilla(S0,K,ChoiceOption,s,r,T,dt)
    print BinomialTreeAsianBarrier(S0,K,B,ChoiceOption,s,r,T,dt)
