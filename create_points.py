
import random

points={(0,0)}
points.clear()
print(type(points))
range_x=10000
range_y=10000
npoints=1000

i=0
while i < npoints:
    tmpX=random.randint(1,range_x)
    tmpY=random.randint(1,range_y)
    if (tmpX,tmpY) not in points:
        points.add((tmpX,tmpY))
        i+=1

outFile=open("points.txt","w")

for (x,y) in points:
    outFile.write(str(x)+" "+str(y)+"\n")


print(len(points))