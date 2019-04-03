import csv

class node:
    def __init__(self):
        self.tids = []
        self.pattern = ""
        self.support = 1

class cp_miner:
    def __init__(self):
        '''
        minimum support will change for test i have taken it as 2
        unique will count the frequency of the 1 items it is kind of header table
        '''
        file = "Datasets/test.csv"
        self.rows = []
        self.count = 0
        self.unique = {}
        with open(file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.rows.append(row)
                for j in row:
                    if j not in self.unique:
                        self.unique[j] = 1
                    else:
                        self.unique[j] += 1
                self.count+=1
        self.minsupport = 2
        self.after_preprocessing = []
        self.maxlen = 0
        self.map_bits = {}
        self.dbv = []

    def preprocess_1_itemset(self):
        '''
        To remove itemset which have count less then minimum support
        and then to remove transaction from dataset
        '''
        for i in self.rows:
            temp = []
            for j in i:
                if self.unique[j] > self.minsupport:
                    temp.append(j)
            if len(temp) != 0:
                self.after_preprocessing.append(sorted(temp))
        self.rows = []

    def assign_dbv(self):
        '''
        Assiging the DBV to the transactions which are left 
        '''
        forsorting = []
        for key,values in self.unique.items():
            if values > self.minsupport:
                forsorting.append(key)
        forsorting = sorted(forsorting)
        for i in range(len(forsorting)):
            self.map_bits[forsorting[i]]= i
        self.maxlen = max(self.maxlen,len(forsorting))
        for i in self.after_preprocessing:
            pattern = [0]*self.maxlen
            for j in i:
                pattern[self.map_bits[j]] = 1
            self.dbv.append(pattern)

def main():
    CP_miner = cp_miner()
    CP_miner.preprocess_1_itemset()
    CP_miner.assign_dbv()

if __name__=='__main__':
    main()

