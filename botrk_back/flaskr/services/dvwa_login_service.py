import requests
from bs4 import BeautifulSoup
import os


def getDVWALogin():
	username = 'admin'
	password = 'password'
	
	f = open('dirsearch_output_test.txt', 'r')
	file_contents = f.readlines()

	for line in file_contents:
		address = line[13:].split(' ')[0].strip()
		if "login.php" in address:
			with requests.Session() as session:
				html = session.get(address)
				html_parsed = BeautifulSoup(html.text, "html.parser")
				user_token = html_parsed.find('input', { "type" : "hidden" })['value']
				creds = {
					"username"   : username,
					"password"   : password,
					"Login"      : "Submit",
					"user_token" : user_token
				}
				request = session.post(address, data = creds)
				cookie = html.cookies.get_dict()
	return cookie
