from subprocess import Popen, PIPE
import re

process = Popen(["docker", "run", "frapsoft/nikto", "-host", "http://45.147.96.25:4242"], stdout=PIPE)

report = ""

for line in process.stdout:
    if("items checked" in line.decode('UTF-8')):
        errors = re.findall(r'\d+', line.decode('UTF-8'))
    elif not line.decode('UTF-8').startswith('-'):
        report += line.decode('UTF-8')

    print(line.decode('UTF-8'), end='')

print(report)