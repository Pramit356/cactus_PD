import csv
import numpy as np
import math

# In this file we run linear regression
training_data = np.genfromtxt('modeldata.csv', delimiter=',')
training_data = np.delete(training_data, (0), axis=0)
print('Training data: ', training_data)

#initializing parameters
learning_rate = 0.01
theta = np.zeros((1,7))
theta0 = 0
m = training_data.shape[0]
print('Training set size: ',m)

#Normalizing the data
mean = np.mean(training_data, axis=0, keepdims=True)
#print('mean:', mean)
sd = np.std(training_data, axis=0, keepdims=True)
#print('SD: ',sd)
print()
print()
normalized_data = (training_data-mean)/sd
print('Normalized data: ',normalized_data)

#Separating and removing the dependent variable from the normalized data
output = normalized_data[:,-1]
normalized_data = np.delete(normalized_data,(-1), axis=1)
h = np.dot(theta, normalized_data.T)+theta0

for i in range(m):
    x = normalized_data[i,:]
    h = np.dot(theta, x.T)+theta0
    theta0 = theta0 - (learning_rate/m)*(h-output[i])
    theta = theta - (learning_rate/m)*(h-output[i])*x
print()
print('Final parameters: ',theta0,theta)

#Working on the test data for finding the accuracy
test_data = np.genfromtxt('modeldata.csv', delimiter=',')
test_data = np.delete(test_data, (0), axis=0)

#Normalizing test data
mean1 = np.mean(test_data, axis=0, keepdims=True)
#print('mean:', mean)
sd1 = np.std(test_data, axis=0, keepdims=True)
#print('SD: ',sd)

normalized_test_data = (test_data-mean1)/sd
print()
print('Normalized test data: ',normalized_test_data)

target_output = normalized_test_data[:,-1]
normalized_test_data = np.delete(normalized_test_data,(-1), axis=1)

Jtheta = np.dot(theta,normalized_test_data.T).T+theta0
rmse = math.sqrt(np.sum((Jtheta-target_output)**2))
print()
print('RMSE value for test data: ', rmse)

meanuser = mean[:,:-1].copy()
sduser = sd[:,:-1].copy()
print()
x = np.array(input("Enter the conditions separated by space in following format(SolnD SolnA Humidity Noise SolnB SolnC Tried): ").split())
x1 = x.astype(np.float)
normalized = (x1-meanuser)/sduser
J = np.dot(theta,normalized.T).T+theta0
J = (J+mean[:,-1])/sd[:,-1]

print("Possibility of success = "+str(J)[2:-2]+"%")