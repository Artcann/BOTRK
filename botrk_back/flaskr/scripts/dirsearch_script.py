from subprocess import Popen, PIPE
import re
import time


print("http://45.147.96.25:4242")

process = Popen(["dirsearch", "-u", "http://45.147.96.25:4242/", "-w", "/usr/share/wordlists/dirb/common.txt", "-t", "80", "-r", "--recursion-depth=1", "--suffixes=.php", "-o", "/temp_dirsearch.txt"], stdout=PIPE)
start = time.time()
print("start dirsearch scanning...")


for line in process.stdout:
    if("Task Completed" in line.decode('UTF-8')):
        end = time.time()
        elapsed = end - start
        print(f'Temps d\'exécution : {elapsed}s')

f = open('/temp_dirsearch.txt', 'r')
file_contents = f.read()
print (file_contents)
