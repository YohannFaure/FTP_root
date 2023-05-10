import numpy as np
import os

# Load data
loc1="C:/FTP_root/DATA/acq2106_178/stream.csv"
loc2="C:/FTP_root/DATA/acq2106_377/stream.csv"
loc="C:/FTP_root/DATA/slowmon.npy"
loc_dict="C:/FTP_root/DATA/Full_Daq.npy"

data1=np.loadtxt(loc1,delimiter=",").T
data2=np.loadtxt(loc2,delimiter=",").T

# find the longest one to synchronize
s1=data1.shape[-1]
s2=data2.shape[-1]

if s1>s2:
    arr=np.concatenate((data1[1:,s1-s2:],data2[1:,:]),0)
elif s2>s1:
    arr=np.concatenate((data1[1:,:],data2[1:,s2-s1:]),0)
else :
    arr=np.concatenate((data1[1:,:],data2[1:,:]),0)

# reshape to only keep a multiple of 4 in length
arr=arr[:,-(arr.shape[-1]//4)*4:]

# mean on 4
arr=(arr.reshape((arr.shape[0],arr.shape[1]//4,4))).mean(axis=-1)



np.save(loc,arr)


## This part saves the data in a format usable by all my routines, and converts from voltage to \epsilon
ylabels=["$\epsilon_{{{}}}$".format(i) for i in range(15)]+["$F_n$ (kg)", "$F_s$ (Kg)"]

n=17
skip=[15]

arr=arr[[i for i in range(len(arr)) if not i in skip]]

def V_to_strain(data,amp=495,G=1.79,i_0=0.0017,R=350):
    """
    Applies the conversion from Voltage to Strain
    amp is the amplification factor
    G is the gauge factor
    i_0 is the fixed current
    R is the gauge resistance
    """
    return(data/(amp*R*G*i_0))

def calibration(data):
    force_calib=lambda x : (500/3)*x
    d=lambda x: V_to_strain(x,amp=495,G=1.79,i_0=0.0017,R=350)
    e=lambda x: -V_to_strain(x,amp=495,G=1.86,i_0=0.0017,R=350)
    functions=[e,d,e,e,d,e,e,d,e,e,d,e,e,d,e,force_calib,force_calib]

    for i in range(n):
        data[i]=functions[i](data[i])
    return(data[:n])

data=calibration(arr)

datadict={"data":data,"ylabels":ylabels,"sampling_freq_in":1,"navg":1}

np.save(loc_dict,datadict)


