import csv
import time


class node:
    def __init__(self):
        self.id = ""
        self.transactions = []
        self.pattern = []
        self.support = 1

class cp_miner:
    def __init__(self,f,sup):
        '''
        minimum support will change for test i have taken it as 2
        unique will count the frequency of the 1 items it is kind of header table
        '''

        # file = "Datasets/test1.csv"
        file = f 
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
                        self.count+=1
                    else:
                        self.unique[j] += 1
        print(self.count)
        self.minsupport = sup
        self.after_preprocessing = []
        self.maxlen = 0
        self.map_bits = {}
        self.dbv = []
        self.colossal_pattern = []
        self.count = 0
        self.start = 0

    def preprocess_1_itemset(self):
        '''
        To remove itemset which have count less then minimum support
        and then to remove transaction from dataset
        '''
        for i in self.rows:
            temp = []
            for j in i:
                if self.unique[j] >= self.minsupport:
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
            if values >= self.minsupport:
                forsorting.append(key)
        forsorting = sorted(forsorting)
        for i in range(len(forsorting)):
            self.map_bits[forsorting[i]]= i
        # print(self.map_bits)
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
        self.runminer(level)

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

    def checkequality(self,a,b):
        for i in range(len(a)):
            if a[i]!=b[i]:
                return True
        return False

    def checknull(self,a):
        for i in a:
            if i!=0:
                return False
        return True

    def countone(self,pattern):
        count = 0
        for i in pattern:
            if i==1:
                count += 1
        return count

    def sort_pattern(self,transactions):
        newtransactions = []
        for i in range(len(transactions)):
            countlen = self.countone(transactions[i].pattern)
            newtransactions.append([transactions[i],countlen])
        newtransactions = sorted(newtransactions,key=lambda item:item[1],reverse = True)
        # print(newtransactions)
        transactions = []
        for i in newtransactions:
            # print(i[0].pattern)
            transactions.append(i[0])
        return transactions

    def givestring(self,a):
        strig = ""
        for i in a:
            strig+= str(i)
        return strig

    def runminer(self,level):
        if level.support == self.minsupport:
            # # print("Entered")
            level.transactions = self.sort_pattern(level.transactions)
            patterns = {}
            for nody in level.transactions:
                self.count += 1
                if self.givestring(nody.pattern) not in patterns:
                    patterns[self.givestring(nody.pattern)] = 1
                else:
                    patterns[self.givestring(nody.pattern)] += 1
                checking = self.check_clossal(nody)
                if checking:
                    self.colossal_pattern.append(nody.pattern)
            return
        else:
            level.transactions = self.sort_pattern(level.transactions)
            dont_take = {}
            other = 0
            for i in range(len(level.transactions)):
                node1 = level.transactions[i]
                checker1 = self.givestring(node1.pattern)
                other_level = node()
                if checker1 not in dont_take:
                    # self.count += 1
                    if (node1.support + len(level.transactions) - i -1 ) >= self.minsupport:
                        for j in range(i+1,len(level.transactions)):
                            temp_node = node()
                            node2 = level.transactions[j]
                            cheker = node2.pattern
                            temp_pattern = self.newpattern(node1.pattern,node2.pattern)
                            # print(temp_pattern)
                            if self.checknull(temp_pattern) == False:
                                checking_subset = self.checkmatching(temp_pattern,node2.pattern)
                                temp_node.pattern = temp_pattern
                                temp_node.support = node1.support + 1
                                if checking_subset:
                                    toadd = self.givestring(node2.pattern)
                                    if toadd in dont_take:
                                        dont_take[toadd] +=1
                                        # if level.support == self.minsupport - 1:
                                        #     pass
                                        # else:
                                        other_level.transactions.append(temp_node)
                                    else:
                                        dont_take[toadd] = 1
                                        other_level.transactions.append(temp_node)
                                else:
                                    other_level.transactions.append(temp_node)
                            else:
                                if self.givestring(temp_pattern) in dont_take:
                                    dont_take[self.givestring(temp_pattern)] += 1
                                else:
                                    dont_take[self.givestring(temp_pattern)] = 1
                    other_level.support = level.support + 1
                    self.runminer(other_level)
                else:
                    dont_take[checker1]+=1
                    other+=1

            # print(len(level.transactions), other)
            self.count += len(level.transactions) - other

def main():
    file = "Datasets/test1.csv"
    sup = 4 
    CP_miner = cp_miner(file,sup)
    CP_miner.preprocess_1_itemset()
    CP_miner.assign_dbv()
    start=time.time()
    CP_miner.maketree(CP_miner.dbv)
    end = time.time()
    print("Runtime of the program : ", end-start)
    # print(CP_miner.colossal_pattern)
    # print(len(CP_miner.colossal_pattern))
    # print(CP_miner.count)

if __name__=='__main__':
    main()

