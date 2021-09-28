#!/usr/bin/python3

'''
Author: Sean Kannanaikal
Last Updated: 9/28/2021
This is a python script meant to be used by linux administrators to 
help with the task of adding users to a linux device after parsing a csv.
'''

'''
#TODO
1. set password for users
2. double check rubric
3. check if it actually runs
'''

#importing necessary modules
import csv
import subprocess
import os
import time

#setting the defaultt password, a set for USERS, and a set containing valid groups
DEFAULT_PASSWD = "password"
USERS = set()
GROUPS = {'pubsafety', 'office'}

#Color codes for pretty printing the terminal
COLORGREEN = '\33[92m'
COLORRED = '\33[91m'
COLOREND = '\33[0m'

'''
This method will clear the terminal screen whenver it is used
'''
def clearTerminal():
	#running linux command clear
	os.system('clear')

'''
This method will process the paramterized
csv file and create the users
'''
def processData(filename):
	#opening the file
	with open(filename) as data:
		#passing to the csv reader and skipping the header line
		reader = csv.reader(data)
		next(reader, None)

		#going through each row repreesnting a user and attempting to create the user
		for row in reader:
			#all the data found within each row's column
			id = row[0]
			lastName = row[1]
			firstName = row[2]
			office = row[3]
			phone = row[4]
			department = row[5]
			group = row[6]
			#calling the larger addUser method which will end up adding the users
			addUser(id, lastName, firstName, office, phone, department, group)

'''
This method is the core of the program and will take the passed
in values and generate all the parts of the user and if succesful
then it will run a command to create the user
'''
def addUser(id, lastName, firstName, office, phone, department, group):
	#create a reference to the global variable default password
	global DEFAULT_PASSWD

	#creating the homedirectory, the username, and determining the shell the user will have
	homeDirectory = createHomeDirectory(department)
	username = generateUsername(lastName, firstName)
	shell = generateShell(group)

	#making sure there were no errors when identifying aspects of the user if so then print a valid error message and terminate the entry attempt for the user
	if shell == None:
		print("Cannot process Employee ID: {} \t".format(id) + COLORRED + "Not a Valid Group" COLOREND + ".")
		return None
	elif username == None or username == 'Error':
		if username == None:
			print("Cannot process Employee ID: {} \t".format(id) + COLORRED + "Data entered in invalid format" COLOREND + ".")
		elif username == 'Error':
			print("Cannot process Employee ID: {} \t".format(id) + COLORRED + "Insufficient Data" COLOREND + ".")
		return None
	elif homeDirectory == None:
		print("Cannot process Employee ID: {} \t".format(id) + COLORRED + "Not a Valid Group" COLOREND + ".")
		return None

	

	#go ahead and make the user
	pipedResults = subprocess.run(["useradd", "-m ", "-d ", str(homeDirectory), " -s ", str(shell), 
		" -g ", str(group), " -u ", str(id), " ", str(username)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

	#if there were no errors when producing the user's details then print the success message
	print("Processing Employee ID: {} \t {} added to system.".format(id, username))
	print()

'''
This method will determine the shell the user will be using
based on whatever group they are a part of
'''	
def generateShell(group):
	#office users have cshell
	if group == 'office':
		return '/bin/csh'
	#other valid g roup members have bash
	elif group in GROUPS:
		return '/bin/bash'
	#if the user is neither of these types of people then there was an error
	return None

'''
This method will go ahead and create the groups that users can be a part of
'''
def createGroups():
	#looping through the set of groups and adding each group
	for group in GROUPS:
		pipedResults = subprocess.run(["groupadd", " -f ", str(group)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

'''
This method wlil create the homedirectory for the users to be a part of
'''
def createHomeDirectory(department):
	#running the command to create an actual folder and then returning the path to the home directory
	pipedResults = subprocess.run(["mkdir", " -f ", "/home/" + str(department)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	return '/home/{}'.format(department) 

'''
This method will determine the username of the 
user
'''
def generateUsername(lastName, firstName):
	#setting up the username variable
	username = ''
	try:
		#as long as the data is in a valid format then take the first letter from firstname
		if firstName[0].isalpha():
			username += firstName[0].lower()
		else:
			return None
		#user countinng for determining repeats
		usercount = 0

		#looping through the last name and determining all the valid letters and making a username made up of only leters
		for letter in lastName:
			if letter.isalpha():
				username += letter.lower()
		
		#verifying there are no repeat usersnames and appending a count if there is a repeat
		while True:
			if username not in USERS:
				USERS.add(username)
				break
			elif username in USERS:
				usercount += 1
				username += str(usercount)
	except:
		#if there is an error return it
		return 'Error'

	#if everything goes well then return the username
	return username
	
	
'''
This is the main method where all the methods are being called
'''
def main():
	#clearing the terminal
	clearTerminal()

	#providing helpful information at the start of the program's start
	print("Adding new users to the sytem.")
	print("Please Note: The default password for new users is " + COLORGREEN + "password" + COLOREND + ".")
	print("For testing purposes. Change the password to " + COLORGREEN + "1$4pizz@" + COLOREND + ".")
	print()

	#create all the groups users can be apart of
	createGroups()

	#processing the data from the passed in csv file
	processData('linux_users.csv')

	#clear the terminal
	clearTerminal()


#main method being called
if __name__ == '__main__':
	main()
