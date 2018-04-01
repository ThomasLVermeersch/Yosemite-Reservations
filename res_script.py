from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import requests
import re
from collections import defaultdict
import time
import sys
import urllib
from pymongo import MongoClient
import config

client = MongoClient(config.MONGODB_URI, connectTimeoutMS=30000)
db = client[config.DATABASE]
upper = db.upper_pines
lower =	db.lower_pines
crane = db.crane_flat
north =	db.north_pines
waw = db.wawona
hodg = db.hodgdon
#20 weeks (2 * 14 days)
def get_reservation_data(site_dict, url1, num_of_sites):
	now = datetime.datetime.now()
	url2 = '&sitepage=true&startIdx='
	session = requests.Session()
	for i in range(1):
		idx = 0
		nowt = now.strftime("%m/%d/%Y")
		url3 = url1 + str(nowt) + url2
		#Set to number of sites in campground
		while idx < num_of_sites:
			complete_url = url3 + str(idx)
			print(complete_url)
			upper_pines_this_week = session.get(complete_url)
			txt = upper_pines_this_week.text
			res_body = BeautifulSoup(txt, "html.parser").find_all('tbody')
			rows = BeautifulSoup(str(res_body), "html.parser").find_all('tr')
			#loop through all rows in availability table
			for row in rows:
				num = 0
				row_soup = BeautifulSoup(str(row), "html.parser")
				tds = row.find_all('td')
				#Go through each cell in each row
				for td in tds:
					txt2 = td.get_text()
					txt = txt2.split('\n')
					val = txt[0]
					try:
						num = int(txt[3])
					except IndexError:
						pass
					except ValueError:
						pass
					#if the first cell holds an int, we know the following tds are valid reservations for that site
					if num != 0:
						if val == 'X' or val == 'R' or val =='A' or val == 'N' or val == 'W':
							site_dict[str(num)].append(val)
			print(now.strftime("%m/%d/%y"))
			print(idx)
			idx += 25
			time.sleep(.25)
		now = now + timedelta(days=14)

def main():
	#campground dictionaries to hold reservation statuses
	upper_pines = defaultdict(list)
	lower_pines = defaultdict(list)
	crane_flat = defaultdict(list)
	north_pines = defaultdict(list)
	wawona = defaultdict(list)
	hodgdon = defaultdict(list)
	#Base urls
	upper_pines_base_url = 'https://www.recreation.gov/campsiteCalendar.do?page=calendar&contractCode=NRSO&parkId=70925&calarvdate='
	lower_pines_base_url = 'https://www.recreation.gov/campsiteCalendar.do?page=calendar&contractCode=NRSO&parkId=70928&calarvdate='
	crane_flat_base_url ='https://www.recreation.gov/campsiteCalendar.do?page=calendar&contractCode=NRSO&parkId=70930&calarvdate='
	north_pines_base_url = 'https://www.recreation.gov/campsiteCalendar.do?page=calendar&contractCode=NRSO&parkId=70927&calarvdate='
	wawona_base_url = 'https://www.recreation.gov/campsiteCalendar.do?page=calendar&contractCode=NRSO&parkId=70924&calarvdate='
	hodgdon_base_url = 'https://www.recreation.gov/campsiteCalendar.do?page=calendar&contractCode=NRSO&parkId=70929&calarvdate='
	#number of sites at each campground
	up_sites = 234
	lp_sites = 72
	cf_sites = 162
	np_sites = 79
	wa_sites = 97
	ho_sites = 103

	#clear database
	upper.delete_many({})
	lower.delete_many({})
	crane.delete_many({})
	north.delete_many({})
	waw.delete_many({})
	hodg.delete_many({})
	#Populate each Dictionary
	get_reservation_data(upper_pines, upper_pines_base_url, up_sites)	
	get_reservation_data(crane_flat, crane_flat_base_url, cf_sites)
	get_reservation_data(north_pines, north_pines_base_url, np_sites)
	get_reservation_data(wawona, wawona_base_url, wa_sites)
	get_reservation_data(hodgdon, hodgdon_base_url, ho_sites)
	get_reservation_data(lower_pines, lower_pines_base_url, lp_sites)
	for i in upper_pines:
		upper.insert_one({ "_id" : i, "availability" : upper_pines[i]})
	for i in lower_pines:
		lower.insert_one({ "_id" : i, "availability" : lower_pines[i]})
	for i in crane_flat:
		crane.insert_one({ "_id" : i, "availability" : crane_flat[i]})
	for i in north_pines:
		north.insert_one({ "_id" : i, "availability" : north_pines[i]})
	for i in wawona:
		waw.insert_one({ "_id" : i, "availability" : wawona[i]})
	for i in hodgdon:
		hodg.insert_one({ "_id" : i, "availability" : hodgdon[i]})

main()






