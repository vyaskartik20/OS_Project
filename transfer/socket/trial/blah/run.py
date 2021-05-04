import os
import subprocess
import matplotlib.pyplot as plt

N = [10, 20, 30, 40, 50]

# os.system("g++ 1.cpp -o exec")
# os.system("D:\ACADS\summer2021\OS\LAB3\exec 10 0.5 5")

compiler = subprocess.Popen("g++ B18CSE020.cpp -o exec".split(" "), stdout = subprocess.PIPE)
result, error = compiler.communicate()

dataFinal = []
for c in range(1,6):   
    dataPreFinal = []
    for n in N :
        dataArray = []
        
        dataArrayTAT = []
        dataArrayWait = []
        dataArrayResponse = []
        
        for i in range(1,11):
            
            compilerRun = subprocess.Popen(f".\exec {n} 0.5 {c}".split(" "), stdout = subprocess.PIPE)
            resultRun, errorRun = compilerRun.communicate()
            

            for line in resultRun.decode().strip().split("\n"):
                if line.startswith("The average turn") : 
                    val = float(line.split(":: ")[1].strip())
                    dataArrayTAT.append(val)
                    
                if line.startswith("The average waiting") : 
                    val = float(line.split(":: ")[1].strip())
                    dataArrayWait.append(val)
                    
                if line.startswith("The average response") : 
                    val = float(line.split(":: ")[1].strip())
                    dataArrayResponse.append(val)
                    
        mini = dataArrayTAT[0]
        maxi = dataArrayTAT[0]
        avgi = 0
        count = 0
                
        for i in dataArrayTAT :
            count = count + 1
            if(i<mini):
                mini = i
            if(i>maxi):
                maxi = i
            avgi = avgi + i 
        
        avgi = avgi / count
        
        dataArray.append(mini)
        dataArray.append(avgi)   
        dataArray.append(maxi)   
        
        
        mini = dataArrayWait[0]
        maxi = dataArrayWait[0]
        avgi = 0
        count = 0
                
        for i in dataArrayWait :
            count = count + 1
            if(i<mini):
                mini = i
            if(i>maxi):
                maxi = i
            avgi = avgi + i 
        
        avgi = avgi / count
        
        dataArray.append(mini)
        dataArray.append(avgi)   
        dataArray.append(maxi)   
        
        
        mini = dataArrayResponse[0]
        maxi = dataArrayResponse[0]
        avgi = 0
        count = 0
                
        for i in dataArrayResponse :
            count = count + 1
            if(i<mini):
                mini = i
            if(i>maxi):
                maxi = i
            avgi = avgi + i 
        
        avgi = avgi / count
        
        dataArray.append(mini)
        dataArray.append(avgi)   
        dataArray.append(maxi)  
        
        # print(f"dataArray : {len(dataArray)} ")
           
        dataPreFinal.append(dataArray)
        
    
    # print(f"dataPreFinal : {len(dataPreFinal)} ")
          
    dataFinal.append(dataPreFinal)


    
#c n i

for n in range(5):
    for i in range(9):
        if((i/3) == 2 ):
            dataFinal[3][n][i] = dataFinal[0][n][i] - dataFinal[1][n][i]; 
        else:
            dataFinal[3][n][i] = (2*dataFinal[0][n][i]) - dataFinal[2][n][i];

labelY = ["Turn Around Minimum Time", "Turn Around Average Time","Turn Around Maximum Time", "Waiting Minimum Time", "Waiting Average Time", "Waiting Maximum Time", "Response Minimum Time", "Response Average Time ", "Response Maximum Time" ]
plt.xlabel("Number of Process")
# plt.ylabel(labelY)


for g in range(1, 10) :
    plt.ylabel(labelY[g-1])
    for c in range(5):
        arrayPrint = []
        for n in range(5) :
            arrayPrint.append(dataFinal[c][n][g-1])
            
        plt.plot(N, arrayPrint)
        
    plt.legend(["FCFS" , "NPESJF" , "PESJF", "ROUND ROBIN", "PROIRITY" ])
    # plt.show()
    plt.savefig(f"{labelY[g-1]}.png")
    plt.clf()