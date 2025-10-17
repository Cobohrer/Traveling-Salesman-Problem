import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt
import random as rnd 
import string



def dataframe():

    alpha = []
    coord = []
    for i in range(ord('a'), ord('z') + 1):
        xrand = np.random.randint(0, 30)
        yrand = np.random.randint(0, 30)

        coord.append([xrand, yrand])
        alpha.append(chr(i))
    
    df = pd.DataFrame(data = coord, index = alpha, columns = ['x', 'y'])

    return df

class SA:
    def __init__(self, iteration, gamma, temp, df):
        # k = iteration, g = gamma, temp = temperature, df = dataframe 
        # initializing some of the constants needed for simualated annealing
        self.iteration = iteration
        self.gamma = gamma
        self.temp = temp
        self.df = df
    
    def cooling(self, temp, gamma):
        tnew = temp * gamma

        return tnew

    def func(self, x1, x2, y1, y2):
        dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)

        return dist
    
    def length(self, df):
        distance = 0
        for idx in range(len(df)-1):
            dist = self.func(df['x'].iloc[idx], df['x'].iloc[idx + 1], df['y'].iloc[idx], df['y'].iloc[idx + 1]) 
            distance += dist

        return distance 

    def probability(self, temp, new, current):
        prob = np.exp(-(new - current)/temp)
        if min(1, prob) > np.random.uniform(0,1):

            return True
        else:

            return False
    
    def swap(self, df):
        dnew = df.copy()

        i = np.random.randint(1, len(df))
        j = np.random.randint(1, len(df))
        if i == j:
            while i == j:
                i = np.random.randint(1, len(df))
                j = np.random.randint(1, len(df))

        dnew.iloc[i], dnew.iloc[j] = dnew.iloc[j].copy(), dnew.iloc[i].copy() 
  
        return dnew
    
    def run(self):
        iteration = self.iteration
        gamma = self.gamma
        temp = self.temp
        df = self.df

        version = []

        current = self.length(df)
        best = current
        df_current = df.copy()

        for k in range(0, iteration):

            df_new = self.swap(df_current)
            new = self.length(df_new)

            if self.probability(temp, new, current):
                df_current = df_new.copy()
                current = new
                if current < best:
                    best = current
                    version.append(df_current.copy())
              
            temp = self.cooling(temp, gamma)
        
        return version, best

def plot(df, animate = False):
    plt.clf()
    plt.plot(df['x'], df['y'], '-o')
    plt.title('TSP')
    plt.xlabel('x position')
    plt.ylabel('y position')

    if animate:
        plt.pause(.3)
        plt.show(block = False)

    else:
        plt.show(block = True)

def main():

    df = dataframe()
    iteration = 1000
    gamma = .99
    temperature = 1000
    sa = SA(iteration, gamma, temperature, df)
    vers, vers_len = sa.run()

    for _, df in enumerate(vers):
        
        plot(df, True)
    
    plot(df)


if __name__ == "__main__":
    main()