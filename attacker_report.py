#!/usr/bin/python3

#Author: Sean Kannanaikal 10/30/2021

#importing necessary packages
import re
import datetime
import calendar
import os
from geoip import geolite2

#a dictionary to hold the login info
loginInfo = {}

#regular expression for matching the format of num.num.num.num
patternMatching = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

#variables for colorful printing
COLORGREEN = '\33[92m'
COLORRED = '\33[91m'
COLOREND = '\33[0m'

'''
method for clearing the terminal screen
'''
def clearTerminal():
	#running linux command clear
	os.system('clear')


'''
method that will go through the log file line by line
and check for ips and then record the collected information
to the loginInfo dictionary
'''
def processLog(filename):
	#opening the log file and looping through it
	with open(filename) as file:
		for line in file:
			#checking it the line has a match with the regular expression
			result = patternMatching.search(line)
			#if theres a match
			if result != None:
				#obtain the "ip" verify that it actually is a vvalid ip
				ip = result[0]
				#split into the 4 octets
				octets = ip.split('.')
				#verify that each octet is between 0 - 255
				for octet in octets:
					if int(octet) >= 0 and int(octet) <= 255:
						validIP = True
					else:
						validIP = False
						break
				#if deemed to bea  valid ip then update the dictionary records
				if validIP:
					updateRecords(ip)

'''
will go into the loginInfo dictionary and update the reocrds accordingly
'''
def updateRecords(ip):
	global loginInfo
	#if the ip is within the loginInfo dictionary already increment the value by 1 to know login attempt count increase
	if ip in loginInfo:
		loginInfo[ip] += 1
	#otherwise  add the ip as a new value into the dictionary with a single login attempt as its defualt value
	else:
		loginInfo[ip] = 1

'''
cross reference the geoip database to identify the country of origin for the ip
'''
def identifyCountry(ip):
	try:
		#lookup the ip in the database to identify the name if found with no errors return it
		match = geolite2.lookup(ip)
		country = match.country
		return country
	except:
		#return none if unable to find the country name
		return None


'''
method for printing out the collected information
regarding failed login attempts in a neat and orderly
fashion
'''
def printLog():

	#sorting the collected login info by the number a times an ip tried to login
	global loginInfo
	intermediaryList = sorted(loginInfo.items(), key=lambda x:x[1])
	sortedInformation = dict(intermediaryList)
	
	#obtaining the current date the program is run on and displaying title information
	currentDate = datetime.datetime.now()
	monthNum = currentDate.month
	year = currentDate.year
	day = currentDate.day
	month = calendar.month_name[monthNum]
	print('' + COLORGREEN + 'Attacker Report ' + COLOREND + f'- {month} {day}, {year}')

	print(COLORRED + f'COUNT\t\tIP ADDRESS\t\tCOUNTRY{COLOREND}'  + COLOREND)

	#going through the dictionary of ips and the login attempts count
	for ip in sortedInformation:
		#identifying the country
		country = identifyCountry(ip)
		#if a valid country was not discernable skip over the printing
		if country is None:
			continue
		#print the information out to the terminal
		print(f'{sortedInformation[ip]}\t\t{ip}\t\t{country}')
		


'''
main method where the program running occurs
'''
def main():
	#clearing the terminal
	clearTerminal()
	
	#processing the log and collecting the login attempts
	processLog('syslog.log')

	#pritning the collected information out in a neat fashion
	printLog()
	print()

#running main method
if __name__ == '__main__':
	main()
