##########################################################################################
#   Script for the Download of historic data of weatherstation from Weatherundergound    #
#  The request info are the ID of the Station and the start and end date of the series   #
#    Developed by Lorenzo Bottaccioli    for info lorenzo.bottaccioli@polito.it   #
##########################################################################################
#   Script for the Download of historic data of weatherstation from Weatherundergound    #
#  The request info are the ID of the Station and the start and end date of the series   #
#    Developed by Lorenzo Bottaccioli    for info lorenzo.bottaccioli@polito.it   #
##########################################################################################

import datetime, datetime
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

	
start='2013-01-01' ###YYYY-MM-DD
end='2014-01-01'
PWS="LGAV"


def main(PWS,start,end):
	start_date=datetime.datetime.strptime(start,'%Y-%m-%d')
	end_date= datetime.datetime.strptime(end,'%Y-%m-%d')
	delta = datetime.timedelta(days=1)
	cur_date=start_date


	url = "https://www.wunderground.com/weatherstation/WXDailyHistory.asp"

	

	lookup_url = "http://www.wunderground.com/history/daily/gr/spata/{}/date/{}-{}-{}"
	headers = {
		'cache-control': "no-cache",
		'postman-token': "72eed757-662e-d840-6ec2-4c0da5caaff9"
		}
	fields=['Date_Time','Temperature_C','Dew_Point_C','Humidity','Wind','Speed_m/s','Gust_m/s','Pressure_Pa','Precip_Rate_mm','Precip_Accum_mm','UV','Solar_W/m2']

	arr=["North","NNE","NE","ENE","East","ESE", "SE", "SSE","South","SSW","SW","WSW","West","WNW","NW","NNW"]    

	values={}
	df=pd.DataFrame(columns=fields)
	while cur_date <= end_date:
		print (cur_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
		   
		url = lookup_url.format(PWS, cur_date.year,cur_date.month, cur_date.day)
		
		#response = requests.request("GET", url, headers=headers)
		options = Options()
		options.add_argument('--headless')
		driver = webdriver.Chrome(options=options)
		driver.get(url)
		time.sleep(15)
		html = driver.page_source
		
		#response = requests.request("GET", url, headers=headers)
		soup = BeautifulSoup(html, features="html.parser")
		#soup = BeautifulSoup(response.text, features="html.parser")
		#text_file = open("Airport.txt", "w")
		#text_file.write("url: "+url+"\n\n"+ str(soup))
		#text_file.close()
		for row in soup.findAll('tr'):
			if len(row.findAll('td')) == 10:
				#print("\nrow: \n", row)
				for i,col in enumerate(row.findAll('td')):
					if fields[i]=='Date_Time':
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						values[fields[i]] = cur_date.strftime('%Y-%m-%d')+' '+a
					elif fields[i] in ['Temperature_C','Dew_Point_C']:
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						if a[-1]=='F':
							try:
								a=float(a[:-2])
							except:
								pass
							values[fields[i]] = a
						else:
							try:
								a=float(a[:-2])
							except:
								pass
							values[fields[i]] = a
					elif fields[i] in ['Precip_Rate_mm', 'Precip_Accum_mm']:
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						if a[-2:] == 'in':
							try:
								a=float(a[:-2])
							except:
								pass
							values[fields[i]] = a
						else:
							try:
								a=float(a[:-2])
							except:
								pass
							values[fields[i]] = a
					elif fields[i] == 'Pressure_Pa':
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						if a[-2:] == 'in':
							try:
								a=float(a[:-2])
							except:
								pass
							values[fields[i]] = a
						else:
							try:
								a=float(a[:-2])
							except:
								pass
							values[fields[i]] = a
					elif fields[i] in ['Speed_m/s', 'Gust_m/s']:
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						if a[-3:] == 'mph':
							try:
								a=float(a[:-3])
							except:
								pass
							values[fields[i]] = a #mph
						else:
							try:
								a=float(a[:-3])
							except:
								pass
							values[fields[i]] = a
					elif fields[i] == 'Humidity':
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						try:
							a=float(a[:-1])
						except:
							pass
						values[fields[i]] = a
					elif fields[i] == 'Solar_W/m2':
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						try:
							a=float(a[:-5])
						except:
							pass
						values[fields[i]] = a
					elif fields[i] == 'Wind':
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						try:
						   a=arr.index(a)*22.5
						   values[fields[i]] = a
						except:
						   values[fields[i]]=0
					else:
						a = re.sub('(<.*?>|&.*?;)','',str(col)).strip('\n')
						values[fields[i]] = a
				#print("values: ", values)
				df=df.append(values,ignore_index=True)

		
		cur_date+=delta
		driver.quit()

	df.to_csv(PWS+'_from_'+start+'_to_'+end,index=False)
if __name__ == "__main__":           
   
	main(PWS,start,end)

