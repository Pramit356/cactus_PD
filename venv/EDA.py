import csv
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np

#Note: On running thois code, the output graphs appear one after the other so close one to move to next. The program
#ends only after all the graphs are closed

#Performs the group by operation on lst attribute which is branch id
def aggregateList(lst, Tried, Completed):
    merged_list = []
    for i in range(len(lst)):
        x = [row[0] for row in merged_list]
        if lst[i] not in x:
            temp = [lst[i], Tried[i], Completed[i]]
            merged_list.append(temp)
        else:
            merged_list[x.index(lst[i])][1]+=Tried[i]
            merged_list[x.index(lst[i])][2]+=Completed[i]
    return merged_list

#creates a final list by merging the two tables on branch id something like join operation
def cartesianProduct(mergedList, testset):
    final_list = []
    for el in merged_list:
        for el1 in testset:
            if el[0] == el1[0]:
                el1.append(el[1])
                el1.append(el[2])
                final_list.append(el1)
                continue
    return  final_list

BatchId = []
GameId = []
Tried = []
Completed = []

names1 = []
names = []

#Read the file containing output
with open('Sudoku_attemps.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    flag = 0
    for row in reader:
        if flag == 0:
            names = row
            flag = 1
            continue
        else:
            BatchId.append(row[0])
            GameId.append(int(row[1][8:]))
            Tried.append(int(row[2]))
            Completed.append(int(row[3]))
myFile.close()

#Display the effect of game ID on successful completions
x = list(set(GameId))
y = []
yattempts = []
for i in range(max(x)):
    y.append(0)
    yattempts.append(0)
for i in range(len(Tried)):
    y[GameId[i]-1]+=Completed[i]
    yattempts[GameId[i]-1]+=Tried[i]

#Some EDA graphs
y_pos = np.arange(len(x))
plt.bar(y_pos, y, align='center', alpha=0.5)
plt.xticks(y_pos, x)
plt.ylabel('Successful completions')
plt.title('Number of successful completions for each problem')
plt.show()

#Effect of gameid on trials of problems
y_pos = np.arange(len(x))
plt.bar(y_pos, yattempts, align='center', alpha=0.5)
plt.xticks(y_pos, x)
plt.ylabel('Successful attempts')
plt.title('Number of tries for each problem')
plt.show()

#Successful percentage of solved problems
ysuccess = []
for i in range(len(y)):
    if y[i] == 0:
        ysuccess.append(0)
    else:
        ysuccess.append((y[i]/yattempts[i])*100)

y_pos = np.arange(len(x))
plt.bar(y_pos, ysuccess, align='center', alpha=0.5)
plt.xticks(y_pos, x)
plt.ylabel('Successful completions percentage')
plt.title('Percentage completition')
plt.show()
testset = []

#Doing same with the test_conditions file
with open('Test_conditions.csv', newline='') as myFile:
    reader = csv.reader(myFile)
    flag = 0
    for row in reader:
        if flag == 0:
            names1 = row
            flag = 1
            continue
        else:
            BId = row[0]
            SolD = float(row[1])
            SolA = float(row[2])
            Humidity = float(row[3])
            Noise = float(row[4])
            SolB = float(row[5])
            SolC = float(row[6])
            temp = [BId, SolD, SolA, Humidity, Noise, SolB, SolC]
            testset.append(temp)

myFile.close()

#Perform join and groupby
merged_list = aggregateList(BatchId, Tried, Completed)

merged_list = cartesianProduct(merged_list, testset)
print('Final merged list: ',merged_list)

#Finding successrate of merged list
successrate = []
for i in range(len(merged_list)):
    successrate.append((merged_list[i][8]/merged_list[i][7])*100)

#Effect of solution D on success rate
x = [row[1] for row in merged_list]
plt.xlabel('Solution D concentration')
plt.ylabel('Success percentage');
plt.plot(x, successrate, 'o', color='black');
plt.show()

#Effect of solution A on success rate
x = [row[2] for row in merged_list]
plt.xlabel('Solution A concentration')
plt.ylabel('Success percentage');
plt.plot(x, successrate, 'o', color='black');
plt.show()

#Effect of relative humidity on success rate
x = [row[3] for row in merged_list]
plt.xlabel('Relative humidity')
plt.ylabel('Success percentage');
plt.plot(x, successrate, 'o', color='black');
plt.show()

#Effect of white noise on success rate
x = [row[4] for row in merged_list]
plt.xlabel('White noise')
plt.ylabel('Success percentage');
plt.plot(x, successrate, 'o', color='black');
plt.show()

#Effect of solution B on success rate
x = [row[5] for row in merged_list]
plt.xlabel('Solution B concentration')
plt.ylabel('Success percentage');
plt.plot(x, successrate, 'o', color='black');
plt.show()

#Effect of solution C on success rate
x = [row[6] for row in merged_list]
plt.xlabel('Solution C concentration')
plt.ylabel('Success percentage');
plt.plot(x, successrate, 'o', color='black');
plt.show()

#Writing to the output file to be used for linear regression
with open('finaldata.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['Batch ID','Soln D Concentration','Soln A Concentration','Relative Humidity','White Noise (db)',
                     'Soln B Concentration','Soln C Concentration','Tried','Completed','Percentage success'])
    for i in range(len(successrate)):
        temp = merged_list[i]
        temp.append(successrate[i])
        writer.writerow(temp)
writeFile.close()