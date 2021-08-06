import pandas as pd
import csv 
import matplotlib.pyplot as plt
import numpy as np

df=pd.read_csv('data_2.csv')

df.plot(x='Date/Time', y='avg_T_in')
plt.xticks(rotation=45)
plt.show()











