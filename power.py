import pandas as pd
import numpy as np
# def closest(lst, K):
#     return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def closest(lst, K):
     
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return lst[idx]


x = 20 # amp limit
t = 4 # total number of motors; 2 - 4
b = 1776 # range of power, up to 1899
r = 1 # 0 - 1; reads off of joystick, magnitude of vector

# formula: (x / t) * r

df = pd.read_excel(r"C:\Users\ISS\Downloads\datasheetT200Thruster.xlsx")

# get data
pwn = df.iloc[:, 0].tolist()
current = df.iloc[:, 2].tolist()

try:
    idx = pwn.index(b)
    ampCur = current[idx] 
except ValueError:
    # get values on either side of current 
    c1 =  closest(pwn, b)
    idx = pwn.index(c1)
    
    ampCur = current[idx] + ((current[idx + 1] - current[idx]) * (b - c1) / 4)
    # print ("ampCur ", ampCur)

if ampCur > 20:
    ampCur = 20

# apply formula
ans = (ampCur / t ) * r
print (ans)


