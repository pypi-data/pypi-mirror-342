from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
import numpy as np

def percent_change(data):return [100.0*(data[i]-data[i-1])/(data[i-1]) for i in range(1,len(data))]

class MDPC:
    """use source closing price to predict next closing price UP/DOWN"""
    def __init__(self,clf:MLPClassifier=MLPClassifier(),wl=7):
        self.clf=clf
        self.wl=wl
    def train_predict(self,closing:list[float]):
        """trains the model based on %change of closing. return tuple of accuracy,confusion matrix,next prediction probability"""
        data=percent_change(closing)
        assert len(data)==len(closing)-1
        xdata=[]
        ydata=[]
        T=len(data)
        for i in range(T-self.wl):
            current_window=data[i:i+self.wl]
            next_value=data[i+self.wl]
            xdata.append(current_window)
            ydata.append(int(next_value>0.0))
        
        self.clf.fit(xdata,ydata)
        ypred=self.clf.predict(xdata)
        accuracy=accuracy_score(ydata,ypred)
        cm=confusion_matrix(ydata,ypred)

        lastwindow=data[T-self.wl:T]
        predprob=self.clf.predict_proba([lastwindow])
        return accuracy,cm,predprob[0]

class MDPHLC:
    """use source HLC to predict next closing price UP/DOWN"""
    def __init__(self,clf:MLPClassifier=MLPClassifier(),wl=7):
        self.clf=clf
        self.wl=wl
    def train_predict(self,high:list[float],low:list[float],closing:list[float]):
        """trains the model based on %change of HLC data. return tuple of accuracy,confusion matrix,next prediction probability"""
        assert len(high) == len(low) == len(closing), "All input lists must have the same length."
        data=np.array([
            percent_change(high),
            percent_change(low),
            percent_change(closing),
        ])
        assert data.shape==(3,len(closing)-1)
        xdata=[]
        ydata=[]
        T=data.shape[1]
        for i in range(T-self.wl):
            current_window=data[:,i:i+self.wl].flatten(order="F")
            next_close=data[2,i+self.wl]
            xdata.append(current_window)
            ydata.append(int(next_close>0.0))
        
        self.clf.fit(xdata,ydata)
        ypred=self.clf.predict(xdata)
        accuracy=accuracy_score(ydata,ypred)
        cm=confusion_matrix(ydata,ypred)

        lastwindow=data[:,T-self.wl:T].flatten(order="F")
        predprob=self.clf.predict_proba([lastwindow])
        return accuracy,cm,predprob[0]

class MDPMORE:
    """use multiple source/indicators (maybe volume) to predict next closing price UP/DOWN"""
    def __init__(self,clf:MLPClassifier=MLPClassifier(),wl=7):
        self.clf=clf
        self.wl=wl
    def train_predict(self,sources:list):
        """trains the model based on %change of sources. return tuple of accuracy,confusion matrix,next prediction probability. note that sources is a list of list[float]. the last list in sources is the source that needs to be predicted(closing price)"""
        closing_length = len(sources[-1])
        for src in sources:
            assert len(src) == closing_length, "All sources must match the length of the closing prices."
        data=np.array([
            percent_change(src) for src in sources
        ])
        assert data.shape==(len(sources),len(sources[-1])-1)
        xdata=[]
        ydata=[]
        T=data.shape[1]
        for i in range(T-self.wl):
            current_window=data[:,i:i+self.wl].flatten(order="F")
            next_close=data[-1,i+self.wl]
            xdata.append(current_window)
            ydata.append(int(next_close>0.0))
        
        self.clf.fit(xdata,ydata)
        ypred=self.clf.predict(xdata)
        accuracy=accuracy_score(ydata,ypred)
        cm=confusion_matrix(ydata,ypred)

        lastwindow=data[:,T-self.wl:T].flatten(order="F")
        predprob=self.clf.predict_proba([lastwindow])
        return accuracy,cm,predprob[0]

if __name__=="__main__": # simple tests
    d=[1,2,3 ,2,3,4 ,3,4,5 ,4,5,6]
    mdpc=MDPC(wl=2,clf=MLPClassifier())
    ac,cm,npp=mdpc.train_predict(d)
    print(ac)
    print(cm)
    print(npp)
    assert npp[0]>npp[1]
    d=[1,2,3 ,2,3,4 ,3,4,5 ,4,5]
    mdpc=MDPC(wl=2,clf=MLPClassifier())
    ac,cm,npp=mdpc.train_predict(d)
    print(ac)
    print(cm)
    print(npp)
    assert npp[0]<npp[1]
    print("----------------------------------")
    h=[1,2, 1,2, 1,2]
    l=[2,1, 2,1, 2,1]
    c=[3,2, 3,2, 3,2] # next is 3
    mdphlc=MDPHLC(wl=2)
    ac,cm,npp=mdphlc.train_predict(h,l,c)
    print(ac)
    print(cm)
    print(npp)
    assert npp[0]<npp[1]
    h=[1,2, 1,2, 1,2, 1]
    l=[2,1, 2,1, 2,1, 2]
    c=[3,2, 3,2, 3,2, 3]
    mdphlc=MDPHLC(wl=2)
    ac,cm,npp=mdphlc.train_predict(h,l,c)
    print(ac)
    print(cm)
    print(npp)
    assert npp[0]>npp[1]
    print("----------------------------------")
    v=[1,2,3,4, 3,4,5,6,   5,6,7,8, ]
    c=[4,3,2,1, 3,2,1,.5, 2,1,.5,.25, ] # pred should give 1
    mdpmore=MDPMORE(wl=3)
    ac,cm,npp=mdpmore.train_predict([v,c])
    print(ac)
    print(cm)
    print(npp)
    assert npp[0]<npp[1]
    h=[1,2, 1,2, 1,2]
    l=[2,1, 2,1, 2,1]
    c=[3,2, 3,2, 3,2] # next is 3
    mdphlc=MDPMORE(wl=2)
    ac,cm,npp=mdphlc.train_predict([h,l,c])
    print(ac)
    print(cm)
    print(npp)
    assert npp[0]<npp[1]