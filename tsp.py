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
    
    def cooling(temp, gamma):
        tnew = temp * gamma

        return tnew

    def func(x1, x2, y1, y2):
        dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)

        return dist
    
    def length(self, df):
        distance = 0
        for idx in range(len(df)-1):
            dist = self.func(df.at[idx,'x'], df.at[idx + 1,'x'], df.at[idx,'y'], df.at[idx + 1,'y'])  # Change to .loc() 
            distance += dist

        return distance 

    def probability(temp, current, old):
        prob = np.e(-(current - old)/temp)
        if min(1, prob) > np.random.randint(0,1):

            return True
        else:

            return False
    
    def swap(self, df):
        dnew = df.copy()

        i = np.random.randint(range(len(df)))
        j = np.random.randint(range(len(df)))
        if i == j:
            while i == j:
                i = np.random.randint(range(len(df)))
                j = np.random.randint(range(len(df)))

        dnew.at[i, 'x'] = df.at[j, 'x']
        dnew.at[i, 'y'] = df.at[j, 'y']
        dnew.at[j, 'x'] = df.at[i, 'x']
        dnew.at[j, 'y'] = df.at[i, 'y']

        return dnew
    
    def run(self):
        iteration = self.iteration
        gamma = self.gamma
        temp = self.gamma
        df = self.df

        version = []
        version_length = []
        current = self.length(df)
        best = current
        version.append(df)
        version_length.append(best)

        for k in range(0, iteration):
            tnew = self.cooling(temp, gamma)

            new = self.swap(df)
            new_length = self.length(new)

            if self.probability(new, df) == True:
               if best > new_length:
                    df = new
                    best = new_length
                    version.append(new)
                    version_length.append(new_length) 
        
        return version, version_length

def main():

    df = dataframe()
    sa = SA(100, .999, 1000, df)
    vers, vers_len = sa.run()


if __name__ == "__main__":
    main()