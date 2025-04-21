# Market Direction Predictor (MDP)
predict UP or DOWN days(candles) based on previous sources/indicators on a crypto/forex... markets using neural networks
## why i should use it when there are other libraries for this task?
well...
1. the code is simple,understandable and easy to use. 
2. use this if you don't want a headache on figuring out how to use neural network for market prediction or even reading the documentation page
## will this 100% work.
IDK. the markets no matter crypto,stock,forex... have non stationary behaviour and mostly influenced by economics,news... but if i were to make a code that trades markets i would have 2 choices:
1. is to make a very complicated program that includes many inputs. economics,news,candlestick... which is very difficult to make
2. use a simple method to trade the market like the one written in this code which only trains a neural network on candlesticks (%changes of sources) to predict next candle direction. (BTW i wouldn't suggest you to make a deep neural network it will easily overfit the data and perform poorly. just need a nn that learns the general pattern this model worked fine but don't take my word `MLPClassifier((8,8),"tanh",solver="lbfgs",max_iter=2000)`)

so to answer your question, no it won't.

## so how do i use it ?
the library is a single file called `mdp.py` and
i've put some tests on the file too. this is the simples way of using the code:
```python
from MDP.mdp import MDPC,MLPClassifier
d=[1,2,3 ,2,3,4 ,3,4,5 ,4,5,6] # this is your closing data provided by the Exchange
mdpc=MDPC(wl=2,clf=MLPClassifier()) # wl stands for window length and it controls how far the model sees the past bars to predict next 
ac,cm,npp=mdpc.train_predict(d) # ac:accuracy(number),cm:confusion table(2x2 array),npp:list of 2 numbers first one is the probability in which model thinks it is going down and UP for the second one.
print(ac)
print(cm)
print(npp)
assert npp[0]>npp[1]
``` 
there are 3 classes. `MDPC,MDPHLC,MDPMORE`. MDPHLC accepts HLC and MDPMORE accepts infinity of features (note that all of them compute %change on the data)







btw my github is https://github.com/navidpgg