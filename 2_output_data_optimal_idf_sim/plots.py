import pandas as pd
import numpy as np
import matplotlib.pylab as plt


n_steps=6 #n. of steps in an hour 
#dataframe with timestep of 10 minutes 
df=pd.read_csv('opt_conf.csv')
#dataframe with hourly values 
df1 = df.rolling(n_steps).mean() 
df1 = df.iloc[::n_steps, : ]
df1 = df1.reset_index()

columns=['T_out', 'Cooling Power', 'Heating Power', 'avg_T_in'] #measurements of interest
xt=range(0, len(df1)+1, 200) #range for xticks
xl=[] #list of labels for xtixks
titles=['Outdoor Temperature over the year', 'Cooling Consumption over the year', 'Heating Consumption over the year', 'Average Indoor Temperature over the year']
ylables=['Temperature [°C]', 'Consumption [kWh]', 'Consumption [kWh]', 'Temperature [°C]']
xlabel='Dates'


k=0

for i in xt:
	xl.append(df1.iloc[i]['Date/Time'].split(' ')[1])    

for column in columns:
    
    fig, ax = plt.subplots()

    df1.plot(ax=ax, xticks=xt, y= column, rot=45)
    ax.set_xticklabels(xl)
    plt.legend(fontsize=13)
    plt.title(titles[k], fontsize=15)
    plt.xlabel(xlabel, fontsize=13) 
    plt.ylabel(ylables[k], fontsize=13)
    plt.grid(axis='y')
    plt.show()
    k+=1
    


