import csv 

filename = 'ACCIDENT50.csv'
outname = 'ACCIDENT100.csv'
# with open(filename,"r") as fin:
#     with open(outname,"w") as fout:
#         writer=csv.writer(fout)
#         for row in csv.reader(fin):
#             writer.writerow(row[:-1])    
output = open(outname,'w')
for line in open(filename,'r'):
    c = str(','.join( line.split(",")[:-1] )) 
    output.write(c+'\n')


