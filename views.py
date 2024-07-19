from django.shortcuts import render
import pymysql
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import seaborn as sb
import matplotlib.pyplot  as plt

# Create your views here.
def home(request):
  return render(request,"user/index.html")
def register(request):
  return render(request,'user/register.html')
def RegAction(request):
  name=request.POST['name']
  email=request.POST['email']
  mobile=request.POST['mobile']
  address=request.POST['address']
  username=request.POST['username']
  password=request.POST['password']
  con=pymysql.connect(host="localhost",user="root",password="root",database="spam_detect",charset='utf8')
  cur=con.cursor()
  i=cur.execute("insert into user values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
  con.commit()
  if i>0:
    context={'data':'Registration Successful...!!'}
    return render(request,'user/index.html',context)
  else:
    context={'data','Registration Failed...!!'}
    return render(request,'user/index.html',context)
def LogAction(request):
  username=request.POST['username']
  password=request.POST['password']

  con=pymysql.connect(host="localhost",user="root",password="root",database="spam_detect",charset='utf8')
  cur=con.cursor()
  cur.execute("select *  from user")
  data=cur.fetchall()
  for d in data:
    if d[5]==username and d[6] == password:
      return render(request,'user/UserHome.html')
    else:
      context={'data':'Login Failed ....!!'}
      return render(request,'user/index.html',context)
global data
def loaddata(request):
  global data
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  data=pd.read_csv(BASE_DIR+"\\dataset\\twitter.csv")
  context={'data':'Dataset Loaded'}
  return render(request,"user/UserHome.html",context)
def viewdata(request):
  strdata = '<table border=1 align=center width=100%><tr><th><font size=4 color=white>Id</th><th><font size=4 color=white>Tweet</th><th><font size=4 color=white>following</th><th><font size=4 color=white>followers</th><th><font size=4 color=white>actions</th><th><font size=4 color=white>is_retweet</th><th><font size=4 color=white>location</th><th><font size=4 color=white>Type</th></tr><tr>'
  rows=data.shape[0] #no of rows count
  cols=data.shape[1] #no of column count

  for i in range(rows):
    for j in range(cols):
      strdata+='<td><font size=3 color=white>'+str(data.iloc[i,j])+'</font></td>'
    strdata+='</tr></tr>'
  context={'data':strdata}
  return render(request,'user/ViewData.html',context)
global x
global y
def preprocess(request):
  global x
  global y
  a=data['actions'].mean()
  data['actions'].fillna(a,inplace=True)
  b=data['following'].mean()
  data['following'].fillna(b,inplace=True)
  c=data['followers'].mean()
  data['followers'].fillna(c,inplace=True)
  d=data['is_retweet'].mean()
  data['is_retweet'].fillna(d,inplace=True)
  data['Type']=data['Type'].map({'Quality':1,'Spam':0})
  
  x=data[['Id','following','followers','actions','is_retweet']]
  y=data[['Type']]
  
  context={'data':'Preprocess Has Done..!!!'}
  return render(request,'user/UserHome.html',context)
global x_train,x_test,y_train,y_test
def splitdata(request):
  global x_train,x_test,y_train,y_test
  x_train,x_test,y_train,y_test=train_test_split(x,y, test_size=0.1)
  context={'data':'Data Splitting Has Done Train data size is 80%'}
  return render(request,'user/SplitData.html',context)
global model
def generatemodel(request):
  global model
  model=DecisionTreeClassifier()
  model.fit(x_train,y_train)
  pred=model.predict(x_test)
  accuracy = accuracy_score(pred, y_test)
  context={'data':accuracy*100}
  return render(request,'user/Accuracy.html',context)
  
def detectspam(request):
  return render(request,'user/Detection.html')
  #d={'Quality':0,'Spam':1}
  #data['Type']=data['Type'].map(d)
  #sb.countplot(data['Type'])
  #plt.show()
  #return render(request,'user/index.html')

def DetectAction(request):
  i=int(request.POST['id'])
  fg=int(request.POST['following'])
  fr=int(request.POST['followers'])
  act=int(request.POST['actions'])
  ret=int(request.POST['retweet'])


  p=model.predict([[i,fg,fr,act,ret]])
  print("Predicted Value: "+str(p))
  if p[0]==1:
    context={'msg':'Tweet Detected As Quality'}
    return render(request,'user/DetectionRes.html',context)
  else:
    context={'msg':'Tweet Detected As Spam'}
    return render(request,'user/DetectionRes.html',context)
    

  
  
  
  
  
  
