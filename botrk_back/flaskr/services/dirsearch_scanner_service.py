from subprocess import Popen, PIPE
import re

def getDirsearchScanReport(url, id):

    print(url)
    file_id = "/scan/dirsearch/dirsearch_" + str(id)
    process = Popen(["dirsearch", "-u", url, "-w /usr/share/wordlists/dirb/common.txt", "-t 80", "-r", "--recursion-depth=1", "--suffixes=.php", "-o", file_id], stdout=PIPE)
    start = time.time()
    print("start dirsearch scanning...")


    for line in process.stdout:
        if("Task Completed" in line.decode('UTF-8')):
            end = time.time()
            elapsed = end - start
            print(f'Temps d\'exécution : {elapsed}s')

    f = open(file_id, 'r')
    report = f.read()
    print (report)

    return report

