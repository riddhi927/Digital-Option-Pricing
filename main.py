#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 19:57:06 2022

@author: riddhipathak
"""

import pandas as pd
import math as m
import numpy as np
from scipy.stats import norm
import Option
import matplotlib.pyplot as plt

r0 = 1.33           # Today's rate
K = r0 + 0.25       # Strike rate
r = 0.01            # Risk Free rate
sigma = 0.17        # Volatility
T = 0.25            # Time to maturity - 3 months
t = 0               # inital time
paths = 1000000     # number of simulations
corr = -0.5         #correlation

#Black Scholes implementation 

opt = Option.Option(K, r, sigma, T, t, r0, paths)
blackScholesValue = opt.calculateValue0()
print("option value Black-Scholes Analytic",blackScholesValue)

#Scenario Analysis
#the time to maturity adjusted to 2 months, since we are conducting our analysis 
#one month forward
scenarioAnalysis = Option.ScenarioAnalysis(K, r, sigma, 0.167, t, r0)
values = scenarioAnalysis.calculateValue0()
scenarioAnalysis.graphScenario()


#monte carlo simulation 
opt = Option.Option(K, r, sigma, T, t, r0, paths)
GBM = Option.GeometricBrowninanMotion(opt)
z = np.random.standard_normal(paths)
rT_prices=GBM.getrT(opt, z)
optionPayoff = Option.OptionPayoff()
monteCarloValue = optionPayoff.getPayoff(opt, GBM)

print("option value monte carlo simulation", monteCarloValue)

mean = [0,0]
cov = [[1,corr],[corr,1]]

x,y = np.random.multivariate_normal(mean, cov, paths).T #simulating correlated random values
nikkei = Option.Nikkei(27382.56)
n = nikkei.getNikkei(opt, x)
dualConOption = Option.OptionPayoff() #initializing payoff object again
dualConPayoff = dualConOption.getDualConOption(opt, GBM, nikkei) 
print("Dual condition option - value monte carlo simulation", dualConPayoff)
