#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 20:00:01 2022

@author: riddhipathak
"""
import pandas as pd
import math as m
import numpy as np
from scipy.stats import norm

class Option:
    def __init__(self, K, r, sigma, T, t, r0, N):
        self.K = K              #strike rate
        self.r = r              #risk free rate
        self.sigma = sigma      #volatility
        self.T = T              #time to maturity
        self.t = t
        self.dt = 1/60
        self.r0 = r0            #initial rate
        self.prices = []        #prices generated for 60 days (3 months)
        self.N = N              #paths
        
    def calculateD(self):
        # calculating the Z value to get the normal distribution
        self.d2 = (m.log(self.r0/self.K)+(self.r - 0.5*self.sigma**2)*
                   (self.T-self.t))/(self.sigma*m.sqrt(self.T-self.t))
    
    def calculateValue0(self):
        self.calculateD()
        # calculating the normal value 
        Nd2 = norm.cdf(self.d2)
        # final valu calcualated using Black-Scholes Analytic
        v0 = Nd2*m.e**(-self.r*(self.T-self.t))
        
        return (v0)
    
class GeometricBrowninanMotion(Option):
    def __init__(self, Option):
        self.rtPrices = []
        
    def getrT(self,Option, z):
        # simulating 1,000,000 values of the rates, at maturity
        self.rtPrices = Option.r0 * np.exp((Option.r - 0.5 * Option.sigma ** 2) 
                                           * Option.T + Option.sigma 
                                           * np.sqrt(Option.T) * z)
        return self.rtPrices
        
    
class OptionPayoff():
    def __init__(self):
        self.payOff = 0
        
    #calculating payoff for single condition digital option
    def getPayoff(self,opt,GBM):
        for rt in GBM.rtPrices:
            if round(rt,2) > opt.K:
                self.payOff += 1
        return (self.payOff/opt.N)*np.exp(-opt.r*opt.T)
    
    #calculating payoff for dual condition option
    def getDualConOption(self, opt, GBM, Nikkei): 
        for i in range(opt.N):
            if (GBM.rtPrices[i] > opt.K and Nikkei.n0/Nikkei.nikkei[i] > 1.05) :
                self.payOff += 1
        return (self.payOff/opt.N)*np.exp(-opt.r*opt.T)
                
                
        
class Nikkei(GeometricBrowninanMotion):
    def __init__(self, n0):
        self.nikkei = []
        self.n0 = n0
        
    def getNikkei(self, Option, z):
        # simulating the value of Nikkei
        self.nikkei = self.n0 * np.exp((Option.r - 0.5 * Option.sigma ** 2) 
                                           * Option.T + Option.sigma 
                                           * np.sqrt(Option.T) * z)
        return self.nikkei
        