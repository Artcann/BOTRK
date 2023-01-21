from subprocess import Popen, PIPE
import time
import os

def getDirsearchScanReport(url):
    print(os.getcwd())
    print(url)
    #dirsearch -u http://45.147.96.25:4242/ -w wordlist.txt -t 80 -r -R 1 -e php -f -o dirsearch_output_test.txt
    process = Popen(["dirsearch", "-u", url, "-w", "wordlist.txt", "-t", "80", "-r", "-R","1", "-e", "php", "-f", "-o", "dirsearch_output_test.txt"], stdout=PIPE)
    start = time.time()
    print("start dirsearch scanning...")
    new_file = ""
    report = []
    elapsed = -1


    for line in process.stdout:
        if("Task Completed" in line.decode('UTF-8')):
            end = time.time()
            elapsed = int(end - start)
            print(f'Temps d\'exécution : {elapsed}s')

    file = open('dirsearch_output_test.txt', 'r')
    file_contents = file.readlines()
    for line in file_contents:
        if((line.startswith("200") or line.startswith("301") or line.startswith("302") or line.startswith("403")) and not line[13:].split(' ')[0].strip().endswith("/")):
            new_file += line.strip()
            report.append(line.strip())
            new_file += "\n"
    file.close()
    file = open('dirsearch_output_test.txt', 'w')
    file.seek(0)
    file.write(new_file)
    file.truncate()
    if elapsed == -1:
        status = "An error occured during the scan !"
    else:
        status = "The scan took " + str(elapsed) + " seconds !"
    return[status, report]
