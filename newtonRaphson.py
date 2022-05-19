import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

def f(theta):
    return [50*math.cos(theta[0])+math.cos(theta[1]) , 50*math.sin(theta[0])+math.sin(theta[1])]

def g(x, theta):
    return np.subtract(np.array(x), np.array(f(theta)))

def dg_dtheta(theta):
    return np.array([[50*math.sin(theta[0]), 50*math.sin(theta[1])], [-50*math.cos(theta[0]), -50*math.cos(theta[1])]])

def NewtonRaphson(fcn, jacobian, guess, thresh):
    theta = guess
    while(abs(fcn(theta)[0]) > thresh or abs(fcn(theta)[1]) > thresh):
        theta = np.subtract(theta, np.matmul(np.linalg.inv(jacobian(theta)), fcn(theta)))
    return theta

def myraph(dest, guess):
    theta = NewtonRaphson(lambda theta: g(dest,theta), dg_dtheta, guess, 1e-6)
    return theta

