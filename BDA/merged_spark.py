#from pyspark import SparkContext
import datetime
from sklearn.cluster import KMeans
import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2, whiten

from pyspark import SparkConf, SparkContext
conf = (SparkConf()
         .setMaster("local")
         .setAppName("merged_spark")
         .set("spark.executor.memory", "1g"))
sc = SparkContext(conf = conf)



def calc_date(st):
    today=datetime.date.today()
    a=(st.split('T',2))[0].split('-',3)
    b=[]
    for i in a:
        b.append(int(i))
    calc=datetime.date(b[0],b[1],b[2])
    d=today-calc
    return d.days

tim=[]
name=[]
day=[]
sqft=[]

lat_long=[]

dic={}

c=0
with open('/home/chai/Desktop/BDA/Purpleyo_Items.csv','rb') as csvfile:
    reader=csv.DictReader(csvfile,)
#created 4 lists 
    for row in reader:
        tim.append(row['listing_date'])
        name.append(row['building_name'])
        lat_long.append([row['lat'],row['lng']])
        sqft.append(row['sqft'])

#calculated days passed for each data point
    for i in tim:
        day.append(calc_date(i))


    days=np.array(day)

    d=KMeans(n_clusters=3)
    d.fit(days.reshape(-1,1))

    a=int(d.n_clusters)
    i=0
    j=0
#initialize dictionary
    while i<a:
        dic.update({i:[]})
        i+=1
 #   print dic
#fill dictionary with clustered values    
    g=0
    for i in day:
        b=d.predict(i)
        b=int(b)
        dic[b].append([tim[g],lat_long[g],name[g],sqft[g]])
        g+=1

kmeans2_n_clusters=5
#initialie global dictionary    
global_dic={}
i=0
while(i<(a*kmeans2_n_clusters)):
  global_dic.update({i:[]})
  i+=1


count=0

for i in dic:
    cluster_latlong_list=[]
    c=0
    #created temporary list within Each Cluster for Lat-long to be provided for Kmeans2
    for j in dic[i]:
        cluster_latlong_list.append([float(j[1][0]),float(j[1][1])])

#    print cluster_latlong_list

    cluster_latlong_numpy=np.array(cluster_latlong_list)
    
    #x = normalized data (lat,long) , y=corresponding label (cluster to which the lat long belongs)
    x,y = kmeans2(whiten(cluster_latlong_numpy), kmeans2_n_clusters, iter = 20) 
    
    u=0
    for u in y:
        k=int(u)
        global_dic[k+count].append(dic[i][c])
        c+=1
    count+=5
    
for i in global_dic:
	print global_dic[i]
    
filename = "cluster"
building_name=''
building_price=""
row=[]
for i in global_dic:
    filepath = filename +str(i) + ".csv"
    writer=csv.writer(open(filepath,'ab'))
    row=[]
    for j in global_dic[i]:
        building_name=j[2]
        if(building_name==""):
            building_name="empty"
        building_price=j[3]
        row.append(building_name)
        row.append(building_price)
        writer.writerow(row)
        row=[]
        building_name=''
        building_price=0
    
