'''
Author: Sean Kannanaikal
Date: 9/13/2021
'''
import os
import subprocess
import time

def printResults(successful):
	if successful:
		print("Please inform your system administarator that the test was SUCCESSFUL!")
	elif not successful:
		print("Please inform your system administrator that the test has FAILED!")

def clearTerminal():
	os.system('clear')

def pingTest(machine, testType):
	clearTerminal()
	print("Testing Connectivity for " + testType + "...")
	time.sleep(2)
	clearTerminal()
	print("Running test, please wait.")
	time.sleep(2)
	clearTerminal()
	pipedResults = subprocess.run(["ping", "-c 1", str(machine)], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	if pipedResults.returncode == 0:
		successful = True
	else:
		successful = False
	printResults(successful)
	time.sleep(2)
	clearTerminal()


def displayGateway():
	clearTerminal()
	gateway = obtainGateway()
	print("Your gateway IP address is " + gateway)
	time.sleep(2)
	clearTerminal()

def obtainGateway():
	pipedResults = subprocess.run(["ip", "r"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	terminalOutput = pipedResults.stdout.decode('utf-8')
	splitOutput = terminalOutput.split(' ')
	gateway = splitOutput[2]
	return gateway

def main():
	while True:
		clearTerminal()
		print(
		"""
		****************************
		**Ping Test Troubleshooter**
		****************************
		"""
		)
		print("Enter Selection: ")
		print()
		print("\t1 - Test connectivity to your gateway.")
		print("\t2 - Test remote connectivity.")
		print("\t3 - Test for DNS resolution.")
		print("\t4 - Display gateway IP Address")
		print()

		choice = input("Please enter a number (1-4) or 'Q/q' to quit the program.\t")

		if choice == 'Q' or choice == 'q':
			break
		elif choice == '1':
			gateway = obtainGateway()
			pingTest(gateway, 'default gateway')
		elif choice == '2':
			pingTest('8.8.8.8', 'remote connectivity')
		elif choice == '3':
			pingTest('google.com', 'dns resolution')
		elif choice == '4':
			displayGateway()
		else:
			print("Unrecognized input provided")

if __name__ == '__main__':
	main()
