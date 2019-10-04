import time
import datetime
import requests
from io import BytesIO
import pandas
import sys
import os

qz={}

jz={}

gj={}

tfjz={}

qztfjz={}

yz=0.8

def get_url(url, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text

def get_qz():
    url="http://www.csindex.com.cn/uploads/file/autofile/closeweight/000300closeweight.xls"
    f=requests.get(url)
    x=BytesIO(f.content)
    df=pandas.read_excel(x,converters={u'成分券代码Constituent Code':str})
    df=df.iloc[:,[4,8]]
    return (df)

def convert(df):
    x=df.to_string(index=0,header=0)
    ss=open("x.txt","w")
    ss.write(x)
    ss.close()

def convertx2():
    f=open("x.txt","r")
    x=""
    while 1:
        t=f.readline().lstrip()
        if (t!=''):
            if(t[:2]=="60"):
                t="sh"+t
                t=t.replace("  ",",")
            elif(t[:2]=="00" or t[:2]=="30"):
                t="sz"+t
                t=t.replace("  ",",")
        else:
            break
        x=x+t
    f2=open("x2.txt","w")
    f2.write(x)
    f2.close()
    f.close()

def convertx3():
    f=open("x.txt","r")
    x=""
    while 1:
        t=f.readline().lstrip()
        if (t!=''):
            t=t[:6]+"\n"
        else:
            break
        x=x+t
    f2=open("x3.txt","w")
    f2.write(x)
    f2.close()
    f.close()

def qzzd():
    global qz
    f=open("x2.txt","r")
    while 1:
        t=f.readline()
        if(t!=""):
            n=t[2:8]
            qz[n]=float(t[9:13])/100
        else:
            break
    f.close()

def get_data():
    url='http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields=TCLOSE;'
    f=open("x3.txt","r")

    ta=datetime.datetime.now()

    end = ta.strftime('%Y%m%d')
    m90 = datetime.timedelta(days=-90)

    stt =ta+m90
    start=stt.strftime('%Y%m%d')
    while 1:
        n=f.readline()
        if(n!=""):
            if(n[:2]=="60"):
                xn="0"+n
            elif(n[:2]=="30" or n[:2]=="00"):
                xn="1"+n
            ge=requests.get(url % (xn.strip(),start,end))
            g=ge.content.decode("gbk")
            rq=""
            g=g[g.find("\n")+1:]
            while 1:
                if(len(g)<11):
                    break
                rtd=g[g.find(",")-10:g.find(",")+1]
                for i in range(3):
                    g=g[g.find(",")+1:]
                rtp="%.2f" % float(g[:g.find(",")])
            
                g=g[g.find(",")+1:]
            
                rq=rq+rtd+rtp+"\n"
            
        
            lg=os.getcwd()+"\\D\\"+n.strip()+".txt"
            f2=open(lg,"w")
            f2.write(rq)
            f2.close()
        else:
            break
        time.sleep(0.2)
    f.close()

def jzzd():
    global jz
    f=open("x3.txt","r")
    while 1:
        n=f.readline()
        if(n!=""):
            x=1
            total=0
            avg=0
            lg=os.getcwd()+"\\D\\"+n.strip()+".txt"
            f2=open(lg,"r")
            while 1:
                t=f2.readline()
                if(t!=""):
                    total =total+float(t[t.find(",")+1:t.find("\n")])
                    x+=1
                else:
                    avg=total/x
                    #print (avg)
                    avg2=int(avg*100+0.5)/100
                    #print (avg2)
                    jz[n.strip()]=avg2
                    
                    f2.close()
                    break
        else:
            break
    f.close()

def xlwzdm():
    f=open("x2.txt","r")
    te=''
    while 1:
        t=f.readline()
        if(t!=""):
            te=te+t[:9]
        else:
           break
    f.close()
    f2=open("wz.txt","w")
    f2.write(te)
    f2.close()

def gjzd():
    global gj
    xl="http://hq.sinajs.cn/list="
    f=open("wz.txt","r")
    x=f.read()
    xl=xl+x
    f2=open("x3.txt","r")
    html=get_url(xl)
    while 1:
        n=f2.readline()
        for i in range(3):
            html=html[html.find(",")+1:]
        gj[n.strip()]=float(html[:html.find(",")])
        html=html[html.find("\n")+1:]
        if(html==""):
            break
    f.close()
    f2.close()

def tfjzzd():
    global tfjz,qztfjz
    for key in gj:
        if(gj[key]>jz[key]):
            tfjz[key]=1
        else:
            tfjz[key]=0
    for key in tfjz:
        qztfjz[key]=qz[key]*tfjz[key]
    x=0
    for key in qztfjz:
        x+=qztfjz[key]
    return x

def mkdir():
    path=os.getcwd()+"\\D\\"
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False

if __name__ == "__main__":
    os.system(r"pip3 install requests")
    os.system(r"pip3 install pandas")
    #time.sleep(120)
    #请安装request和pandas模块
    mkdir()
    df=get_qz() #获取权重
    convert(df) 
    convertx2()
    convertx3() #格式转换
    xlwzdm()
    get_data()  #获取90天数据
    qzzd()      #生成权重字典
    jzzd()      #生成90天均值数据字典
    gjzd()      #获取最新股价并生成股价字典
    x=tfjzzd()  #计算在90天均值以上的比例
    if(x>yz):
        print("请满仓300")
    elif(x<(1-yz)):
        print("请空仓")
    else:
        print("请等待")
    while 1:
        time.sleep(5)
