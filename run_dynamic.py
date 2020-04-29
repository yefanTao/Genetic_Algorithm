import math
import random
import functools



file = open("Devices.txt","r")
lines = file.readlines()


# generate a crossover bewteen two base lists
def crossover(bases):
    i,j=random.sample(range(0,len(bases)),2)
    base1,base2=bases[i],bases[j]
    k=random.randint(0,len(base1))
    #print("crossover between "+str(i)+" and "+str(j)+" at point "+str(k))
    newBase1=base1[:k]+base2[k:]
    newBase2=base2[:k]+base1[k:]
    return newBase1,newBase2


# genreate a mutation inside one single base list
def mutation(base):
    i,j=random.sample(range(0,len(base)),2)
    #print("mutation between  point "+str(i)+" and point "+str(j))
    base[i],base[j]=base[j],base[i]

def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])*(point1[0]-point2[0])+(point1[1]-point2[1])*(point1[1]-point2[1]))


# define a evaluation function, returns the connected devices
def eval(devices, base, maxD=400):
    #define the number of devices on each base
    base_occ=[0]*len(base)
    nConnectedDevices=0
    #list of non-zero base
    base_index=[]
    for j in range(len(base)):
        if base[j]==1:
            base_index.append(j)
    #print(base_index)


    for i in range(len(devices)):
        minD=1000000
        cur_base=-1
        for j in base_index:
            d=distance(devices[i],devices[j])
            if d<minD:
                minD,cur_base=d,j
        if minD<maxD:
            nConnectedDevices+=1
            base_occ[cur_base]+=1
    #print("connectedDevices="+str(nConnectedDevices))
    #print(base_occ)
#    return sum(base_occ)
    abw=0
    for occ in base_occ:
        if occ>=20:
            abw+=100
        else:
            abw+=5*occ
    #return len(base_index)*100/sum(base_occ)
    return abw/1000


#compare function between two base list
def comp(x,y):
    return eval(x)<eval(y)



t = 0
nT = 1
points=[([]*1000) for i in range (nT)]
line_index=0
results=[]
while t<nT:
    while line_index < (t+1)*1000:
        line=lines[line_index]
        tmp=line.split(" ")
        tmpX=tmp[2] 
        tmpY=tmp[3]    
        #points[t][i]=(tmpX,tmpY)
        points[t].append((float(tmpX),float(tmpY)))
        line_index+=1

    #generate random 100 bases from the 1000 devices
    bases=[]
    nbases=100
    nNetwork=100
    i,j=0,0
    while i < nNetwork:
        base=[0]*1000
        j=0
        while j < nbases:
            tmp=random.randint(0,999)
            if base[tmp] == 0:
                base[tmp]=1
                j+=1
        bases.append(base)
        i+=1

    max_abw=0    
    nCycles=200
    iCycle=0
    print("cycle, max_abw, coverage rate")
    for iCycle in range(nCycles):
        #in each cycle, choose 50% individuals from the last generation
        performance=[]
        for base in bases:
            performance.append(eval(points[t],base,400))
        #print("at cycle "+str(i)+", max connected devices="+str(max(performance)))
        #print("at time "+str(t)+", cycle "+str(iCycle)+", max_abw="+str(max(performance)))

        base_index=[]
        coverage=0
        for i in range(len(bases[0])):
            if bases[0][i]==1:
                base_index.append(i)
        i=0
        while i<len(points[t]):
            minD=1000000
            cur_base=-1
            j=0
            while j < len(base_index):
            #for j in base_index:
                #print("i="+str(i)+", j="+str(j))
                d=distance(points[t][i],points[t][base_index[j]])
                if d<minD:
                    minD,cur_base=d,j
                j+=1
            if minD<400:
                coverage+=1
            i+=1
        print(str(iCycle)+" "+str(max(performance))+" "+str(coverage/1000.0))

        bases=sorted(bases,key=lambda x:eval(points[t],x,400))
        bases=bases[len(bases)//2:]

        #generate 50% new children to fill the individuals
        #mutation rate 1%, crossover rate 70%

        mutation_rate=0.1
        while len(bases)<nNetwork:
            newBase1,newBase2=crossover(bases)
            bases+=[newBase1,newBase2]
        for base in bases:
            if random.random()<mutation_rate:
                mutation(base)

    for base in bases:
        max_abw=max(max_abw, eval(points[t],base))

    #outputing
    outputFileName1="devices_"+str(t)+".csv"
    outputFileName2="routers_"+str(t)+".csv"
    outputFileName3="edges_"+str(t)+".csv"
    outFile1=open(outputFileName1,"w")
    outFile2=open(outputFileName2,"w")
    outFile3=open(outputFileName3,"w")

    outFile1.write("Id,Time,Longitude,Latitude,type\n")
    i=0
    while i<len(points[t]):
        outFile1.write(str(i)+","+str(t)+","+str(points[t][i][0])+","+str(points[t][i][1])+","+"device\n")
        #print(str(i)+","+str(t*100)+","+str(points[t][i][0])+","+str(points[t][i][1])+","+"device\n")
        i+=1
    print("writing device files at time "+str(t)+"...\n")
    outFile1.close()

    outFile2.write("Id,Time,Longitude,Latitude,type\n")
    i=0
    iRouter=1000
    while i<len(bases[0]):
        if bases[0][i]==1:
            outFile2.write(str(iRouter)+","+str(t)+","+str(points[t][i][0])+","+str(points[t][i][1])+","+"router\n")
            iRouter+=1
        i+=1
    print("writing router files at time "+str(t)+"...\n")
    outFile2.close()

    outFile3.write("Time,Source,Target\n")
    base_index=[]
    coverage=0
    for i in range(len(bases[0])):
        if bases[0][i]==1:
            base_index.append(i)
    i=0
    while i<len(points[t]):
        minD=1000000
        cur_base=-1
        j=0
        while j < len(base_index):
        #for j in base_index:
            #print("i="+str(i)+", j="+str(j))
            d=distance(points[t][i],points[t][base_index[j]])
            if d<minD:
                minD,cur_base=d,j
            j+=1
        if minD<400:
            coverage+=1
            outFile3.write(str(t)+","+str(1000+cur_base)+","+str(i)+"\n")
        i+=1
    print("writing dege files at time "+str(t)+"...\n")
    outFile3.close()

    print("at time "+str(t)+", max_abw="+str(max_abw)+", coverage rate="+str(coverage/1000.0))
    results.append((t,max_abw,coverage/1000.0))
    t+=1

for i,j,k in results:
    print(str(i)+" "+str(j)+" "+str(k))






