from subprocess import Popen, PIPE
import time
import os

def getDirsearchScanReport(url):
    print(os.getcwd())
    print(url)
    #dirsearch -u http://45.147.96.25:4242/ -w wordlist.txt -t 80 -r -R 1 --suffixes=.php, -o dirsearch_output_test
    process = Popen(["dirsearch", "-u", "http://45.147.96.25:4242/", "-w", "/usr/share/wordlists/dirb/common.txt", "-t", "80", "-r", "-R","1", "--suffixes=.php", "-o", "botrk_back/dirsearch_output_test"], stdout=PIPE)
    start = time.time()
    print("start dirsearch scanning...")


    for line in process.stdout:
        if("Task Completed" in line.decode('UTF-8')):
            end = time.time()
            elapsed = end - start
            print(f'Temps d\'exécution : {elapsed}s')