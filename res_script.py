from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
import requests
import re
from collections import defaultdict
import time

#20 weeks (2 * 14 days)
def get_reservation_data(site_dict, url1, num_of_sites):
	now = datetime.datetime.now()
	url2 = '&sitepage=true&startIdx='
	session = requests.Session()
	for i in range(10):
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
						print(num)
					except IndexError:
						pass
					except ValueError:
						pass
					#if the first cell holds an int, we know the following tds are valid reservations for that site
					if num != 0:
						if val == 'X' or val == 'R' or val =='A' or val == 'N' or val == 'W':
							site_dict[num].append(val)
			print(now.strftime("%m/%d/%y"))
			print(idx)
			idx += 25	
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
	#Populate each Dictionary
	get_reservation_data(upper_pines, upper_pines_base_url, up_sites)
	get_reservation_data(lower_pines, lower_pines_base_url, lp_sites)
	get_reservation_data(crane_flat, crane_flat_base_url, cf_sites)
	get_reservation_data(north_pines, north_pines_base_url, np_sites)
	get_reservation_data(wawona, wawona_base_url, wa_sites)
	get_reservation_data(hodgdon, hodgdon_base_url, ho_sites)
	for i in upper_pines:
		print("Upper Pines Site: ", i, upper_pines[i])
	for i in lower_pines:
		print("Lower Pines Site: ", i, lower_pines[i])
	for i in crane_flat:
		print("Crane Flat Site: ", i, crane_flat[i])
	for i in north_pines:
		print("North Pines Site: ", i, north_pines[i])
	for i in wawona:
		print("Wawona Site: ", i, wawona[i])
	for i in hodgdon:
		print("Hodgdon Site: ", i, hodgdon[i])

main()






