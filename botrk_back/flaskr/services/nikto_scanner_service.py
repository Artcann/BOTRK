from subprocess import Popen, PIPE
import re

def getNiktoScanReport(hostname):

    print(hostname)

    process = Popen(["docker", "run", "frapsoft/nikto", "-host", hostname], stdout=PIPE)

    print("start Nikto scanning...")

    report = ""
    
    for line in process.stdout:
        if("items checked" in line.decode('UTF-8')):
            errors = re.findall(r'\d+', line.decode('UTF-8'))
        elif not line.decode('UTF-8').startswith('-'):
            report += line.decode('UTF-8')

    report = report.replace(" ", "").split("+")

    return [errors, report]