import csv

class node:
    def __init__(self):
        self.id = ""
        self.transactions = []
        self.pattern = []
        self.support = 1

class cp_miner:
    def __init__(self):
        '''
        minimum support will change for test i have taken it as 2
        unique will count the frequency of the 1 items it is kind of header table
        '''
        file = "Datasets/RETAIL.csv"
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
        self.minsupport = 3
        self.after_preprocessing = []
        self.maxlen = 0
        self.map_bits = {}
        self.dbv = []
        self.colossal_pattern = []
        self.count = 0

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

    def maketree(self,pattern):
        levels = []
        level = node()
        for i in range(len(pattern)):
            newnode =  node()
            newnode.support = 1
            newnode.pattern = pattern[i]
            newnode.id = str(i+1)
            level.transactions.append(newnode)
        level.support = 1
        levels.append(level)
        self.runminer(levels)

    def newpattern(self,a,b):
        newpat = []
        for i in range(len(a)):
            newpat.append(a[i]&b[i])
        return newpat

    def checkmatching(self,a,b):
        for i in range(len(a)):
            if b[i] == 1 and a[i] == 0:
                return False
        return True
    def check_clossal(self,node):
        for pattern  in self.colossal_pattern:
            if self.checkmatching(pattern,node.pattern):
                return False
        return True

    def runminer(self,levels):
        new_levels = []
        checker = len(levels)
        for level in levels:
            checker1 = len(level.transactions)
            for i in range(len(level.transactions)-1):
                other_level = node()
                node1 = level.transactions[i]
                checker3 = node1.pattern
                checker4 = node1.id

                for j in range(i+1,len(level.transactions)):
                    self.count += 1
                    node2 = level.transactions[j]
                    checker5 = node2.pattern
                    checker6 = node2.id
                    temp_node = node()
                    temp_node.id = node1.id + node2.id[-1]
                    temp_node.pattern = self.newpattern(node1.pattern,node2.pattern)
                    temp_node.support = node1.support + node2.support
                    if temp_node.support >= self.minsupport:
                        checking = self.check_clossal(temp_node)
                        if checking:
                            self.colossal_pattern.append(temp_node.pattern)
                    other_level.transactions.append(temp_node)
                other_level.support = level.support + 1
                if other_level.support == self.minsupport:
                    pass
                else:
                    new_levels.append(other_level)
        if len(levels)==0:
            return
        else:
            return self.runminer(new_levels)



def main():
    CP_miner = cp_miner()
    CP_miner.preprocess_1_itemset()
    CP_miner.assign_dbv()
    CP_miner.maketree(CP_miner.dbv)
    print(CP_miner.colossal_pattern)
    print(CP_miner.count)

if __name__=='__main__':
    main()

