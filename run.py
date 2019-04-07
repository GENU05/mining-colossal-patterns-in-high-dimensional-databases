
import cp_miner as cp 
import pcp_miner as pcp 
import time 
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.lines as mlines

def newline(p1, p2):
    ax = plt.gca()
    xmin, xmax = ax.get_xbound()

    if(p2[0] == p1[0]):
        xmin = xmax = p1[0]
        ymin, ymax = ax.get_ybound()
    else:
        ymax = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmax-p1[0])
        ymin = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmin-p1[0])

    l = mlines.Line2D([xmin,xmax], [ymin,ymax])
    ax.add_line(l)
    return l

def main():
    f = 'Datasets/T10I4D100K-100.csv'
    sup = [2,3,4]
    cp_time = []
    for i in range(len(sup)):
        CP_miner = cp.cp_miner(f,sup[i])
        start = time.time()
        CP_miner.preprocess_1_itemset()
        CP_miner.assign_dbv()
        # start=time.time()
        CP_miner.maketree(CP_miner.dbv)
        end = time.time()
        cp_time.append("{:10.6f}".format(end - start ) )
        # end = time.time()
        # print("Runtime of the program : ", end-start)
    # for i in range(len(sup)):
    #     print('Sup: ',sup[i],'Time: ',cp_time[i])
    # ##PCP
    pcp_time = []
    for i in range(len(sup)):
        CP_miner = pcp.cp_miner(f,sup[i])
        start = time.time()
        CP_miner.preprocess_1_itemset()
        CP_miner.assign_dbv()
        # start=time.time()
        CP_miner.maketree(CP_miner.dbv)
        end = time.time()
        pcp_time.append("{:10.6f}".format(end - start ) )
        # end = time.time()
        # print("Runtime of the program : ", end-start)
    for i in range(len(sup)):
        # print('Sup: ',sup[i],'CP: ',cp_time[i],'PCP:',pcp_time[i])
        print(cp_time[i] , pcp_time[i])
    return True
   

    x, y , z = sup , cp_time , pcp_time
    # plt.axis(0.01,1)
    # for i in range(0, len(x)):
    #     plt.plot(x[i], y[i], 'r+')
    #     plt.plot(x[i],z[i],'bo')
    plt.title(f)
    plt.xlabel('minSup')
    plt.ylabel('Time(s)')
    plt.xlim(0,5)
    plt.ylim(0,20)
    plt.axis('equal')     
    # line 1 points
    x1=[]
    x1 += x # [10,20,30]
    y1 = y #[20,40,10]
    # plotting the line 1 points 
    plt.plot(x1, y1, label = "line 1",color='red')
    # line 2 points
    x2 = []
    x2 += x # [10,20,30]
    y2 = z # [40,10,30]
    # plotting the line 2 points 
    plt.plot(x1, y2, label = "line 2",color='blue')
    plt.xlabel('x - axis')
    # Set the y axis label of the current axis.
    plt.ylabel('y - axis')
    # Set a title of the current axes.
    plt.title('Two or more lines on same plot with suitable legends ')
    # show a legend on the plot
    plt.legend()
    # Display a figure.
    plt.show()

    # plt.show()


        



if __name__ == '__main__':
    main()