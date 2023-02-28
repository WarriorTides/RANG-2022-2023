import pandas as pd
import numpy as np
import array
# def closest(lst, K):
#     return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def closest(lst, K):
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
    #  return lst[idx]
     return idx

def motors(arr):
    cnt = 0
    for i in arr:
        if arr[i] != 0:
            cnt += 1
    return cnt
# formula: (x / t) * r
def power(arr):
    x = 20 # amp limit
    t = motors(arr) # total number of motors running

    df = pd.read_excel(r"C:\\Users\\ISS\Downloads\datasheetT200Thruster.xlsx")
    # get data
    pwn = df.iloc[:, 0].tolist() # pwn colunmn
    current = df.iloc[:, 2].tolist() # current colunmn

    sum = 0
    for i in arr:
        sum += abs(arr[i])

    out = []
    for i in range(len(arr)):
        
        r = abs(arr[i])
        amp = r / sum
        if r == 0:
            out.append(1500)
            continue
        try:
            idx = current.index(amp)
            pwnCur = current[idx]
            if arr[i] < 0:
                out.append(pwnCur * (-1)) 
            else:
                out.append(pwnCur)
        except ValueError as e:
            # get idx of value closest
            idx =  closest(current, amp)
            pwnCur = pwn[idx]
            if arr[i] < 0:
                out.append(pwnCur * (-1)) 
            else:
                out.append(pwnCur)

    return out

print(power([1,1,1,1,0,0]))

