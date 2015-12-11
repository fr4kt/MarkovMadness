"""
Created on Tue Jul 07 19:40:08 2015

@author: Jeremy Batterson
"""

import numpy as np
import matplotlib.pyplot as plt

class MarkovError(Exception):
    pass

class MarkovChain():            
    def __init__(self,matrix, nodeWeights):
        self.matrix = np.matrix(matrix,dtype=np.float)
        self.origMatrix = self.matrix
        self.step = 0
        self.states = range(len(matrix))
        self.nodeWeights = np.array(nodeWeights,dtype=np.int)
        self.history = self.nodeWeights
        #Make sure everything is kosher
        if len(self.nodeWeights) != len(self.matrix):
            raise MarkovError("Node weight list should be as long as matrix dimension")        
        for row in self.matrix:
            if np.round(np.sum(row),5) != 1.0:
                print row
                raise MarkovError("All rows in matrix must sum to 1. See above row")
        if not np.all(self.nodeWeights >= 0):
            raise MarkovError("All node weights must be non-negative")
        
    def addWeight(self,nodeIndex, weight):
        self.nodeWeights[nodeIndex] += weight
        if not np.all(self.nodeWeights >= 0):
            raise MarkovError("All node weights must be non-negative")
        
    def modTransProb(self, fromNode, toNode, val):
        self.matrix[fromNode, toNode] = val
        if np.round(np.sum(self.matrix[fromNode]),5) != 1:
            print self.matrix[fromNode]
            raise MarkovError("All rows in matrix must sum to 1. See above row")
    
    def update(self):
        self.step += 1
        newNodeWeights = self.nodeWeights
        for i in self.states:
            if self.nodeWeights[i] < 1:
                continue
            interval = self.matrix[i].cumsum()
            seed = np.random.rand()
            #print seed
            #not sure why np.where returning 2 arrays, but this is workaround
            nodeIndex = np.min(np.where(interval > seed)[1])
            #print nodeIndex
            #TODO: allow different weight transfers
            newNodeWeights[i] -= 1
            newNodeWeights[nodeIndex] += 1
        self.nodeWeights = newNodeWeights
        self.history = np.vstack([self.history,self.nodeWeights])
        return self.nodeWeights
                    
    def simulate(self,steps):
        count = 0
        while count < steps:
            self.update()
            count += 1
        return self.history
        
    def reset(self):
        self.matrix = self.origMatrix
        self.nodeWeights = self.history[0]
        self.step = 0
        
    def plot(self,transpose = False):
        plt.figure(figsize=(10,10))
        plt.title("Markov Sim")
        if transpose:
            plt.imshow(self.history.transpose(),interpolation='nearest')
        else:
            plt.imshow(self.history,interpolation='nearest')
        plt.show()

def randMat(size):
    mat = np.random.rand((size,size))
    for row in mat:
        row = row/np.sum(row)
    return mat    
    
transMat = [[.2,.1,.3,.2,.2],
            [.2,.2,.3,.1,.2]
            ,[.2,.2,.3,.2,.1]
            ,[.1,.2,.3,.2,.2]
            ,[.2,.1,.3,.2,.2]]
nodeWeights = [10,10,10,10,10]
mc = MarkovChain(transMat,nodeWeights)
mc.simulate(50)
mc.plot(transpose=True)