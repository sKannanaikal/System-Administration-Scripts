import csv
import subprocess

DEFAULT_PASSWD = "password"
USERS = set()
GROUPS = {'pubsafety', 'office'}

'''
Tasks that must be finished
1. Use subprocess module and actually run the linux commands - FINISHED I THINK
2. Get all the proper error message to print out into the terminal
3. Pretty Print all the data with colors
4. Clear the terminal Screen whenever necessary
5. Comment the code
6. shebang
7. double check with directions and rubric
'''

def processData(filename):
	with open(filename) as data:
		reader = csv.reader(data)
		next(reader, None)
		for row in reader:
			id = row[0]
			lastName = row[1]
			firstName = row[2]
			office = row[3]
			phone = row[4]
			department = row[5]
			group = row[6]
			addUser(id, lastName, firstName, office, phone, department, group)

def addUser(id, lastName, firstName, office, phone, department, group):
	global DEFAULT_PASSWD
	homeDirectory = createHomeDirectory(department)
	username = generateUsername(lastName, firstName)
	shell = generateShell(group)

	command = 'useradd -m -d {} -s {} -g {} -u {} {}'.format(homeDirectory, shell, group, id, username)
	pipedResults = subprocess.run(["useradd", "-m ", "-d ", str(homeDirectory), " -s ", str(shell), 
		" -g ", str(group), " -u ", str(id), " ", str(username)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	print(pipedResults)

def generateShell(group):
	if group == 'office':
		return '/bin/csh'
	return '/bin/bash'

def createGroups():
	for group in GROUPS:
		command = 'groupadd -f {}'.format(group)
		pipedResults = subprocess.run(["groupadd", " -f ", str(group)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def createHomeDirectory(department):
	pipedResults = subprocess.run(["mkdir", " -f ", "/home/" + str(department)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	print(pipedResults)
	return '/home/{}'.format(department) 

def generateUsername(lastName, firstName):
	username = ''
	try:
		if firstName[0].isalpha():
			username += firstName[0].lower()
		else:
			print("Data entered is not in valid format")
			return None
		usercount = 0
		for letter in lastName:
			if letter.isalpha():
				username += letter.lower()
		while True:
			if username not in USERS:
				print(username)
				USERS.add(username)
				break
			elif username in USERS:
				usercount += 1
				username += str(usercount)
	except:
		print('Insufficient Data')
		return None

	return username
	
	

def main():
	createGroups()
	processData('linux_users.csv')


if __name__ == '__main__':
	main()