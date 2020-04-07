import math
import random
import functools

points=[]
file = open("points.txt","r")
lines = file.readlines()
for line in lines:
    tmp=line.split(" ")
    tmpX=tmp[0] 
    tmpY=tmp[1]
    points.append((int(tmpX),int(tmpY)))

print(len(points))



#generate random 100 bases from the 1000 devices
bases=[]
nbases=100
nNetwork=200
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
def eval(base, maxD=200, maxN=50):
    #define the number of devices on each base
    base_occ=[0]*len(base)
    nConnectedDevices=0
    #list of non-zero base
    base_index=[]
    for j in range(len(base)):
        if base[j]==1:
            base_index.append(j)
    #print(base_index)

    for i in range(len(points)):
        minD=1000000
        cur_base=-1
        for j in base_index:
            d=distance(points[i],points[j])
            if d<minD and base_occ[j]<maxN:
                minD,cur_base=d,j
        if minD<maxD:
            nConnectedDevices+=1
            base_occ[cur_base]+=1
    #print("connectedDevices="+str(nConnectedDevices))
    #print(base_occ)
#    return sum(base_occ)
    return len(base_index)*100/sum(base_occ)

     

#compare function between two base list
def comp(x,y):
    return eval(x)<eval(y)


maxDevices=0    
nCycles=200
for i in range(nCycles):
    #in each cycle, choose 50% individuals from the last generation
    performance=[]
    for base in bases:
        performance.append(eval(base,200,50))
    #print("at cycle "+str(i)+", max connected devices="+str(max(performance)))
    print(str(i)+" "+str(max(performance)))

    bases=sorted(bases,key=lambda x:eval(x))
    bases=bases[len(bases)//2:]

    #generate 50% new children to fill the individuals
    #mutation rate 1%, crossover rate 70%

    mutation_rate=0.1
    while len(bases)<200:
        newBase1,newBase2=crossover(bases)
        bases+=[newBase1,newBase2]
    for base in bases:
        if random.random()<mutation_rate:
            mutation(base)







for base in bases:
    maxDevices=max(maxDevices, eval(points,base))
    
print(maxDevices)
